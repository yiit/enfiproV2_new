import os
import django
from django.conf import settings  # ✅ settings modülünü doğru içe aktarın

# Ayar dosyanızı doğru tanımlayın
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_pos.settings')

# Django ortamını başlat
django.setup()

from django.db import connections
from products.models import Product, Category

# Tüm verileri sil
#Product.objects.all().delete()
#print("✅ Product tablosundaki tüm veriler silindi!")

# ✅ Varsayılan kategori ekle (Eğer yoksa oluştur)
try:
    # ID'si 1 olan ilk kategoriye eriş
    kategori = Category.objects.get(id=1)
except Category.DoesNotExist:
    # Eğer ID 1'de bir kategori yoksa, ilk bulunan kategoriyi al
    kategori = Category.objects.first()

# Eğer hala kategori bulunamadıysa, varsayılan bir kategori oluştur
if not kategori:
    kategori = Category.objects.create(name="Varsayılan Kategori", status="ACTIVE")

# PRN dosyalarının olduğu klasör
prn_folder = os.path.join(settings.BASE_DIR, 'static', 'printer')

# Klasördeki tüm .prn dosyalarını al
eyz_prn_files = [file for file in os.listdir(prn_folder) if file.endswith(".prn")]

# İlk sıradaki PRN dosyasını varsayılan olarak ayarla
default_prn_file = eyz_prn_files[0] if eyz_prn_files else "Tanımsız"

# ✅ SQL Server bağlantısını aç ve sadece barkodu olan verileri çek
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

# ✅ PostgreSQL'e aktar (Silme işlemi yapılmaz, sadece ekleme/güncelleme yapılır)
for veri in veriler:
    (
        urun_kod, urun_ismi1, urun_stt, urun_min, urun_max, urun_barkod,
        urun_mesaj1, urun_mesaj2, urun_mesaj3, urun_mesaj4, urun_mesaj5,
        urun_mesaj6, urun_mesaj7, urun_icerik, urun_aciklama
    ) = veri

    # Eğer barkod boşsa bu ürünü atla
    if not urun_barkod:
        print(f"🚫 Barkodsuz ürün atlandı: {urun_ismi1} ({urun_kod})")
        continue


    # 🔥 Eğer barkod, kod, isim veya diğer kritik alanlar boşsa varsayılan bir değer ata
    urun_kod = urun_kod or "Tanımsız"
    urun_ismi1 = urun_ismi1 or "Tanımsız"
    urun_barkod = urun_barkod or "Tanımsız"
    #urun_kodtip = urun_kodtip or "Tanımsız"
    urun_icerik = urun_icerik or "Tanımsız"

    # 🔥 Numeric alanlar için None değerleri sıfıra çevir
    urun_min = urun_min or 0
    urun_max = urun_max or 0
    urun_stt = urun_stt or 0

    # ✅ PostgreSQL'de ürün var mı kontrol et
    urun = Product.objects.filter(urun_kod=urun_kod, urun_barkod=urun_barkod).first()

    if urun:
        # 🛠️ Güncelleme yap (SQL Server'dan gelenleri değiştir, diğerlerini koru)
        urun.urun_ismi1 = urun_ismi1
        urun.urun_barkod = urun_barkod
        urun.urun_min = urun_min
        urun.urun_max = urun_max
        urun.urun_stt = urun_stt
        #urun.urun_kodtip = urun_kodtip
        urun.urun_icerik = urun_icerik
        urun.urun_mesaj1 = urun_mesaj1 or urun.urun_mesaj1
        urun.urun_mesaj2 = urun_mesaj2 or urun.urun_mesaj2
        urun.urun_mesaj3 = urun_mesaj3 or urun.urun_mesaj3
        urun.urun_mesaj4 = urun_mesaj4 or urun.urun_mesaj4
        urun.urun_mesaj5 = urun_mesaj5 or urun.urun_mesaj5
        urun.urun_mesaj6 = urun_mesaj6 or urun.urun_mesaj6
        urun.urun_mesaj7 = urun_mesaj7 or urun.urun_mesaj7
        urun.save()
        print(f"🔄 Güncellendi: {urun_ismi1} ({urun_kod})")
    else:
        # 🆕 Yeni ürün ekle
        yeni_urun = Product(
            urun_kod=urun_kod,
            urun_ismi1=urun_ismi1,
            urun_barkod=urun_barkod,
            urun_min=urun_min,
            urun_max=urun_max,
            urun_etiket=default_prn_file,
            urun_fiyat=0,  # SQL Server'da fiyat bilgisi yok, sıfır olarak ayarlandı
            urun_dara=0,    # Dara bilgisi olmadığı için sıfır yapıldı
            #urun_kodtip=urun_kodtip,
            urun_stt=urun_stt,
            urun_icerik=urun_icerik,
            urun_mesaj1=urun_mesaj1 or "Tanımsız",
            urun_mesaj2=urun_mesaj2 or "Tanımsız",
            urun_mesaj3=urun_mesaj3 or "Tanımsız",
            urun_mesaj4=urun_mesaj4 or "Tanımsız",
            urun_mesaj5=urun_mesaj5 or "Tanımsız",
            urun_mesaj6=urun_mesaj6 or "Tanımsız",
            urun_mesaj7=urun_mesaj7 or "Tanımsız",
            category=kategori,  # ✅ NULL olmaması için kategori ekledik
            status="ACTIVE"
        )
        yeni_urun.save()
        print(f"🆕 Yeni ürün eklendi: {urun_ismi1} ({urun_kod})")

print("✅ SQL Server'daki `_TERAZI` verileri PostgreSQL'deki `Product` tablosuna başarıyla aktarıldı! 🚀")