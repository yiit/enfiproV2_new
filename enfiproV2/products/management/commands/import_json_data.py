import json
from django.core.management.base import BaseCommand
from products.models import Product, Category

# Tüm verileri sil
Product.objects.all().delete()
#print("✅ Product tablosundaki tüm veriler silindi!")

class Command(BaseCommand):
    help = 'JSON verisini Product modeline aktarır'

    def handle(self, *args, **kwargs):
        # JSON dosyasını UTF-8 kodlamasıyla açıyoruz
        with open('plus.json', encoding='utf-8') as f:
            data = json.load(f)

        for product_data in data:
            if isinstance(product_data, dict) and 'urun_kodu' in product_data:
                # Kategori seçimi: kategori varsa kullan, yoksa varsayılan ID=1
                category_name = product_data.get('kategori', None)
                if category_name:
                    category, _ = Category.objects.get_or_create(name=category_name.strip())
                else:
                    category = Category.objects.get(id=1)

                # JSON'dan gelen etiket verilerini alıyoruz
                etiket_form = product_data.get('etiket_form', '').strip()
                top_etiket_form = product_data.get('top_etiket_form', '').strip()

                # "printer/" ön ekini kaldırıyoruz
                if etiket_form.lower().startswith('printer/'):
                    etiket_form = etiket_form[len('printer/'):].strip()
                if top_etiket_form.lower().startswith('printer/'):
                    top_etiket_form = top_etiket_form[len('printer/'):].strip()

                # Eğer değerlerin sonu .prn ile bitmiyorsa ekliyoruz
                if etiket_form and not etiket_form.lower().endswith('.prn'):
                    etiket_form += '.prn'
                if top_etiket_form and not top_etiket_form.lower().endswith('.prn'):
                    top_etiket_form += '.prn'

                product = Product.objects.create(
                    urun_kod=product_data.get('urun_kodu', '').strip(),
                    urun_ismi1=product_data.get('urun_ismi', '').strip(),
                    urun_ismi2=product_data.get('urun_ismi2', '').strip(),
                    urun_grup=product_data.get('urun_grup', '').strip(),
                    urun_fiyat=product_data.get('urun_fiyat', 0),
                    urun_barkod=product_data.get('urun_barkodu', '').strip(),
                    urun_qrkod=product_data.get('urun_qrkod', '').strip(),
                    urun_min=product_data.get('minimum_gramaj', 0),
                    urun_max=product_data.get('maximum_gramaj', 0),
                    urun_hedef=product_data.get('adet_sayisi', 0),
                    urun_etiket=etiket_form,
                    urun_top_etiket=top_etiket_form,
                    urun_izleme=product_data.get('urun_izleme', '').strip(),
                    urun_tanim=product_data.get('urun_tanim', '').strip(),
                    urun_mesaj1=product_data.get('etiket_mesaj1', '').strip(),
                    urun_mesaj2=product_data.get('etiket_mesaj2', '').strip(),
                    urun_mesaj3=product_data.get('etiket_mesaj3', '').strip(),
                    urun_mesaj4=product_data.get('etiket_mesaj4', '').strip(),
                    urun_mesaj5=product_data.get('etiket_mesaj5', '').strip(),
                    category=category,
                    status="ACTIVE",    # Varsayılan değer ACTIVATE
                    name="TANIMSIZ"        # Varsayılan değer TANIMSIZ
                )

                self.stdout.write(self.style.SUCCESS(
                    f"Ürün {product.urun_ismi1} eklendi. (Etiket: {product.urun_etiket} - Top Etiket: {product.urun_top_etiket})"
                ))
