from django.db import models

class Terazi(models.Model):
    kod = models.CharField(max_length=50)  # KOD
    isim = models.CharField(max_length=255)  # ISIM
    raf_omru = models.IntegerField(null=True, blank=True)  # RAFOMRU
    minimum_gr = models.FloatField(null=True, blank=True)  # MINIMUMGR
    max_gr = models.FloatField(null=True, blank=True)  # MAXGR
    barkod = models.CharField(max_length=50, null=True, blank=True)  # BARKOD
    enerji = models.FloatField(null=True, blank=True)  # Enerji
    yag = models.FloatField(null=True, blank=True)  # Yag
    doymus_yag = models.FloatField(null=True, blank=True)  # DoymusYag
    karbonhidrat = models.FloatField(null=True, blank=True)  # Karbonhidrat
    sekerler = models.FloatField(null=True, blank=True)  # Sekerler
    protein = models.FloatField(null=True, blank=True)  # Protein
    tuz = models.FloatField(null=True, blank=True)  # Tuz
    icindekiler_1 = models.TextField(null=True, blank=True)  # Icindekiler_1
    icindekiler_2 = models.TextField(null=True, blank=True)  # Icindekiler_2

    class Meta:
        managed = False  # Django'nun tabloyu yönetmesini istemiyoruz
        db_table = '_TERAZI'  # SQL Server'daki view adı
