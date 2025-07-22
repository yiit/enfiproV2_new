import os
from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django_pos.wsgi import *
from django_pos import settings
from django.template.loader import get_template
from customers.models import Customer
from products.models import Product
#from weasyprint import HTML, CSS
from .models import Sale, SaleDetail, PrintLog

#import chardet


import subprocess
from django.http import JsonResponse
import json

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def update_adet_gramaj(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Geçersiz istek'})

    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        adet_gramaj = data.get('adet_gramaj')

        if not product_id or adet_gramaj is None:
            return JsonResponse({'success': False, 'error': 'Eksik veri'})

        product = Product.objects.get(id=product_id)
        product.urun_adet_gramaj = adet_gramaj
        product.save()

        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    
@csrf_exempt
def get_product(request):
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        product = Product.objects.get(id=product_id)

        return JsonResponse({
            'id': product.id,
            'urun_ismi1': product.urun_ismi1,
            'urun_kod': product.urun_kod,
            'urun_barkod': product.urun_barkod,
            'urun_tip': product.urun_tip,
            'urun_adet_gramaj': product.urun_adet_gramaj,
            'urun_min': product.urun_min,
            'urun_max': product.urun_max,
            'urun_hedef': product.urun_hedef,
            'urun_adet': product.urun_adet,
            'urun_etiket': product.urun_etiket,
            'urun_top_etiket': product.urun_top_etiket,
            'urun_mesaj1': product.urun_mesaj1,
            'urun_mesaj2': product.urun_mesaj2,
            'urun_mesaj3': product.urun_mesaj3,
            'urun_mesaj4': product.urun_mesaj4,
            'urun_mesaj5': product.urun_mesaj5,
            'urun_mesaj6': product.urun_mesaj6,
            'urun_mesaj7': product.urun_mesaj7,
            'urun_mesaj8': product.urun_mesaj8,
            'urun_mesaj9': product.urun_mesaj9,
            'urun_icerik': product.urun_icerik,
            'urun_stt': product.urun_stt,
            'urun_resim': product.urun_resim.url if product.urun_resim else ''
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})



def get_all_products(request):
    if request.method == 'POST':
        products = Product.objects.select_related('category').all()
        product_list = [
            {
                'id': product.id,
                'urun_ismi1': product.urun_ismi1,
                'urun_kod': product.urun_kod,
                'urun_barkod': product.urun_barkod,
                'urun_tip': product.urun_tip,
                'urun_adet_gramaj': product.urun_adet_gramaj,
                'urun_min': product.urun_min,
                'urun_max': product.urun_max,
                'urun_hedef': product.urun_hedef,
                'urun_adet': product.urun_adet,
                'urun_etiket': product.urun_etiket,
                'urun_top_etiket': product.urun_top_etiket,
                'urun_mesaj1': product.urun_mesaj1,
                'urun_mesaj2': product.urun_mesaj2,
                'urun_mesaj3': product.urun_mesaj3,
                'urun_mesaj4': product.urun_mesaj4,
                'urun_mesaj5': product.urun_mesaj5,
                'urun_mesaj6': product.urun_mesaj6,
                'urun_mesaj7': product.urun_mesaj7,
                'urun_mesaj8': product.urun_mesaj8,
                'urun_mesaj9': product.urun_mesaj9,
                'urun_icerik': product.urun_icerik,
                'urun_stt': product.urun_stt,
                'urun_resim': str(product.urun_resim) if product.urun_resim else None,
                'urun_kategori': product.category.name if product.category else 'Genel'
            }
            for product in products
        ]
        
        # JSON çıktısını kontrol etmek için log ekleyelim
        print("Ürün Listesi:", product_list)  # Terminal veya loglarda kontrol et
        
        return JsonResponse(product_list, safe=False)
    
    return JsonResponse({'error': 'Geçersiz istek.'}, status=400)



def get_products_by_customer(request):
    if request.method == 'POST':
        customer_id = request.POST.get('customer_id')
        if not customer_id:
            return JsonResponse({'error': 'Müşteri ID gönderilmedi.'}, status=400)
        
        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            return JsonResponse({'error': 'Müşteri bulunamadı.'}, status=404)

        # Müşteri kategorisine göre ürünleri filtrele
        products = Product.objects.filter(category=customer.category)
        product_list = [
            {
                'id': product.id,
                'urun_ismi1': product.urun_ismi1,
                'urun_kod': product.urun_kod,
                'urun_barkod': product.urun_barkod,
                'urun_tip': product.urun_tip,
                'urun_adet_gramaj': product.urun_adet_gramaj,
                'urun_min': product.urun_min,
                'urun_max': product.urun_max,
                'urun_hedef': product.urun_hedef,
                'urun_adet': product.urun_adet,
                'urun_etiket': product.urun_etiket,
                'urun_top_etiket': product.urun_top_etiket,
                'urun_mesaj1': product.urun_mesaj1,
                'urun_mesaj2': product.urun_mesaj2,
                'urun_mesaj3': product.urun_mesaj3,
                'urun_mesaj4': product.urun_mesaj4,
                'urun_mesaj5': product.urun_mesaj5,
                'urun_mesaj6': product.urun_mesaj6,
                'urun_mesaj7': product.urun_mesaj7,
                'urun_mesaj8': product.urun_mesaj8,
                'urun_mesaj9': product.urun_mesaj9,
                'urun_icerik': product.urun_icerik,
                'urun_stt': product.urun_stt,
                'urun_resim': product.urun_resim,
            }
            for product in products
        ]
        return JsonResponse(product_list, safe=False)
    return JsonResponse({'error': 'Geçersiz istek.'}, status=400)

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


@login_required(login_url="/accounts/login/")
def sales_list_view(request):
    context = {
        "active_icon": "sales",
        "sales": Sale.objects.all()
    }
    return render(request, "sales/sales.html", context=context)


@login_required(login_url="/accounts/login/")
def sales_add_view(request):
    context = {
        "active_icon": "sales",
        "customers": [c.to_select2() for c in Customer.objects.all()],
        'NODE_SERVER_IP': getattr(settings, "NODE_SERVER_IP", "127.0.0.1")  # Varsayılan değeri belirle
    }

    if request.method == 'POST':
        if is_ajax(request=request):
            # Save the POST arguments
            data = json.load(request)

            sale_attributes = {
                "customer": Customer.objects.get(id=int(data['customer'])),
                "sub_total": float(data["sub_total"]),
                "grand_total": float(data["grand_total"]),
                "tax_amount": float(data["tax_amount"]),
                "tax_percentage": float(data["tax_percentage"]),
                "amount_payed": float(data["amount_payed"]),
                "amount_change": float(data["amount_change"]),
            }
            try:
                # Create the sale
                new_sale = Sale.objects.create(**sale_attributes)
                new_sale.save()
                # Create the sale details
                products = data["products"]

                for product in products:
                    detail_attributes = {
                        "sale": Sale.objects.get(id=new_sale.id),
                        "product": Product.objects.get(id=int(product["id"])),
                        "price": product["price"],
                        "quantity": product["quantity"],
                        "total_detail": product["total_product"]
                    }
                    sale_detail_new = SaleDetail.objects.create(
                        **detail_attributes)
                    sale_detail_new.save()

                print("Sale saved")

                messages.success(
                    request, 'Sale created successfully!', extra_tags="success")

            except Exception as e:
                messages.success(
                    request, 'There was an error during the creation!', extra_tags="danger")

        return redirect('sales:sales_list')

    return render(request, "sales/sales_add.html", context=context)


@login_required(login_url="/accounts/login/")
def sales_details_view(request, sale_id):
    """
    Args:
        request:
        sale_id: ID of the sale to view
    """
    try:
        # Get the sale
        sale = Sale.objects.get(id=sale_id)

        # Get the sale details
        details = SaleDetail.objects.filter(sale=sale)

        context = {
            "active_icon": "sales",
            "sale": sale,
            "details": details,
        }
        return render(request, "sales/sales_details.html", context=context)
    except Exception as e:
        messages.success(
            request, 'There was an error getting the sale!', extra_tags="danger")
        print(e)
        return redirect('sales:sales_list')


@login_required(login_url="/accounts/login/")
def receipt_pdf_view(request, sale_id):
    """
    Args:
        request:
        sale_id: ID of the sale to view the receipt
    """
    # Get the sale
    sale = Sale.objects.get(id=sale_id)

    # Get the sale details
    details = SaleDetail.objects.filter(sale=sale)

    template = get_template("sales/sales_receipt_pdf.html")
    context = {
        "sale": sale,
        "details": details
    }
    html_template = template.render(context)

    # CSS Boostrap
    css_url = os.path.join(
        settings.BASE_DIR, 'static/css/receipt_pdf/bootstrap.min.css')

    # Create the pdf
    pdf = HTML(string=html_template).write_pdf(stylesheets=[CSS(css_url)])

    return HttpResponse(pdf, content_type="application/pdf")

"""def print_file(request):
    if request.method == 'POST':
        # Dosya yolunu oluştur
        file_path = os.path.join(settings.BASE_DIR, 'static', 'printer', 'eyz.prn')
        if not os.path.exists(file_path):
            return JsonResponse({'success': False, 'message': 'File not found.'}, status=404)

        try:
            # Yazdırma komutunu çalıştır
            subprocess.run(['lp', file_path], check=True)
            return JsonResponse({'success': True, 'message': 'File sent to the printer successfully.'})
        except subprocess.CalledProcessError as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    else:
        return
"""

import os
import time
import json
import usb.core
import usb.util
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import PrintLog  # Yazdırılan etiketleri kaydetmek için model
from django.views.decorators.csrf import csrf_exempt

# Yazıcı Vendor ve Product ID
# RONGTA RP806

VENDOR_ID = 0x0fe6
PRODUCT_ID = 0x8800
OUT_ENDPOINT = 0x01  # Yazıcıya veri göndermek için kullanılan endpoint
STATUS_ENDPOINT = 0x82  # Yazıcı durumu için kullanılan endpoint
MAX_RETRIES = 5
RETRY_DELAY = 2  # Denemeler arası bekleme süresi

"""
# XPRINTER
VENDOR_ID = 0x2d84
PRODUCT_ID = 0x4e7b
OUT_ENDPOINT = 0x01     # Yazıcıya veri göndermek için kullanılan endpoint
STATUS_ENDPOINT = 0x82  # Yazıcı durumu için kullanılan endpoint
MAX_RETRIES = 5
RETRY_DELAY = 2  # Denemeler arası bekleme süresi
"""

import re
import os
import json
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import subprocess
from django.conf import settings


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from customers.models import Customer

@csrf_exempt
def get_customer_info(request):
    if request.method == 'POST':
        customer_id = request.POST.get('customer_id')
        if not customer_id:
            return JsonResponse({'success': False, 'message': 'Müşteri ID eksik.'}, status=400)

        try:
            # Müşteri bilgilerini getir
            customer = Customer.objects.get(id=customer_id)
            customer_data = {
                'first_name': customer.first_name,
                'last_name': customer.last_name,
                'address': customer.address,
            }
            return JsonResponse({'success': True, 'data': customer_data})
        except Customer.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Müşteri bulunamadı.'}, status=404)
    return JsonResponse({'success': False, 'message': 'Geçersiz istek yöntemi.'}, status=400)

def calculate_new_x(original_x, font_width, text_length):
    """
    Calculates the new X position to center the text based on its length using the provided formula.
    Formula: (original_x / 2) + (font_width / 2 * (text_length / 2))
    """
    new_x = int((original_x / 2) + ((font_width / 2) * (text_length / 2)))
    return new_x


def split_text_into_lines(text, max_chars_per_line):
    """
    Splits the text into multiple lines based on the maximum number of characters per line,
    ensuring no word is split across lines.
    """
    words = text.split()  # Metni kelimelere ayır
    lines = []
    current_line = ""

    for word in words:
        # Eğer kelime mevcut satıra sığmazsa, yeni bir satır başlat
        if len(current_line) + len(word) + 1 > max_chars_per_line:
            lines.append(current_line.strip())
            current_line = word  # Yeni satırı başlat
        else:
            current_line += f" {word}"  # Kelimeyi mevcut satıra ekle

    # Son satırı ekle
    if current_line:
        lines.append(current_line.strip())

    return lines


def calculate_new_x_centered(original_x, font_width, text_length):
    """
    Metni ortalamak için X konumunu hesaplar.
    Uzun metinlerde karakter başına katkı azalır.
    """
    # Temel katkı
    base_adjust = 15.0

    # Karakter başına katkıyı azalt
    if text_length > 5:
        base_adjust -= (text_length - 5) * 0.48  # her fazla karakterde 0.1 azalt
        base_adjust = max(base_adjust, 4.0)     # minimum katkı sınırı

    shift = (font_width + base_adjust) * (text_length / 2)
    return int((original_x / 2) + shift)

@csrf_exempt
def print_file(request):
    """
    Tek bir endpoint:
      - 'printSource': 'auto' -> Seri port (RS232) üzerinden yazdırma (otomatik)
      - 'printSource': 'manual' -> USB yazıcı üzerinden yazdırma
    """
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=400)

    try:
        data = json.loads(request.body)

        # Hangi kaynaktan geldiğini ayırt eden parametre
        print_source = data.get('printSource', 'auto')  # default auto

        # Placeholder sözlüğü
        placeholders = {
            "%net%": data.get('weight', '').strip(),
            "%partino%": data.get('customText', '').strip(),
            "%musteri_ismi1%": data.get('customerName', '').encode('UTF-8').decode('ISO-8859-9', errors='ignore'),
            "%musteri_ismi2%": data.get('customerName2', ''),
            "%urun_ismi1%": data.get('productName', '').encode('UTF-8').decode('ISO-8859-9', errors='ignore'),
            "%urun_kodu%": data.get('productCode', ''),
            "%urun_barkod%": data.get('productBarkod', ''),
            "%sno%": data.get('serialNumber', ''),
            "%musteri_adresi%": data.get('customerAddress', ''),
            "%stt%": (datetime.now() + timedelta(days=int(data.get('productstt', 0)))).strftime('%d-%m-%Y'),
            "%tarih%": datetime.now().strftime('%d-%m-%Y'),
            "%urt%": data.get('dateText', '').strip(),
            "%saat%": datetime.now().strftime('%H:%M'),
            "%paketsayisi%": data.get('paketSayisi', '').strip(),
            "%topnet%": data.get('topnet', '').strip(),
            "%pakettopnet%": data.get('pakettopnet', '').strip(),
            "%msg1%": data.get('productMesaj1', '').encode('UTF-8').decode('ISO-8859-9', errors='ignore'),
            "%msg2%": data.get('productMesaj2', '').encode('UTF-8').decode('ISO-8859-9', errors='ignore'),
            "%msg3%": data.get('productMesaj3', '').encode('UTF-8').decode('ISO-8859-9', errors='ignore'),
            "%msg4%": data.get('productMesaj4', '').encode('UTF-8').decode('ISO-8859-9', errors='ignore'),
            "%msg5%": data.get('productMesaj5', '').encode('UTF-8').decode('ISO-8859-9', errors='ignore'),
            "%msg6%": data.get('productMesaj6', '').encode('UTF-8').decode('ISO-8859-9', errors='ignore'),
            "%msg7%": data.get('productMesaj7', '').encode('UTF-8').decode('ISO-8859-9', errors='ignore'),
            "%msg8%": data.get('productMesaj8', '').encode('UTF-8').decode('ISO-8859-9', errors='ignore'),
            "%msg9%": data.get('productMesaj9', '').encode('UTF-8').decode('ISO-8859-9', errors='ignore'),
            "%icerik%": data.get('producticerik', ''),
            "%operator%": data.get('operator', ''),
            "%EAN13barkod%": data.get('productBarkod', ''),
            "%topadet%": data.get('topAdet', '').strip(),
            "%adet_gramaj%": data.get('adetGramaj', ''),
            "%adet_hesap%": data.get('adetHesap', ''),
            "%adet_hesap_barkod%": data.get('adetHesapBarkod', ''),
        }
        
        if print_source == 'manual':
            input_tspl_topeyz_path = os.path.join(settings.BASE_DIR, 'static', 'printer', str(data.get('topetiketText', 'eyz.prn')))
            output_tspl_topeyz_path = os.path.join(settings.BASE_DIR, 'static', 'printer', 'yaz_topeyz.lbl')
            if not os.path.exists(input_tspl_topeyz_path):
                return JsonResponse({'success': False, 'message': 'Template file not found.'}, status=404)

            with open(input_tspl_topeyz_path, 'r', encoding='ISO-8859-9') as file:
               original_lines = file.readlines()

            updated_lines = []

            # TEXT satırları işleme
            for line in original_lines:
                stripped_line = line.rstrip('\r\n')
                # 🔁 FONT adını değiştir
                stripped_line = stripped_line.replace("ENDUTEK.TTF", "0")

                if stripped_line.startswith("TEXT"):
                    match = re.match(r'TEXT\s+(\d+),\s*(\d+),\s*"([^"]+)",\s*(\d+),\s*(\d+),\s*(\d+),\s*"(.*)"', stripped_line)
                    if match:
                        original_x, y, font, rotation, font_width, font_height, text_data = match.groups()
                        original_x = int(original_x)
                        y = int(y)
                        font_width = int(font_width)
                        font_height = int(font_height)

                        # Placeholderları değiştir
                        for ph, val in placeholders.items():
                            if ph in text_data:
                                text_data = text_data.replace(ph, val)

                        # %ORTA% varsa ortalayacağız
                        is_centered = "%ORTA%" in text_data
                        text_data = text_data.replace("%ORTA%", "").strip()

                        total_len = len(text_data)
                        max_chars = int(original_x / ((font_width * 1.1) or 1))

                        if is_centered and total_len <= max_chars:
                            new_x = calculate_new_x_centered(original_x, font_width, total_len)
                            new_line = f'TEXT {new_x},{y},"{font}",{rotation},{font_width},{font_height},"{text_data}"'
                            updated_lines.append(new_line)
                        else:
                            # Çok satırlı bölme
                            splitted = split_text_into_lines(text_data, max_chars)
                            for i, splitted_line in enumerate(splitted):
                                if i > 0:
                                    y -= (font_height * 2) + 6
                                new_line = f'TEXT {original_x},{y},"{font}",{rotation},{font_width},{font_height},"{splitted_line}"'
                                updated_lines.append(new_line)
                    else:
                        updated_lines.append(stripped_line)
                else:
                    # Diğer satırlarda placeholder değiştir
                    for ph, val in placeholders.items():
                        if ph in stripped_line:
                            stripped_line = stripped_line.replace(ph, val)
                    updated_lines.append(stripped_line)

            # Güncellenmiş TSPL dosyasını kaydet
            with open(output_tspl_topeyz_path, 'w', encoding='ISO-8859-9') as out_file:
                out_file.write("\n".join(updated_lines))
                out_file.write("\r\n")

            # Print log kaydet
            save_print_log(request, placeholders, output_tspl_topeyz_path)
        
            success_usb = send_data_to_usb_printer(output_tspl_topeyz_path)
            if not success_usb:
                return JsonResponse({'success': False, 'message': 'Could not print via USB (manual).'}, status=500)
            return JsonResponse({'success': True, 'message': 'File sent to USB (manual) successfully.'})

        elif print_source == 'auto':
            input_tspl_eyz_path = os.path.join(settings.BASE_DIR, 'static', 'printer', str(data.get('etiketText', 'eyz.prn')))
            output_tspl_eyz_path = os.path.join(settings.BASE_DIR, 'static', 'printer', 'yaz_eyz.lbl')
            if not os.path.exists(input_tspl_eyz_path):
                return JsonResponse({'success': False, 'message': 'Template file not found.'}, status=404)

            with open(input_tspl_eyz_path, 'r', encoding='ISO-8859-9') as file:
               original_lines = file.readlines()

            updated_lines = []

            # TEXT satırları işleme
            for line in original_lines:
                stripped_line = line.rstrip('\r\n')

                if stripped_line.startswith("TEXT"):
                    match = re.match(r'TEXT\s+(\d+),\s*(\d+),\s*"([^"]+)",\s*(\d+),\s*(\d+),\s*(\d+),\s*"(.*)"', stripped_line)
                    if match:
                        original_x, y, font, rotation, font_width, font_height, text_data = match.groups()
                        original_x = int(original_x)
                        y = int(y)
                        font_width = int(font_width)
                        font_height = int(font_height)

                        # Placeholderları değiştir
                        for ph, val in placeholders.items():
                            if ph in text_data:
                                text_data = text_data.replace(ph, val)

                        # %ORTA% varsa ortalayacağız
                        is_centered = "%ORTA%" in text_data
                        text_data = text_data.replace("%ORTA%", "").strip()

                        total_len = len(text_data)
                        max_chars = int(original_x / (font_width or 1))

                        if is_centered and total_len <= max_chars:
                            new_x = calculate_new_x_centered(original_x, font_width, total_len)
                            new_line = f'TEXT {new_x},{y},"{font}",{rotation},{font_width},{font_height},"{text_data}"'
                            updated_lines.append(new_line)
                        else:
                            # Çok satırlı bölme
                            splitted = split_text_into_lines(text_data, max_chars)
                            for i, splitted_line in enumerate(splitted):
                                if i > 0:
                                    y -= (font_height * 2) + 6
                                new_line = f'TEXT {original_x},{y},"{font}",{rotation},{font_width},{font_height},"{splitted_line}"'
                                updated_lines.append(new_line)
                    else:
                        updated_lines.append(stripped_line)
                else:
                    # Diğer satırlarda placeholder değiştir
                    for ph, val in placeholders.items():
                        if ph in stripped_line:
                            stripped_line = stripped_line.replace(ph, val)
                    updated_lines.append(stripped_line)

            # Güncellenmiş TSPL dosyasını kaydet
            with open(output_tspl_eyz_path, 'w', encoding='ISO-8859-9') as out_file:
                out_file.write("\n".join(updated_lines))
                out_file.write("\r\n")

            # Otomatik -> Seri port
            success_serial = send_data_to_serial_printer(output_tspl_eyz_path)
            if not success_serial:
                return JsonResponse({'success': False, 'message': 'Could not print via Serial Port (auto).'}, status=500)
            return JsonResponse({'success': True, 'message': 'File sent via RS232 (auto) successfully.'})
            
        elif print_source == 'copy-product':
            # Otomatik -> Seri port
            output_tspl_eyz_path = os.path.join(settings.BASE_DIR, 'static', 'printer', 'yaz_eyz.lbl')
            success_serial = send_data_to_serial_printer(output_tspl_eyz_path)
            if not success_serial:
                return JsonResponse({'success': False, 'message': 'Could not print via Serial Port (auto).'}, status=500)
            return JsonResponse({'success': True, 'message': 'File sent via RS232 (auto) successfully.'})
        
        elif print_source == 'copy-total':
            output_tspl_topeyz_path = os.path.join(settings.BASE_DIR, 'static', 'printer', 'yaz_topeyz.lbl')
            success_usb = send_data_to_usb_printer(output_tspl_topeyz_path)
            if not success_usb:
                return JsonResponse({'success': False, 'message': 'Could not print via USB (manual).'}, status=500)
            return JsonResponse({'success': True, 'message': 'File sent to USB (manual) successfully.'})

        else:
            # Tanımsız source
            return JsonResponse({'success': False, 'message': f'Unknown printSource: {print_source}'}, status=400)

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid JSON format.'}, status=400)
    except Exception as e:
        import traceback
        error_message = traceback.format_exc()
        print(error_message)
        return JsonResponse({'success': False, 'message': f'Unexpected error: {str(e)}'}, status=500)

