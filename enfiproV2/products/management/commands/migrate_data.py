import os
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import connections
from products.models import Product, Category

class Command(BaseCommand):
    help = 'SQL Server’dan verileri okuyup PostgreSQL veritabanına aktarır.'

    def handle(self, *args, **kwargs):
        #Product.objects.all().delete()
        #self.stdout.write("✅ Product tablosundaki tüm veriler silindi!")

        try:
            kategori = Category.objects.get(id=1)
        except Category.DoesNotExist:
            kategori = Category.objects.first()
        if not kategori:
            kategori = Category.objects.create(name="Varsayılan Kategori", status="ACTIVE")

        prn_folder = os.path.join(settings.BASE_DIR, 'static', 'printer')
        prn_files = [file for file in os.listdir(prn_folder) if file.endswith(".prn")]
        default_prn_file = prn_files[0] if prn_files else "Tanımsız"

        sql_conn = connections['sqlserver'].cursor()
        sql_conn.execute("""
            SELECT KOD, ISIM, RAFOMRU, MINIMUMGR, MAXGR, BARKOD, 
                   Enerji, Yag, DoymusYag, Karbonhidrat, Sekerler, 
                   Protein, Tuz, Icindekiler_1, Icindekiler_2 
            FROM _TERAZI
            WHERE BARKOD IS NOT NULL AND BARKOD != ''
        """)
        veriler = sql_conn.fetchall()
        sql_conn.close()

        for veri in veriler:
            (
                urun_kod, urun_ismi1, urun_stt, urun_min, urun_max, urun_barkod,
                urun_mesaj1, urun_mesaj2, urun_mesaj3, urun_mesaj4, urun_mesaj5,
                urun_mesaj6, urun_mesaj7, urun_icerik, urun_aciklama
            ) = veri

            if not urun_barkod:
                self.stdout.write(f"🚫 Barkodsuz ürün atlandı: {urun_ismi1} ({urun_kod})")
                continue

            urun = Product.objects.filter(urun_kod=urun_kod, urun_barkod=urun_barkod).first()

            if urun:
                urun.urun_ismi1 = urun_ismi1 or "Tanımsız"
                urun.urun_barkod = urun_barkod
                urun.urun_min = urun_min or 0
                urun.urun_max = urun_max or 0
                urun.urun_stt = urun_stt or 0
                urun.urun_icerik = urun_icerik or "Tanımsız"
                urun.urun_mesaj1 = urun_mesaj1 or urun.urun_mesaj1
                urun.urun_mesaj2 = urun_mesaj2 or urun.urun_mesaj2
                urun.urun_mesaj3 = urun_mesaj3 or urun.urun_mesaj3
                urun.urun_mesaj4 = urun_mesaj4 or urun.urun_mesaj4
                urun.urun_mesaj5 = urun_mesaj5 or urun.urun_mesaj5
                urun.urun_mesaj6 = urun_mesaj6 or urun.urun_mesaj6
                urun.urun_mesaj7 = urun_mesaj7 or urun.urun_mesaj7
                urun.save()
                self.stdout.write(f"🔄 Güncellendi: {urun_ismi1} ({urun_kod})")
            else:
                Product.objects.create(
                    urun_kod=urun_kod or "Tanımsız",
                    urun_ismi1=urun_ismi1 or "Tanımsız",
                    urun_barkod=urun_barkod,
                    urun_min=urun_min or 0,
                    urun_max=urun_max or 0,
                    urun_etiket=default_prn_file,
                    urun_fiyat=0,
                    urun_dara=0,
                    urun_stt=urun_stt or 0,
                    urun_icerik=urun_icerik or "Tanımsız",
                    urun_mesaj1=urun_mesaj1 or "Tanımsız",
                    urun_mesaj2=urun_mesaj2 or "Tanımsız",
                    urun_mesaj3=urun_mesaj3 or "Tanımsız",
                    urun_mesaj4=urun_mesaj4 or "Tanımsız",
                    urun_mesaj5=urun_mesaj5 or "Tanımsız",
                    urun_mesaj6=urun_mesaj6 or "Tanımsız",
                    urun_mesaj7=urun_mesaj7 or "Tanımsız",
                    urun_aciklama=urun_aciklama or "Tanımsız",
                    category=kategori,
                    status="ACTIVE"
                )
                self.stdout.write(f"🆕 Yeni ürün eklendi: {urun_ismi1} ({urun_kod})")

        self.stdout.write("✅ SQL Server'dan PostgreSQL'e veri aktarımı tamamlandı! 🚀")
