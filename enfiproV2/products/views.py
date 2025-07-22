import os
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Category, Product
from products.models import Product
from django_pos import settings

import subprocess
import sys

from django.core.management import call_command
from io import StringIO

@login_required
def run_migrate_data(request):
    try:
        output = StringIO()
        call_command('migrate_data', stdout=output)
        return JsonResponse({
            'success': True,
            'output': output.getvalue()
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        })
"""
def run_migrate_data(request):
    # Sanal ortamın Python yorumlayıcısını dinamik olarak al
    python_path = sys.executable
    script_path = r"D:\enfiproV2\enfiproV2\enfiproV2\migrate_data.py"

    try:
        result = subprocess.run([python_path, script_path], capture_output=True, text=True)
        
        if result.returncode == 0:
            return JsonResponse({
                "success": True, 
                "message": "Veri taşıma işlemi başarılı!", 
                "output": result.stdout
            })
        else:
            return JsonResponse({
                "success": False, 
                "message": "Betiği çalıştırırken bir hata oluştu.", 
                "error": result.stderr
            })

    except Exception as e:
        return JsonResponse({
            "success": False, 
            "message": str(e)
        })
"""
        
@login_required(login_url="/accounts/login/")
def categories_list_view(request):
    context = {
        "active_icon": "products_categories",
        "categories": Category.objects.all()
    }
    return render(request, "products/categories.html", context=context)

@login_required(login_url="/accounts/login/")
def categories_add_view(request):
    context = {
        "active_icon": "products_categories",
        "category_status": Category.status.field.choices
    }

    if request.method == 'POST':
        data = request.POST
        attributes = {
            "name": data.get('name'),
            "status": data.get('state'),
            "description": data.get('description')
        }

        if Category.objects.filter(**attributes).exists():
            messages.error(request, 'Kategori Zaten Var!', extra_tags="warning")
            return redirect('products:categories_add')

        try:
            Category.objects.create(**attributes)
            messages.success(request, f'Kategori: {attributes["name"]} Oluşturuldu!', extra_tags="success")
            return redirect('products:categories_list')
        except Exception as e:
            messages.error(request, 'Kategori Oluşturulken Hata Oluştu!', extra_tags="danger")
            print(e)
            return redirect('products:categories_add')

    return render(request, "products/categories_add.html", context=context)