"""
@csrf_exempt
def print_file(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            placeholders = {
                "%net%": data.get('weight', '').strip(),
                "%partino%": data.get('customText', '').strip(),
                "%musteri_ismi1%": data.get('customerName', '').encode('UTF-8').decode('ISO-8859-9', errors='ignore'),
                "%musteri_ismi2%": data.get('customerName2', '').encode('UTF-8').decode('ISO-8859-9', errors='ignore'),
                "%urun_ismi1%": data.get('productName', '').encode('UTF-8').decode('ISO-8859-9', errors='ignore'),
                "%urun_kodu%": data.get('productCode', ''),
                "%urun_barkod%": data.get('productBarkod', ''),
                "%sno%": data.get('serialNumber', ''),
                "%musteri_adresi%": data.get('customerAddress', '').replace('\n', '\n').encode('UTF-8').decode('ISO-8859-9', errors='ignore'),
                #"%date%": datetime.now().strftime('%d-%m-%Y'),
                "%stt%": (datetime.now() + timedelta(days=int(data.get('productstt')))).strftime('%d-%m-%Y'),
                "%tarih%": datetime.now().strftime('%d-%m-%Y'),
                #"%date%": data.get('dateText', '').strip(),
                "%urt%": data.get('dateText', '').strip(),
                "%saat%": datetime.now().strftime('%H:%M'),
                "%paketsayisi%": data.get('paketSayisi', '').strip(),
                "%msg1%": data.get('productMesaj1', '').encode('UTF-8').decode('ISO-8859-9', errors='ignore'),
                "%msg2%": data.get('productMesaj2', '').encode('UTF-8').decode('ISO-8859-9', errors='ignore'),
                "%msg3%": data.get('productMesaj3', '').encode('UTF-8').decode('ISO-8859-9', errors='ignore'),
                "%msg4%": data.get('productMesaj4', '').encode('UTF-8').decode('ISO-8859-9', errors='ignore'),
                "%msg5%": data.get('productMesaj5', '').encode('UTF-8').decode('ISO-8859-9', errors='ignore'),
                "%msg6%": data.get('productMesaj6', '').encode('UTF-8').decode('ISO-8859-9', errors='ignore'),
                "%msg7%": data.get('productMesaj7', '').encode('UTF-8').decode('ISO-8859-9', errors='ignore'),
                "%msg8%": data.get('productMesaj8', '').encode('UTF-8').decode('ISO-8859-9', errors='ignore'),
                "%msg9%": data.get('productMesaj9', '').encode('UTF-8').decode('ISO-8859-9', errors='ignore'),
                "%icerik%": data.get('producticerik', '').encode('UTF-8').decode('ISO-8859-9', errors='ignore')
            }

            input_tspl_path = os.path.join(settings.BASE_DIR, 'static', 'printer', str(data.get('etiketText')))
            output_tspl_path = os.path.join(settings.BASE_DIR, 'static', 'printer', 'yaz_eyz.lbl')
            print(input_tspl_path)
            if not os.path.exists(input_tspl_path):
                return JsonResponse({'success': False, 'message': 'Template file not found.'}, status=404)

            with open(input_tspl_path, 'r', encoding='ISO-8859-9') as file:
                content = file.readlines()

            updated_lines = []

            for line in content:
                original_line = line.strip()

                if original_line.startswith("TEXT"):
                    match = re.match(r'TEXT\s+(\d+),\s*(\d+),\s*"([^"]*)",\s*(\d+),\s*(\d+),\s*(\d+),\s*"([^"]*)"', original_line)
                    if match:
                        original_x, y, font, rotation, font_width, font_height, data = match.groups()
                        original_x, y, font_width, font_height = map(int, [original_x, y, font_width, font_height])

                        # Placeholder'ları değiştir
                        for placeholder, value in placeholders.items():
                            if placeholder in data:
                                data = data.replace(placeholder, value)

                        # `%ORTA%` kontrolü
                        is_centered = "%ORTA%" in data
                        data = data.replace("%ORTA%", "").strip()

                        # Harf uzunluğu ve satır kontrolü
                        total_length = len(data)
                        #max_chars_per_line = int(original_x / (font_width * 1.22))
                        max_chars_per_line = int(original_x / (font_width * 1))

                        if total_length <= max_chars_per_line and is_centered:
                            # `%ORTA%` varsa ve tek satıra sığıyorsa ortala
                            text_length = total_length
                            new_x = calculate_new_x_centered(original_x, font_width, text_length)
                            updated_line = f'TEXT {new_x},{y},"{font}",{rotation},{font_width},{font_height},"{data}"'
                            updated_lines.append(updated_line)
                        else:
                            # Çok satırlıysa veya `%ORTA%` yoksa, orijinal X değerini kullan
                            lines = split_text_into_lines(data, max_chars_per_line)
                            for i, line_text in enumerate(lines):
                                new_x = original_x
                                if i > 0:
                                    y -= (font_height*2) + 6

                                updated_line = f'TEXT {new_x},{y},"{font}",{rotation},{font_width},{font_height},"{line_text}"'
                                updated_lines.append(updated_line)
                        continue
                else:
                    for placeholder, value in placeholders.items():
                        if placeholder in original_line:
                            original_line = original_line.replace(placeholder, value)
                            
                updated_lines.append(original_line)

            with open(output_tspl_path, 'w', encoding='ISO-8859-9') as output_file:
                output_file.write("\n".join(updated_lines))
                output_file.write("\r\n")  # Dosyanın sonuna CR LF ekle

            try:
                # Yazdırma işlemi başarılı olduğunda log kaydet
                save_print_log(request, placeholders, output_tspl_path)
                print("DEBUG: Print log kayıt işlemi başarılı!")
                send_data_to_serial_printer(output_tspl_path)
                JsonResponse({'success': True, 'message': 'Label sent via RS232 successfully'})
            except:
                return JsonResponse({'success': True, 'message': 'Başarısız'})


            #subprocess.run(['lp', output_tspl_path], check=True)

            # Yazıcıya bağlan
            printer = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)
            if printer is None:
                return JsonResponse({'success': False, 'message': 'Printer not found.'}, status=404)

            # Kernel sürücüsünü serbest bırak
            if printer.is_kernel_driver_active(0):
                printer.detach_kernel_driver(0)

            # Yazıcıyı yapılandır
            printer.set_configuration()

            with open(output_tspl_path, 'rb') as file:
                tspl_data = file.read()

            # Yazdırma işlemi için deneme mekanizması
            for attempt in range(MAX_RETRIES):
                try:
                    printer.write(OUT_ENDPOINT, tspl_data)

                    # Yazdırma işleminden sonra yazıcıyı serbest bırak
                    release_usb(printer)

                    return JsonResponse({'success': True, 'message': f'File sent to printer successfully on attempt {attempt + 1}.'})
                except usb.core.USBError as e:
                    if e.errno == 16:  # Resource Busy
                        reset_usb_port(printer)  # USB portunu resetle
                        time.sleep(RETRY_DELAY)
                    elif e.errno == 13:  # Permission Denied
                        return JsonResponse({'success': False, 'message': 'Permission denied. Check USB permissions.'}, status=403)
                    else:
                        return JsonResponse({'success': False, 'message': f'USB error: {str(e)}'}, status=500)
            # Maksimum deneme sayısına ulaşıldı
            return JsonResponse({'success': False, 'message': 'Printer is busy. Maximum retries reached.'}, status=500)

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON format.'}, status=400)
        except Exception as e:
            import traceback
            error_message = traceback.format_exc()
            print(error_message)
            return JsonResponse({'success': False, 'message': f'Unexpected error: {str(e)}'}, status=500)

    return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=400)
"""

