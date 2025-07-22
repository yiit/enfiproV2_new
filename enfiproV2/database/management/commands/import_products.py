import os
import sys
import json
from django.core.management.base import BaseCommand

# Proje kök dizinini sys.path'e ekleyin (manage.py'nin bulunduğu dizin)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(PROJECT_ROOT))

# DJANGO_SETTINGS_MODULE ayarını yapın
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_pos.settings")

import django
django.setup()

from database.models import Product, Category

class Command(BaseCommand):
    help = "Import products from a JSON file into the database."

    def add_arguments(self, parser):
        parser.add_argument(
            '--json_path',
            type=str,
            default="plus.json",  # Varsayılan dosya adı (manage.py'nin bulunduğu dizinde arar)
            help="Path to the JSON file containing product data"
        )

    def handle(self, *args, **options):
        json_path = options['json_path']

        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f"JSON dosyası bulunamadı: {json_path}"))
            return

        default_category, _ = Category.objects.get_or_create(
            name="Otomatik",
            defaults={"description": "Otomatik eklenenler", "status": "ACTIVE"}
        )

        count = 0
        for item in data:
            # Sadece 'urun_kodu' değeri varsa ekleyelim
            if not isinstance(item, dict) or not item.get("urun_kodu"):
                continue

            Product.objects.create(
                name=item.get("urun_ismi", "Tanımsız"),
                description=item.get("etiket_tanimi", ""),
                status="ACTIVE",
                category=default_category,
                urun_kod=item.get("urun_kodu", ""),
                urun_barkod=item.get("urun_barkodu", ""),
                urun_mesaj1=item.get("etiket_mesaj1", ""),
                urun_mesaj2=item.get("etiket_mesaj2", ""),
                urun_mesaj3=item.get("etiket_mesaj3", ""),
                urun_mesaj4=item.get("etiket_mesaj4", ""),
                urun_mesaj5=item.get("etiket_mesaj5", ""),
                urun_etiket=item.get("etiket_form", ""),
                urun_top_etiket=item.get("top_etiket_form", ""),
            )
            count += 1

        self.stdout.write(self.style.SUCCESS(f"[+] Toplam {count} ürün başarıyla eklendi."))