@login_required(login_url="/accounts/login/")
def categories_update_view(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        messages.error(request, 'Kategori Bulunamadı!', extra_tags="danger")
        return redirect('products:categories_list')

    context = {
        "active_icon": "products_categories",
        "category_status": Category.status.field.choices,
        "category": category
    }

    if request.method == 'POST':
        data = request.POST
        attributes = {
            "name": data.get('name'),
            "status": data.get('state'),
            "description": data.get('description')
        }

        if Category.objects.filter(**attributes).exclude(id=category_id).exists():
            messages.error(request, 'Bu Kategori Benzeri Zaten Var!', extra_tags="warning")
            return redirect('products:categories_update', category_id=category_id)

        try:
            Category.objects.filter(id=category_id).update(**attributes)
            messages.success(request, f'Category: {attributes["name"]} updated successfully!', extra_tags="success")
            return redirect('products:categories_list')
        except Exception as e:
            messages.error(request, 'Kategori Güncellenirken Hata Oluştu!', extra_tags="danger")
            print(e)
            return redirect('products:categories_update', category_id=category_id)

    return render(request, "products/categories_update.html", context=context)

@login_required(login_url="/accounts/login/")
def categories_delete_view(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
        category.delete()
        messages.success(request, f'Kategori: {category.name} silindi!', extra_tags="success")
        return redirect('products:categories_list')
    except Category.DoesNotExist:
        messages.error(request, 'Kategori Bulunamadı!', extra_tags="danger")
        return redirect('products:categories_list')
    except Exception as e:
        messages.error(request, 'Kategori Silinirken Hata Oluştu!', extra_tags="danger")
        print(e)
        return redirect('products:categories_list')

@login_required(login_url="/accounts/login/")
def products_list_view(request):
    context = {
        "active_icon": "products",
        "products": Product.objects.all()
    }
    return render(request, "products/products.html", context=context)

@login_required(login_url="/accounts/login/")
def products_add_view(request):
    # Ürünlerin toplam sayısını al
    last_product = Product.objects.order_by('id').last()
    try:
        if (last_product != None):
          print(last_product.id)
          product = Product.objects.get(id=(last_product.id))
          fields = [
            #{"name": "urun_kod", "label": "Ürün Kodu", "type": "text", "value": str(int(product.urun_kod) + 1)}
            {"name": "urun_kod", "label": "Ürün Kodu", "type": "text", "value": product.urun_kod, "is_textarea": False},
            {"name": "urun_ismi1", "label": "Ürün İsmi 1", "type": "text", "value": product.urun_ismi1,"is_textarea": False},
            {"name": "urun_ismi2", "label": "Ürün İsmi 2", "type": "text", "value": product.urun_ismi2,"is_textarea": False},
            {"name": "urun_grup", "label": "Ürün Grubu", "type": "text", "value": product.urun_grup,"is_textarea": False},
            {"name": "urun_tip", "label": "Ürün Tipi", "type": "select", "value": product.urun_tip,"choices": [("ADET", "Adet"),("AGIRLIK", "Ağırlık"),("SABITFIYAT", "Sabit Fiyat"),("SABITAGIRLIK", "Sabit Ağırlık")]},
            {"name": "urun_fiyat", "label": "Ürün Fiyat ₺", "type": "number", "value": product.urun_fiyat,"step": "0.001","is_textarea": False},
            {"name": "urun_musteri", "label": "Ürün Müşteri", "type": "text", "value": product.urun_musteri,"is_textarea": False},
            {"name": "urun_barkod", "label": "Ürün Barkod", "type": "number", "value": product.urun_barkod,"step": "1","is_textarea": False},
            {"name": "urun_qrkod", "label": "Ürün QRkod", "type": "text", "value": product.urun_qrkod,"is_textarea": False},
            {"name": "urun_stt", "label": "Ürün STT", "type": "number", "value": product.urun_stt,"step": "1","is_textarea": False},
            {"name": "urun_resim", "label": "Ürün Resim", "type": "text", "value": product.urun_resim,"is_textarea": False},
            {"name": "urun_min", "label": "Ürün Min", "type": "number", "value": product.urun_min,"step": "0.001","is_textarea": False},
            {"name": "urun_max", "label": "Ürün Max", "type": "number", "value": product.urun_max,"step": "0.001","is_textarea": False},
            {"name": "urun_hedef", "label": "Ürün Hedef", "type": "number", "value": product.urun_hedef,"step": "1","is_textarea": False},
            {"name": "urun_adet_gramaj", "label": "Ürün Adet Gramaj", "type": "number", "value": product.urun_adet_gramaj,"step": "0.0001","is_textarea": False},
            {"name": "urun_dara", "label": "Ürün Dara", "type": "number", "value": product.urun_dara,"step": "0.001","is_textarea": False},
            {"name": "urun_adet", "label": "Ürün Adet", "type": "number", "value": product.urun_adet,"step": "1","is_textarea": False},
            {"name": "urun_etiket", "label": "Ürün Etiket", "type": "text", "value": product.urun_etiket,"is_textarea": False},
            {"name": "urun_top_etiket", "label": "Ürün Toplam Etiketi", "type": "text", "value": product.urun_top_etiket,"is_textarea": False},
            {"name": "urun_izleme", "label": "Ürün İzleme", "type": "text", "value": product.urun_izleme,"is_textarea": False},
            {"name": "urun_kodtip", "label": "Ürün Kod Tipi", "type": "text", "value": product.urun_kodtip,"is_textarea": False},
            {"name": "urun_tablo", "label": "Ürün Tablo", "type": "text", "value": product.urun_tablo,"is_textarea": False},
            {"name": "urun_mesaj1", "label": "Ürün Mesaj1", "type": "text", "value": product.urun_mesaj1,"is_textarea": True},
            {"name": "urun_mesaj2", "label": "Ürün Mesaj2", "type": "text", "value": product.urun_mesaj2,"is_textarea": True},
            {"name": "urun_mesaj3", "label": "Ürün Mesaj3", "type": "text", "value": product.urun_mesaj3,"is_textarea": True},
            {"name": "urun_mesaj4", "label": "Ürün Mesaj4", "type": "text", "value": product.urun_mesaj4,"is_textarea": True},
            {"name": "urun_mesaj5", "label": "Ürün Mesaj5", "type": "text", "value": product.urun_mesaj5,"is_textarea": True},
            {"name": "urun_mesaj6", "label": "Ürün Mesaj6", "type": "text", "value": product.urun_mesaj6,"is_textarea": True},
            {"name": "urun_mesaj7", "label": "Ürün Mesaj7", "type": "text", "value": product.urun_mesaj7,"is_textarea": True},
            {"name": "urun_mesaj8", "label": "Ürün Mesaj8", "type": "text", "value": product.urun_mesaj8,"is_textarea": True},
            {"name": "urun_mesaj9", "label": "Ürün Mesaj9", "type": "text", "value": product.urun_mesaj9,"is_textarea": True},
            {"name": "urun_tanim", "label": "Ürün Tanımı", "type": "text", "value": product.urun_tanim,"is_textarea": True},
            {"name": "urun_icerik", "label": "Ürün İçeriği", "type": "text", "value": product.urun_icerik,"is_textarea": True},
            {"name": "urun_aciklama", "label": "Ürün Açıklaması", "type": "text", "value": product.urun_aciklama,"is_textarea": True},
            {"name": "urun_mensei", "label": "Ürün Menşei", "type": "text", "value": product.urun_mensei,"is_textarea": False}
          ]
        else:
            product = None
            fields = [
                {"name": "urun_kod", "label": "Ürün Kodu", "type": "text", "value": "","is_textarea": False},
                {"name": "urun_ismi1", "label": "Ürün İsmi 1", "type": "text", "value": "","is_textarea": False},
                {"name": "urun_ismi2", "label": "Ürün İsmi 2", "type": "text", "value": "","is_textarea": False},
                {"name": "urun_grup", "label": "Ürün Grubu", "type": "text", "value": "","is_textarea": False},
                {"name": "urun_tip", "label": "Ürün Tipi", "type": "select", "value": product.urun_tip,"choices": [("ADET", "Adet"),("AGIRLIK", "Ağırlık"),("SABITFIYAT", "Sabit Fiyat"),("SABITAGIRLIK", "Sabit Ağırlık")]},
                {"name": "urun_musteri", "label": "Ürün Müşteri", "type": "text", "value": 0,"is_textarea": False},
                {"name": "urun_barkod", "label": "Ürün Barkod", "type": "number", "value": 0,"step": "any", "min": "0","is_textarea": False},
                {"name": "urun_qrkod", "label": "Ürün QRkod", "type": "text", "value": "","is_textarea": False},
                {"name": "urun_stt", "label": "Ürün STT", "type": "number", "value": 0,"step": "any", "min": "0","is_textarea": False},
                {"name": "urun_resim", "label": "Ürün Resim", "type": "text", "value": "","is_textarea": False},
                {"name": "urun_min", "label": "Ürün Min", "type": "number", "value": 0,"step": "any", "min": "0","is_textarea": False},
                {"name": "urun_max", "label": "Ürün Max", "type": "number", "value": 0,"step": "any", "min": "0","is_textarea": False},
                {"name": "urun_hedef", "label": "Ürün Hedef", "type": "number", "value": 0,"step": "any", "min": "0","is_textarea": False},
                {"name": "urun_adet_gramaj", "label": "Ürün Adet Gramaj", "type": "number","value": 0 ,"step": "any", "min": "0", "is_textarea": False},
                {"name": "urun_dara", "label": "Ürün Dara", "type": "number", "value": 0,"step": "any", "min": "0","is_textarea": False},
                {"name": "urun_adet", "label": "Ürün Adet", "type": "number", "value": 0,"step": "any", "min": "0","is_textarea": False},
                {"name": "urun_etiket", "label": "Ürün Etiket", "type": "text", "value": "","is_textarea": False},
                {"name": "urun_top_etiket", "label": "Ürün Toplam Etiketi", "type": "text", "value": "","is_textarea": False},
                {"name": "urun_izleme", "label": "Ürün İzleme", "type": "text", "value": "","is_textarea": False},
                {"name": "urun_kodtip", "label": "Ürün Kod Tipi", "type": "text", "value": "","is_textarea": False},
                {"name": "urun_tablo", "label": "Ürün Tablo", "type": "text", "value": "","is_textarea": False},
                {"name": "urun_mesaj1", "label": "Ürün Mesaj1", "type": "text", "value": "","is_textarea": True},
                {"name": "urun_mesaj2", "label": "Ürün Mesaj2", "type": "text", "value": "","is_textarea": True},
                {"name": "urun_mesaj3", "label": "Ürün Mesaj3", "type": "text", "value": "","is_textarea": True},
                {"name": "urun_mesaj4", "label": "Ürün Mesaj4", "type": "text", "value": "","is_textarea": True},
                {"name": "urun_mesaj5", "label": "Ürün Mesaj5", "type": "text", "value": "","is_textarea": True},
                {"name": "urun_mesaj6", "label": "Ürün Mesaj6", "type": "text", "value": "","is_textarea": True},
                {"name": "urun_mesaj7", "label": "Ürün Mesaj7", "type": "text", "value": "","is_textarea": True},
                {"name": "urun_mesaj8", "label": "Ürün Mesaj8", "type": "text", "value":"","is_textarea": True},
                {"name": "urun_mesaj9", "label": "Ürün Mesaj9", "type": "text", "value": "","is_textarea": True},
                {"name": "urun_tanim", "label": "Ürün Tanımı", "type": "text", "value": "","is_textarea": True},
                {"name": "urun_icerik", "label": "Ürün İçeriği", "type": "text", "value": "","is_textarea": True},
                {"name": "urun_aciklama", "label": "Ürün Açıklaması", "type": "text", "value": "","is_textarea": True},
                {"name": "urun_mensei", "label": "Ürün Menşei", "type": "text", "value": "","is_textarea": False}
            ]
    except Product.DoesNotExist:
        messages.error(request, 'Ürün Bulunamadı!', extra_tags="danger")
        return redirect('products:products_list')

    context = {
        "active_icon": "products_categories",
        "product": product,
        "fields": fields,
        "urun_etiket_value": product.urun_etiket if product else "",  # Bu, mevcut etiket değerini şablona gönderecek
        "urun_top_etiket_value": product.urun_top_etiket if product else "",  # Bu, mevcut etiket değerini şablona gönderecek
        "product_status": Product.status.field.choices,
        "categories": Category.objects.filter(status="ACTIVE")
    }
    
    if request.method == 'POST':
        data = request.POST
        try:
            category = Category.objects.get(id=data.get('category'))
        except Category.DoesNotExist:
            messages.error(request, 'Tanımsız Kategori!', extra_tags="danger")
            return redirect('products:products_add')
        
        valid_tips = ["ADET", "AGIRLIK", "SABITFIYAT", "SABITAGIRLIK"]
        urun_tip_value = data.get("urun_tip", "").strip().upper()

        attributes = {
                    "urun_tip": urun_tip_value if urun_tip_value in valid_tips else "AGIRLIK",
                    "status": data.get('state', "TANIMSIZ"),
                    "category": category,
                    **{key: data.get(key, "") for key in [
                        "urun_kod", "urun_ismi1", "urun_ismi2", "urun_grup", "urun_musteri",
                        "urun_qrkod", "urun_resim", "urun_etiket", "urun_top_etiket",
                        "urun_izleme", "urun_kodtip", "urun_tablo", 
                        "urun_mesaj1", "urun_mesaj2", "urun_mesaj3", "urun_mesaj4", "urun_mesaj5", 
                        "urun_mesaj6", "urun_mesaj7", "urun_mesaj8", "urun_mesaj9",
                        "urun_tanim",  "urun_icerik", "urun_aciklama", "urun_mensei"
                    ]},
                    **{key: float(data.get(key, 0)) for key in [
                        "urun_fiyat", "urun_min", "urun_max", "urun_adet_gramaj", "urun_dara"
                    ]},
                    **{key: int(data.get(key, 0)) for key in [
                        "urun_barkod", "urun_stt", "urun_hedef", "urun_adet"
                    ]},
                        "name": data.get('name', "TANIMSIZ"),
                        "description": data.get('description', "TANIMSIZ"),
                        "price": float(data.get('price', 0))
                    }

        if Product.objects.filter(**attributes).exists():
            messages.error(request, 'Ürün Zaten Var!', extra_tags="warning")
            return redirect('products:products_add')

        try:
            Product.objects.create(**attributes)
            messages.success(request, f'Ürün: {attributes["urun_ismi1"]} Başarıyla Oluşturuldu!', extra_tags="success")
            return redirect('products:products_list')
        except Exception as e:
            messages.error(request, 'ürün Oluşturulurken Hata Oluştu!', extra_tags="danger")
            print(e)
            return redirect('products:products_add')

    return render(request, "products/products_add.html", context=context)

@login_required(login_url="/accounts/login/")
def products_update_view(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        messages.error(request, 'Ürün Bulunamadı!', extra_tags="danger")
        return redirect('products:products_list')

    fields = [
        {"name": "urun_kod", "label": "Ürün Kodu", "type": "text", "value": product.urun_kod, "is_textarea": False},
        {"name": "urun_ismi1", "label": "Ürün İsmi 1", "type": "text", "value": product.urun_ismi1,"is_textarea": False},
        {"name": "urun_ismi2", "label": "Ürün İsmi 2", "type": "text", "value": product.urun_ismi2,"is_textarea": False},
        {"name": "urun_grup", "label": "Ürün Grubu", "type": "text", "value": product.urun_grup,"is_textarea": False},
        {"name": "urun_tip", "label": "Ürün Tipi", "type": "select", "value": product.urun_tip,"choices": [("ADET", "Adet"),("AGIRLIK", "Ağırlık"),("SABITFIYAT", "Sabit Fiyat"),("SABITAGIRLIK", "Sabit Ağırlık")]},
        {"name": "urun_fiyat", "label": "Ürün Fiyat ₺", "type": "number", "value": product.urun_fiyat,"step": "0.001","is_textarea": False},
        {"name": "urun_musteri", "label": "Ürün Müşteri", "type": "text", "value": product.urun_musteri,"is_textarea": False},
        {"name": "urun_barkod", "label": "Ürün Barkod", "type": "number", "value": product.urun_barkod,"step": "1","is_textarea": False},
        {"name": "urun_qrkod", "label": "Ürün QRkod", "type": "text", "value": product.urun_qrkod,"is_textarea": False},
        {"name": "urun_stt", "label": "Ürün STT", "type": "number", "value": product.urun_stt,"step": "1","is_textarea": False},
        {"name": "urun_resim", "label": "Ürün Resim", "type": "text", "value": product.urun_resim,"is_textarea": False},
        {"name": "urun_min", "label": "Ürün Min", "type": "number", "value": product.urun_min,"step": "0.001","is_textarea": False},
        {"name": "urun_max", "label": "Ürün Max", "type": "number", "value": product.urun_max,"step": "0.001","is_textarea": False},
        {"name": "urun_hedef", "label": "Ürün Hedef", "type": "number", "value": product.urun_hedef,"step": "1","is_textarea": False},
        {"name": "urun_adet_gramaj", "label": "Ürün Adet Gramaj", "type": "number", "value": product.urun_adet_gramaj,"step": "0.0001","is_textarea": False},
        {"name": "urun_dara", "label": "Ürün Dara", "type": "number", "value": product.urun_dara,"step": "0.001","is_textarea": False},
        {"name": "urun_adet", "label": "Ürün Adet", "type": "number", "value": product.urun_adet,"step": "1","is_textarea": False},
        {"name": "urun_etiket", "label": "Ürün Etiket", "type": "text", "value": product.urun_etiket,"is_textarea": False},
        {"name": "urun_top_etiket", "label": "Ürün Toplam Etiketi", "type": "text", "value": product.urun_top_etiket,"is_textarea": False},
        {"name": "urun_izleme", "label": "Ürün İzleme", "type": "text", "value": product.urun_izleme,"is_textarea": False},
        {"name": "urun_kodtip", "label": "Ürün Kod Tipi", "type": "text", "value": product.urun_kodtip,"is_textarea": False},
        {"name": "urun_tablo", "label": "Ürün Tablo", "type": "text", "value": product.urun_tablo,"is_textarea": False},
        {"name": "urun_mesaj1", "label": "Ürün Mesaj1", "type": "text", "value": product.urun_mesaj1,"is_textarea": True},
        {"name": "urun_mesaj2", "label": "Ürün Mesaj2", "type": "text", "value": product.urun_mesaj2,"is_textarea": True},
        {"name": "urun_mesaj3", "label": "Ürün Mesaj3", "type": "text", "value": product.urun_mesaj3,"is_textarea": True},
        {"name": "urun_mesaj4", "label": "Ürün Mesaj4", "type": "text", "value": product.urun_mesaj4,"is_textarea": True},
        {"name": "urun_mesaj5", "label": "Ürün Mesaj5", "type": "text", "value": product.urun_mesaj5,"is_textarea": True},
        {"name": "urun_mesaj6", "label": "Ürün Mesaj6", "type": "text", "value": product.urun_mesaj6,"is_textarea": True},
        {"name": "urun_mesaj7", "label": "Ürün Mesaj7", "type": "text", "value": product.urun_mesaj7,"is_textarea": True},
        {"name": "urun_mesaj8", "label": "Ürün Mesaj8", "type": "text", "value": product.urun_mesaj8,"is_textarea": True},
        {"name": "urun_mesaj9", "label": "Ürün Mesaj9", "type": "text", "value": product.urun_mesaj9,"is_textarea": True},
        {"name": "urun_tanim", "label": "Ürün Tanımı", "type": "text", "value": product.urun_tanim,"is_textarea": True},
        {"name": "urun_icerik", "label": "Ürün İçeriği", "type": "text", "value": product.urun_icerik,"is_textarea": True},
        {"name": "urun_aciklama", "label": "Ürün Açıklaması", "type": "text", "value": product.urun_aciklama,"is_textarea": True},
        {"name": "urun_mensei", "label": "Ürün Menşei", "type": "text", "value": product.urun_mensei,"is_textarea": False}
    ]

    prn_folder = os.path.join(settings.BASE_DIR, 'static', 'printer')
    eyz_prn_files = [file for file in os.listdir(prn_folder) if file.startswith("eyz#") and file.endswith(".prn")]
    top_prn_files = [file for file in os.listdir(prn_folder) if file.startswith("topeyz#") and file.endswith(".prn")]

    context = {
        "active_icon": "products",
        "product": product,
        "fields": fields,
        "urun_etiket_value": product.urun_etiket,  # Mevcut değer
        "urun_top_etiket_value": product.urun_top_etiket,  # Mevcut değer
        "eyz_prn_files": eyz_prn_files,  # PRN dosyaları
        "top_prn_files": top_prn_files,  # PRN dosyaları
        "product_status": Product.status.field.choices,
        "categories": Category.objects.filter(status="ACTIVE"),
    }

    if request.method == 'POST':
        data = request.POST
        try:
            category = Category.objects.get(id=data.get('category'))
        except Category.DoesNotExist:
            messages.error(request, 'Tanımsız Kategori!', extra_tags="danger")
            return redirect('products:products_update', product_id=product_id)
            
        valid_tips = ["ADET", "AGIRLIK", "SABITFIYAT", "SABITAGIRLIK"]
        urun_tip_value = data.get("urun_tip", "").strip().upper()


        attributes = {
            "urun_tip": urun_tip_value if urun_tip_value in valid_tips else "AGIRLIK",
            "status": data.get('state', "TANIMSIZ"),
            "category": category,
            **{key: data.get(key, "") for key in [
                "urun_kod", "urun_ismi1", "urun_ismi2", "urun_grup", "urun_musteri",
                "urun_barkod", "urun_qrkod", "urun_resim", "urun_etiket", "urun_top_etiket",
                "urun_izleme", "urun_kodtip", "urun_tablo", 
                "urun_mesaj1", "urun_mesaj2", "urun_mesaj3", "urun_mesaj4", "urun_mesaj5", "urun_mesaj6", "urun_mesaj7", "urun_mesaj8", "urun_mesaj9",
                "urun_tanim",  "urun_icerik", "urun_aciklama", "urun_mensei"
            ]},
            **{key: data.get(key, 0) for key in [
                "urun_fiyat", "urun_stt", "urun_min", "urun_max", "urun_hedef", "urun_adet_gramaj", "urun_dara", "urun_adet"
            ]},
            "name": data.get('name', "TANIMSIZ"),
            "description": data.get('description', "TANIMSIZ"),
            "price": float(data.get('price', 0))
        }

        if Product.objects.filter(**attributes).exclude(id=product_id).exists():
            messages.error(request, 'Bu Ürün Benzeri Zaten Var!', extra_tags="warning")
            return redirect('products:products_update', product_id=product_id)

        try:
            Product.objects.filter(id=product_id).update(**attributes)
            messages.success(request, f'Ürün: {product.urun_ismi1} Başarıyla Güncellendi!', extra_tags="success")
            return redirect('products:products_list')
        except Exception as e:
            messages.error(request, 'Ürün Güncellenirken Hata Oluştu!', extra_tags="danger")
            print(e)
            return redirect('products:products_update', product_id=product_id)

    return render(request, "products/products_update.html", context=context)

@login_required(login_url="/accounts/login/")
def products_delete_view(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        product.delete()
        messages.success(request, f'Ürün: {product.urun_ismi1} Silindi!', extra_tags="success")
        return redirect('products:products_list')
    except Product.DoesNotExist:
        messages.error(request, 'Ürün Bulunamadı!', extra_tags="danger")
        return redirect('products:products_list')
    except Exception as e:
        messages.error(request, 'Ürün Silinirken Hata Oluştu!', extra_tags="danger")
        print(e)
        return redirect('products:products_list')

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

@login_required(login_url="/accounts/login/")
def get_products_ajax_view(request):
    if request.method == 'POST' and is_ajax(request=request):
        data = []
        term = request.POST.get('term', '')
        products = Product.objects.filter(name__icontains=term)
        for product in products[:10]:
            data.append(product.to_json())
        return JsonResponse(data, safe=False)

@login_required(login_url="/accounts/login/")
def get_products(request):
    term = request.POST.get('term', '').strip()
    all_products = request.POST.get('all', 'false') == 'true'

    if all_products:
        products = Product.objects.all()
    else:
        products = Product.objects.filter(urun_ismi1__icontains=term)

    results = [
        {
            "id": product.id,
            "urun_ismi1": product.urun_ismi1,
            "urun_kod": product.urun_kod,
            "urun_tip": product.urun_tip,
            "urun_adet_gramaj": product.urun_adet_gramaj,
            #"category": product.category.name,
            "urun_barkod": product.urun_barkod,
            "urun_min": product.urun_min,   
            "urun_max": product.urun_max,
            "urun_etiket": product.urun_etiket,
            "urun_top_etiket": product.urun_top_etiket,                
            #"urun_barkod": product.urun_barkod if product.urun_barkod else "Barkod Yok"
        }
        for product in products
    ]
    return JsonResponse(results, safe=False)

@login_required(login_url="/accounts/login/")
def get_eyz_prn_files(request):
    # PRN dosyalarının bulunduğu klasör
    prn_folder = os.path.join(settings.BASE_DIR, 'static', 'printer')

    # Klasördeki .prn dosyalarını listele
    try:
        eyz_prn_files = [f for f in os.listdir(prn_folder) if f.startswith("eyz#") and f.endswith('.prn')]
        return JsonResponse({'success': True, 'files': eyz_prn_files})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})
    
@login_required(login_url="/accounts/login/")
def get_top_prn_files(request):
    # PRN dosyalarının bulunduğu klasör
    prn_folder = os.path.join(settings.BASE_DIR, 'static', 'printer')

    # Klasördeki .prn dosyalarını listele
    try:
        top_prn_files = [f for f in os.listdir(prn_folder) if f.startswith("topeyz#") and f.endswith('.prn')]
        return JsonResponse({'success': True, 'files': top_prn_files})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})