import serial

# **RS232 Yazıcı Tanımlamaları**
SERIAL_PORT = "/dev/ttyS1"  # Linux için
# SERIAL_PORT = "COM3"  # Windows için
BAUDRATE = 115200  # Yazıcının baudrate hızı

def send_data_to_serial_printer(file_path):
    #RS232 (seri port) yazıcıya TSPL komutlarını gönderir.
    try:
        with open(file_path, 'r', encoding='ISO-8859-9') as file:
            tspl_data = file.read()

        with serial.Serial(SERIAL_PORT, BAUDRATE, timeout=2) as ser:
            ser.write(tspl_data.encode('ISO-8859-9'))
            ser.flush()
            print("File sent to Serial (RS232) printer successfully.")
            return True
    except Exception as e:
        print(f"Unexpected serial error: {str(e)}")
        return False


"""
@csrf_exempt
def print_file(request):
    if request.method == 'POST':
        try:
            import json, os, re
            from django.http import JsonResponse
            from django.conf import settings
            from datetime import datetime
            import subprocess

            # JSON verilerini al
            data = json.loads(request.body)
            placeholders = {
                "%net%": data.get('weight', '').strip(),
                "%partino%": data.get('customText', '').strip(),
                "%musteri_ismi1%": data.get('customerName', ''),
                "%musteri_ismi2%": data.get('customerName2', ''),
                "%urun_ismi1%": data.get('productName', ''),
                "%urun_kodu%": data.get('productCode', ''),
                "%sno%": data.get('serialNumber', ''),
                "%musteri_adresi%": data.get('customerAddress', ''),
                "%date%": datetime.now().strftime('%d-%m-%Y')
            }

            minimum_x_position = 0
            line_spacing = 25  # Satırlar arası boşluk
            max_chars_per_line = 25  # Bir satırda maksimum karakter sayısı

            file_path = os.path.join(settings.BASE_DIR, 'static', 'printer', 'eyz.prn')
            yaz_file_path = os.path.join(settings.BASE_DIR, 'static', 'printer', 'yaz_eyz.prn')

            if not os.path.exists(file_path):
                return JsonResponse({'success': False, 'message': 'Template file not found.'}, status=404)

            with open(file_path, 'r', encoding='ISO-8859-9') as file:
                content = file.read()

                # ENDUTEK.TTF yerine 0 koy
                content = content.replace('ENDUTEK.TTF', '0')

                for placeholder, value in placeholders.items():
                    if placeholder not in content:
                        print(f"Placeholder {placeholder} not found in template.")
                        continue

                    match = re.search(
                        rf'TEXT\s+(\d+),(\d+),\"(\d+)\",(\d+),(\d+),(\d+),\".*{re.escape(placeholder)}.*\"',
                        content
                    )
                    if not match:
                        print(f"No match found for placeholder: {placeholder}")
                        continue

                    original_x_position = int(match.group(1))
                    y_position = int(match.group(2))
                    font_type = match.group(3)
                    rotation = int(match.group(4))
                    font_width = int(match.group(5))
                    font_height = int(match.group(6))

                    # Metni 25 karakterlik parçalara ayır
                    def chunk_text(text, chunk_size):
                        return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

                    chunks = chunk_text(value, max_chars_per_line)

                    # Her parça için yeni satırlar oluştur
                    new_lines = []
                    for i, chunk in enumerate(chunks):
                        chunk_length = len(chunk)  # Parçanın uzunluğunu öğren
                        total_width = chunk_length * font_width  # Metnin toplam genişliği
                        adjusted_x = max(
                            ((original_x_position // 2) - (total_width // 2)),  # X eksenini ortala
                            minimum_x_position
                        )
                        adjusted_x = max(min(adjusted_x, 700), minimum_x_position)  # Sınırlar içinde tut
                        new_line = f'TEXT {adjusted_x},{y_position - (i * line_spacing)},"{font_type}",{rotation},{font_width},{font_height},"{chunk}"\n'
                        new_lines.append(new_line)

                    # TEXT içinde sadece placeholder'ı değiştir
                    content = re.sub(
                        rf'(TEXT\s+\d+,\d+,\"[^\"]+\",\d+,\d+,\d+,\".*){re.escape(placeholder)}(.*\")',
                        lambda m: f"{m.group(1)}{value}{m.group(2)}",
                        content
                    )

            with open(yaz_file_path, 'w', encoding='ISO-8859-9') as yaz_file:
                yaz_file.write(content)

            subprocess.run(['lp', yaz_file_path], check=True)

            return JsonResponse({'success': True, 'message': 'Etiket başarıyla yazdırıldı.'})

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON format.'}, status=400)
        except Exception as e:
            import traceback
            error_message = traceback.format_exc()
            print(error_message)
            return JsonResponse({'success': False, 'message': f'Unexpected error: {str(e)}'}, status=500)

    return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=400)
"""

