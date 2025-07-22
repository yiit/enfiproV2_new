import os
import json
import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.core.management import call_command
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.text import get_valid_filename
from products.models import Product
from django.apps import apps


def get_products(request):
    try:
        with open('products_data.json', 'r', encoding='utf-8') as f:
            products = json.load(f)
        return JsonResponse({'products': products}, status=200)
    except FileNotFoundError:
        return JsonResponse({'error': 'Veri dosyası bulunamadı!'}, status=404)

@csrf_exempt
def export_data(request):
    model_name = request.GET.get('model_name', None)

    # Ekstra loglama
    print("GET Parametreleri:", request.GET)
    print("Model Name:", model_name)

    if not model_name or '.' not in model_name:
        return JsonResponse({'error': 'App ve model isimleri belirtilmelidir.'}, status=400)

    app_name, model_name = model_name.split('.', 1)

    # Uygulama ve model doğrulaması
    if not apps.is_installed(app_name):
        return JsonResponse({'error': f'{app_name} uygulaması bulunamadı.'}, status=400)

    try:
        apps.get_model(app_name, model_name)
    except LookupError:
        return JsonResponse({'error': f'{model_name} modeli bulunamadı.'}, status=400)

    # Dosya yolu ve media klasör kontrolü
    os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
    file_name = f"{model_name}_data.json"
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)

    # Veriyi JSON formatında dışa aktarma
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            call_command('dumpdata', f'{app_name}.{model_name}', indent=4, stdout=file)
        return JsonResponse({'message': f"Data başarıyla {file_name} dosyasına kaydedildi.", 'file_path': file_path})
    except Exception as e:
        return JsonResponse({'error': f'Veri dışa aktarma sırasında hata oluştu: {str(e)}'}, status=500)

@csrf_exempt
def import_data(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Sadece POST isteği kabul edilir.'}, status=405)

    uploaded_file = request.FILES.get('json_file')
    if not uploaded_file:
        return JsonResponse({'error': 'Bir JSON dosyası yüklenmelidir.'}, status=400)

    try:
        data = json.load(uploaded_file)

        from products.models import Category
        default_category = Category.objects.first()
        if not default_category:
            return JsonResponse({'error': 'Veritabanında en az bir kategori bulunmalıdır.'}, status=500)

        for item in data:
            if item['model'] == 'products.product':
                category_id = item['fields'].get('category')
                if not Category.objects.filter(id=category_id).exists():
                    item['fields']['category'] = default_category.id
                    print(f"🔄 Kategori ID'si bulunamadı, varsayılan kategori ({default_category.id}) atandı.")

        # Geçici olarak kaydet ve yükle
        os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
        temp_path = os.path.join(settings.MEDIA_ROOT, 'temp_upload.json')
        with open(temp_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        call_command('loaddata', temp_path)
        os.remove(temp_path)

        return JsonResponse({'message': 'Veri başarıyla içe aktarıldı.'})
    
    except json.JSONDecodeError as e:
        return JsonResponse({'error': f'Geçersiz JSON formatı: {str(e)}'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'İçe aktarma hatası: {str(e)}'}, status=500)



@csrf_exempt
def update_remote(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Sadece POST isteği kabul edilir.'}, status=405)

    remote_ip = request.POST.get('remote_ip').strip()
    json_file = request.FILES.get('json_file')

    if not remote_ip or not json_file:
        return JsonResponse({'error': 'IP adresi ve JSON dosyası gereklidir.'}, status=400)

    # Dosyayı güvenli bir şekilde kaydet
    os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
    file_path = os.path.join(settings.MEDIA_ROOT, get_valid_filename(json_file.name))

    with open(file_path, 'wb') as f:
        for chunk in json_file.chunks():
            f.write(chunk)

    # JSON dosyası doğrulaması
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
    except json.JSONDecodeError as e:
        return JsonResponse({'status': 'error', 'message': f'Hata: JSON dosyası doğrulanamadı: {str(e)}'}, status=400)

    # Uzak sisteme POST isteği gönder
    remote_url = f'{remote_ip}/database/update/'
    try:
        headers = {'Content-Type': 'application/json'}
        response = requests.post(remote_url, json=json_data, headers=headers, timeout=10)
        response.raise_for_status()
        os.remove(file_path)  # Dosyayı işlem sonrası sil
        return JsonResponse({'status': 'success', 'remote_response': response.json()})
    except requests.RequestException as e:
        return JsonResponse({'status': 'error', 'message': f'Uzak sistemle iletişim kurulamadı: {str(e)}'}, status=500)

def get_models(request):
    """
    Tüm kayıtlı Django modellerini (tabloları) döndür.
    """
    models = []
    for app in apps.get_app_configs():
        for model in app.get_models():
            models.append({
                "app_label": app.label,
                "model_name": model.__name__,
                "verbose_name": model._meta.verbose_name,
            })
    return JsonResponse(models, safe=False)

def data_management(request):
    return render(request, 'database/data_management.html')

from products.models import Category  # Kategori modelini içe aktar

from products.models import Category

@csrf_exempt
def update(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Sadece POST isteği kabul edilir.'}, status=405)

    json_data = request.FILES.get('json_file')
    if not json_data:
        return JsonResponse({'error': 'JSON dosyası gereklidir.'}, status=400)

    try:
        # JSON dosyasını oku ve doğrula
        data = json.load(json_data)
        if not isinstance(data, list):
            return JsonResponse({'error': 'Geçersiz JSON formatı: Liste bekleniyor.'}, status=400)

        # Kategorileri kontrol et ve eksik olanları oluştur
        category_ids = set()  # Eşsiz kategori ID'leri toplamak için

        for item in data:
            model_name = item.get('model')
            if model_name == 'products.product':
                category_id = item['fields'].get('category')
                if category_id:
                    category_ids.add(category_id)

        # Eksik kategorileri oluştur
        for category_id in category_ids:
            category, created = Category.objects.get_or_create(
                id=category_id,
                defaults={'name': f'Otomatik Kategori {category_id}'}
            )
            if created:
                print(f'✅ Yeni kategori oluşturuldu: {category_id}')
            else:
                print(f'📦 Mevcut kategori bulundu: {category_id}')

        # JSON verisini geçici bir dosyaya kaydet
        temp_file_path = os.path.join(settings.MEDIA_ROOT, 'temp_data.json')
        with open(temp_file_path, 'w', encoding='utf-8') as temp_file:
            json.dump(data, temp_file, ensure_ascii=False, indent=4)

        # Veritabanına yükle
        try:
            call_command('loaddata', temp_file_path)
            os.remove(temp_file_path)  # Geçici dosyayı sil
            return JsonResponse({'status': 'success', 'message': 'Veri başarıyla yüklendi.'})
        except Exception as e:
            print(f'❌ Veri yükleme hatası: {str(e)}')
            return JsonResponse({'error': f'Problem installing fixtures: {str(e)}'}, status=500)

    except json.JSONDecodeError as e:
        print(f'❌ Geçersiz JSON dosyası: {str(e)}')
        return JsonResponse({'error': f'Geçersiz JSON dosyası: {str(e)}'}, status=400)