"""
@csrf_exempt
def print_file(request):
    if request.method == 'POST':
        try:
            # JSON body'den weight değerini al
            data = json.loads(request.body)
            weight = data.get('weight', '').strip()  # Ağırlığı al
            custom_text = data.get('customText', '').strip()
            customer_name = data.get('customerName')
            #customer_address = data.get("customerAddress")
            #customer_last_name = data.get("customerLastName")
            product_name = data.get('productName')
            product_code = data.get('productCode')

            # Bugünün tarihi
            today_date = datetime.now().strftime('%d-%m-%Y')  # Gün-Ay-Yıl formatında

            if not weight:
                return JsonResponse({'success': False, 'message': 'Weight value is missing.'}, status=400)

            # Dosya yolları
            file_path = os.path.join(settings.BASE_DIR, 'static', 'printer', 'eyz.prn')
            yaz_file_path = os.path.join(settings.BASE_DIR, 'static', 'printer', 'yaz_eyz.prn')
            if not os.path.exists(file_path):
                return JsonResponse({'success': False, 'message': 'Template file not found.'}, status=404)

            # Dosya içeriğini oku ve %net% ile tartı bilgisini değiştir
            with open(file_path, 'r', encoding='ISO-8859-9') as file:
                content = file.read()
                content = content.replace('%net%', weight)
                content = content.replace('%partino%', custom_text)
                content = content.replace('%musteri_ismi1%', customer_name)
                #content = content.replace('%musteri_ismi2%', customer_last_name)
                #content = content.replace('%musteri_adres%', customer_address)
                content = content.replace('%urun_ismi1%', product_name)
                content = content.replace('%urun_kodu%', product_code)
                content = content.replace('%date%', today_date)
                content = content.replace('ENDUTEK.TTF', '0')

            # Geçici dosyaya yaz
            with open(yaz_file_path, 'w') as yaz_file:
                yaz_file.write(content)

            # Yazıcıya gönder
            subprocess.run(['lp', yaz_file_path], check=True)
            
            # Yazıcıya bağlan
            printer = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)
            if printer is None:
                return JsonResponse({'success': False, 'message': 'Printer not found.'}, status=404)

            # Kernel sürücüsünü serbest bırak
            if printer.is_kernel_driver_active(0):
                printer.detach_kernel_driver(0)

            # Yazıcıyı yapılandır
            printer.set_configuration()

            # Yazdırma işlemi için deneme mekanizması
            for attempt in range(MAX_RETRIES):
                try:
                    printer.write(OUT_ENDPOINT, content.encode('ISO-8859-9'))

                    # Yazdırma işleminden sonra yazıcıyı serbest bırak
                    release_usb(printer)

                    # Yazdırma bilgilerini SQL'e kaydet
                    save_print_log(weight, file_path)

                    return JsonResponse({'success': True, 'message': f'File sent to printer successfully on attempt {attempt + 1}.'})
                except usb.core.USBError as e:
                    if e.errno == 16:  # Resource Busy
                        reset_usb_port(printer)  # USB portunu resetle
                        time.sleep(RETRY_DELAY)
                    elif e.errno == 13:  # Permission Denied
                        return JsonResponse({'success': False, 'message': 'Permission denied. Check USB permissions.'}, status=403)
                    else:
                        return JsonResponse({'success': False, 'message': f'USB error: {str(e)}'}, status=500)

            # Maksimum deneme sayısına ulaşıldı
            return JsonResponse({'success': False, 'message': 'Printer is busy. Maximum retries reached.'}, status=500)
            """"""
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON format.'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Unexpected error: {str(e)}'}, status=500)

    return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=400)
"""

@csrf_exempt
def print_label(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            weight = data.get('weight', '').strip()  # Ağırlığı al
            custom_text = data.get('customText', '').strip()
            customer_name = data.get('customerName')
            #customer_address = data.get("customerAddress")
            #customer_last_name = data.get("customerLastName")
            product_name = data.get('productName')
            product_code = data.get('productCode')

            # Bugünün tarihi
            today_date = datetime.now().strftime('%d-%m-%Y')  # Gün-Ay-Yıl formatında

            if not weight:
                return JsonResponse({'success': False, 'message': 'Weight value is missing.'}, status=400)

            file_path = os.path.join(settings.BASE_DIR, 'static', 'printer', 'eyz.prn')
            yaz_file_path = os.path.join(settings.BASE_DIR, 'static', 'printer', 'yaz_eyz.prn')

            if not os.path.exists(file_path):
                return JsonResponse({'success': False, 'message': 'Template file not found.'}, status=404)

            with open(file_path, 'r', encoding='ISO-8859-9') as file:
                content = file.read()
                content = file.read().replace('%net%', weight)
                content = content.replace('%partino%', custom_text)
                content = content.replace('%musteri_ismi1%', customer_name)
                #content = content.replace('%musteri_ismi2%', customer_last_name)
                #content = content.replace('%musteri_adres%', customer_address)
                content = content.replace('%urun_ismi1%', product_name)
                content = content.replace('%urun_kodu%', product_code)
                content = content.replace('%date%', today_date)
                content = content.replace('ENDUTEK.TTF', '0')

            with open(yaz_file_path, 'w') as yaz_file:
                yaz_file.write(content)

            #subprocess.run(['lp', yaz_file_path], check=True)

            return JsonResponse({'success': True, 'message': 'Etiket yazdırıldı.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Unexpected error: {str(e)}'}, status=500)

    return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=400)

def reset_usb_port(printer):
    """
    USB portunu resetler ve yazıcıyı serbest bırakır.
    """
    try:
        printer.reset()  # Yazıcıyı sıfırla
        print("USB port has been reset.")
    except usb.core.USBError as e:
        print(f"Error resetting USB port: {str(e)}")

def release_usb(printer):
    """
    Yazıcıyı serbest bırakır ve kernel sürücüsünü yeniden bağlar.
    """
    try:
        usb.util.dispose_resources(printer)  # Kaynakları serbest bırak
        if not printer.is_kernel_driver_active(0):
            printer.attach_kernel_driver(0)  # Kernel sürücüsünü yeniden bağla
        print("USB resources released and kernel driver reattached.")
    except usb.core.USBError as e:
        print(f"Error releasing USB resources: {str(e)}")


def save_print_log(request, placeholders, file_path):
    try:
        product = Product.objects.filter(urun_kod=placeholders.get("%urun_kodu%", None)).first()
        customer = Customer.objects.filter(first_name=placeholders.get("%musteri_ismi1%", None)).first()

        PrintLog.objects.create(
            user=request.user if request.user.is_authenticated else None,

            # Müşteri bilgileri
            customer=customer,
            customer_name1=placeholders.get("%musteri_ismi1%", "Tanımsız"),
            customer_name2=placeholders.get("%musteri_ismi2%", "Tanımsız"),
            customer_address=placeholders.get("%musteri_adresi%", "Tanımsız"),

            # Ürün bilgileri
            product=product,
            product_category = product.category,
            product_name=placeholders.get("%urun_ismi1%", "Tanımsız"),
            product_code=placeholders.get("%urun_kodu%", "Tanımsız"),
            product_barkod=placeholders.get("%urun_barkod%", "Tanımsız"),
            product_stt=placeholders.get("%stt%", "Tanımsız"),

            # Diğer bilgiler
            weight=placeholders.get("%pakettopnet%", "Tanımsız"),
            topnet=placeholders.get("%topnet%", "Tanımsız"),  # 👈 EKLENEN SATIR
            custom_text=placeholders.get("%partino%", "Tanımsız"),
            serial_number=placeholders.get("%sno%", "Tanımsız"),
            date_text=placeholders.get("%urt%", "Tanımsız"),
            time_text=placeholders.get("%saat%", "Tanımsız"),
            paket_sayisi=placeholders.get("%paketsayisi%", "Tanımsız"),
            toplam_paket_sayisi = placeholders.get("%topadet%", "Tanımsız"),

            # Mesajlar ve içerik
            msg1=placeholders.get("%msg1%", "Tanımsız"),
            msg2=placeholders.get("%msg2%", "Tanımsız"),
            msg3=placeholders.get("%msg3%", "Tanımsız"),
            msg4=placeholders.get("%msg4%", "Tanımsız"),
            msg5=placeholders.get("%msg5%", "Tanımsız"),
            msg6=placeholders.get("%msg6%", "Tanımsız"),
            msg7=placeholders.get("%msg7%", "Tanımsız"),
            msg8=placeholders.get("%msg8%", "Tanımsız"),
            msg9=placeholders.get("%msg9%", "Tanımsız"),
            icerik=placeholders.get("%icerik%", "Tanımsız"),

            # Dosya ve zaman
            file_path=file_path,
            timestamp=datetime.now()
        )
        print("DEBUG: Print log kayıt işlemi başarılı!")
    except Exception as e:
        import traceback
        error_message = traceback.format_exc()
        print(f"ERROR: Print log kaydedilirken hata oluştu: {error_message}")


def send_data_to_usb_printer(file_path):
    """
    Manuel (manual) yazdırmada kullanılacak: USB yazıcıya gönderme.
    """
    try:
        printer = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)
        if printer is None:
            print("USB Printer not found.")
            return False

        if printer.is_kernel_driver_active(0):
            printer.detach_kernel_driver(0)

        printer.set_configuration()

        with open(file_path, 'rb') as f:
            tspl_data = f.read()

        # Deneme mekanizması
        for attempt in range(MAX_RETRIES):
            try:
                printer.write(OUT_ENDPOINT, tspl_data)
                release_usb(printer)
                print(f"USB printing success at attempt {attempt+1}.")
                return True

            except usb.core.USBError as e:
                print(f"USB printing error at attempt {attempt+1}: {e}")
                if e.errno == 16:  # Resource Busy
                    reset_usb_port(printer)
                    time.sleep(RETRY_DELAY)
                elif e.errno == 13:  # Permission Denied
                    print("USB permission denied. Check udev rules or user group.")
                    return False
                else:
                    return False

        print("USB printer is busy. Max retries reached.")
        return False

    except Exception as ex:
        print(f"USB printing exception: {ex}")
        return False


"""
def check_printer_status():
    #Yazıcının meşgul olup olmadığını kontrol eder.
    
    try:
        printer = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)
        if printer is None:
            return {'status': 'not_found', 'message': 'Printer not found.'}

        if printer.is_kernel_driver_active(0):
            printer.detach_kernel_driver(0)

        printer.set_configuration()

        try:
            status = printer.read(STATUS_ENDPOINT, 64, timeout=1000)
            if status[0] == 0x00:
                return {'status': 'idle', 'message': 'Printer is idle and ready.'}
            elif status[0] == 0x01:
                return {'status': 'busy', 'message': 'Printer is busy.'}
            else:
                return {'status': 'unknown', 'message': 'Unknown printer status.'}
        except usb.core.USBError as e:
            if e.errno == 110:  # Timeout
                return {'status': 'timeout', 'message': 'No response from printer.'}
            else:
                return {'status': 'error', 'message': f'USB error: {str(e)}'}
    except Exception as e:
        return {'status': 'error', 'message': f'Unexpected error: {str(e)}'}
"""

"""
import json
import os
import subprocess
from django.http import JsonResponse
from django.conf import settings

def print_file(request):
    if request.method == 'POST':
        try:
            # JSON body'den weight değerini al
            data = json.loads(request.body)
            weight = data.get('weight')
            if not weight:
                return JsonResponse({'success': False, 'message': 'Weight value is missing.'}, status=400)

            # Dosya yolları
            file_path = os.path.join(settings.BASE_DIR, 'static', 'printer', 'eyz.prn')
            temp_file_path = os.path.join(settings.BASE_DIR, 'static', 'printer', 'temp_eyz.prn')

            if not os.path.exists(file_path):
                return JsonResponse({'success': False, 'message': 'Template file not found.'}, status=404)

            # Dosya içeriğini oku ve %net% ile tartı bilgisini değiştir
            with open(file_path, 'r', encoding='ISO-8859-9') as file:
                # Binary içerik üzerinde %net% yer tutucusunu değiştir
                content = file.read()
            try:
                content = content.replace('%net%', weight)
            except Exception as e:
                return JsonResponse({'success': False, 'message': f'Replace error: {str(e)}'}, status=500)

            # Geçici dosyaya yaz
            with open(temp_file_path, 'w') as temp_file:
                temp_file.write(content)

            # Yazıcıya gönder
            subprocess.run(['lp', temp_file_path], check=True)

            # Geçici dosyayı temizle
            os.remove(temp_file_path)

            return JsonResponse({'success': True, 'message': 'File sent to printer successfully.'})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON format.'}, status=400)
        except subprocess.CalledProcessError as e:
            return JsonResponse({'success': False, 'message': f'Printing error: {str(e)}'}, status=500)
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Unexpected error: {str(e)}'}, status=500)
    return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=400)
"""

from django.http import HttpResponse
from .models import PrintLog
import csv

def export_print_logs(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="print_logs.csv"'

    writer = csv.writer(response)
    writer.writerow(['Tarih', 'Müşteri Adı', 'Ürün Adı', 'Ağırlık'])

    for log in PrintLog.objects.all():
        writer.writerow([log.timestamp.strftime('%d-%m-%Y %H:%M'), log.customer_name1, log.product_name, log.weight])

    return response

from collections import defaultdict
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from customers.models import Customer
from products.models import Product

@login_required(login_url="/accounts/login/")
def sales_add_view(request):
    # Ürünleri kategorilere göre gruplandır
    categorized_products = defaultdict(list)
    products = Product.objects.all()

    for product in products:
        category = product.category if product.category else 'Genel'
        categorized_products[category].append(product)

    context = {
        "active_icon": "sales",
        "customers": [c.to_select2() for c in Customer.objects.all()],
        "categorized_products": categorized_products,
        'NODE_SERVER_IP': "127.0.0.1"  # Varsayılan Node Server IP
    }

    return render(request, "sales/sales_add.html", context=context)


@login_required
def print_log_list(request):
    logs = PrintLog.objects.all().order_by('-timestamp')
    return render(request, "sales/print_log_list.html", {'logs': logs})


from django.http import HttpResponse
from openpyxl import Workbook
from django.utils.encoding import smart_str

def print_log_report(request):
    from .models import PrintLog
    from django.db.models import Sum, IntegerField
    from django.db.models.functions import Cast
    from datetime import datetime, timedelta
    from django.utils import timezone

    logs_qs = PrintLog.objects.all().order_by('-timestamp')

    # Tarih aralığı filtreleme
    start_date_str = request.GET.get("start_date")
    end_date_str = request.GET.get("end_date")
    if start_date_str and end_date_str:
        try:
            # Gelen tarih "YYYY-MM-DD" formatındadır
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
        except ValueError:
            start_date = end_date = None

        if start_date and end_date:
            # Yerel saat diliminize göre bilinçli (aware) datetime nesneleri oluşturun
            current_tz = timezone.get_current_timezone()
            start_date = timezone.make_aware(start_date, current_tz)
            # Bitiş tarihini günün sonuna (23:59:59) ayarlayın
            end_date = timezone.make_aware(end_date + timedelta(days=1) - timedelta(seconds=1), current_tz)

            logs_qs = logs_qs.filter(timestamp__range=[start_date, end_date])

    # Eğer Excel butonuna basılmışsa
    if request.GET.get("export") == "excel":
        return export_logs_to_excel(logs_qs)

    logs = [
        {
            #'Tarih': localtime(log.timestamp).strftime('%d-%m-%Y %H:%M'),
            'Tarih': log.timestamp.strftime('%d-%m-%Y %H:%M'),
            'Musteri': log.customer_name1,
            'Kategori': log.product_category.name if log.product_category else 'Genel',
            'Urun': log.product_name,
            'Agirlik': log.weight,
            'Operator': log.user.username if log.user else '',
            'Paket_Sayisi': log.paket_sayisi,
            'Toplam_Paket_Sayisi': log.toplam_paket_sayisi,
        }
        for log in logs_qs
    ]

    # Paket sayısı sadece sayısal olanlardan toplansın
    logs_qs_filtered = logs_qs.filter(paket_sayisi__regex=r'^\d+$')

    total_weight = logs_qs.aggregate(Sum('weight'))['weight__sum'] or 0
    total_adet = logs_qs_filtered.aggregate(total=Sum(Cast('paket_sayisi', IntegerField())))['total'] or 0
    total_count = logs_qs.count()

    return render(request, "sales/print_log_report.html", {
        'logs': logs,
        'total_count': total_count,
        'total_weight': total_weight,
        'total_adet': total_adet
    })

from django.utils.timezone import localtime

def export_logs_to_excel(queryset):
    wb = Workbook()
    ws = wb.active
    ws.title = "Yazdırma Kayıtları"

    columns = [
        'Tarih', 'Müşteri', 'Kategori', 'Ürün', 
        'Ağırlık', 'Operatör', 'Paket Sayısı', 'Toplam Paket Sayısı'
    ]
    ws.append(columns)

    for log in queryset:
        ws.append([
            log.timestamp.strftime('%d-%m-%Y %H:%M'),
            smart_str(log.customer_name1),
            smart_str(log.product_category.name if log.product_category else 'Genel'),
            smart_str(log.product_name),
            log.weight,
            smart_str(log.user.username if log.user else ''),
            log.paket_sayisi,
            log.toplam_paket_sayisi,
        ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="yazdirma_kayitlari.xlsx"'
    wb.save(response)
    return response

