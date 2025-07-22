from django.db import models
from django.forms import model_to_dict
from decimal import Decimal


class Category(models.Model):
    STATUS_CHOICES = (  # new
        ("ACTIVE", "Aktif"),
        ("INACTIVE", "Pasif")
    )

    name = models.CharField(max_length=256)
    description = models.TextField(max_length=256)
    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=100,
        verbose_name="Status of the category",
    )

    class Meta:
        # Table's name
        db_table = "Category"
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    STATUS_CHOICES = (  # new
        ("ACTIVE", "Aktif"),
        ("INACTIVE", "Pasif")
    )

    URUN_TIP_CHOICES = (
        ("ADET", "Adet"),
        ("AGIRLIK", "Ağırlık"),
        ("FIYAT", "Fiyat"),
        ("SABITAGIRLIK", "Sabit Ağırlık"),
    )

    name = models.CharField(max_length=256, default="Tanımsız", blank=True)
    description = models.TextField(max_length=256, default="Tanımsız", blank=True)
    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=100,
        verbose_name="Status of the product",
    )
    category = models.ForeignKey(
        Category, related_name="category", on_delete=models.CASCADE, db_column='category')

    price            = models.FloatField(default=0, blank=True)
    urun_kod         = models.CharField(max_length=256, blank=True)
    urun_grup        = models.CharField(max_length=256, blank=True)
    urun_tip         = models.CharField(max_length=20, choices=URUN_TIP_CHOICES, default="AGIRLIK",blank=True)
    urun_ismi1       = models.CharField(max_length=256, blank=True)
    urun_ismi2       = models.CharField(max_length=256, blank=True)
    urun_fiyat       = models.DecimalField(max_digits=10, decimal_places=3, default=0.0)
    urun_musteri     = models.CharField(max_length=256, blank=True)
    urun_barkod      = models.CharField(max_length=256, blank=True)
    urun_qrkod       = models.CharField(max_length=256)
    urun_stt         = models.IntegerField(default=0, blank=True)
    urun_resim       = models.CharField(max_length=256, blank=True)
    urun_min         = models.DecimalField(max_digits=10, decimal_places=3, default=0.0)
    urun_max         = models.DecimalField(max_digits=10, decimal_places=3, default=0.0)
    urun_hedef       = models.IntegerField(default=0, blank=True)
    urun_adet_gramaj = models.DecimalField(max_digits=10, decimal_places=4, default=0.0000)
    urun_dara        = models.DecimalField(max_digits=10, decimal_places=3, default=0.0)
    urun_adet        = models.IntegerField(default=0, blank=True)
    urun_etiket      = models.CharField(max_length=256, blank=True)
    urun_top_etiket  = models.CharField(max_length=256, blank=True)
    urun_izleme      = models.CharField(max_length=256, blank=True)
    urun_kodtip      = models.CharField(max_length=256, blank=True)
    urun_tablo       = models.CharField(max_length=256, blank=True)
    urun_mesaj1      = models.TextField(max_length=256, blank=True)
    urun_mesaj2      = models.TextField(max_length=256, blank=True)
    urun_mesaj3      = models.TextField(max_length=256, blank=True)
    urun_mesaj4      = models.TextField(max_length=256, blank=True)
    urun_mesaj5      = models.TextField(max_length=256, blank=True)
    urun_mesaj6      = models.TextField(max_length=256, blank=True)
    urun_mesaj7      = models.TextField(max_length=256, blank=True)
    urun_mesaj8      = models.TextField(max_length=256, blank=True)
    urun_mesaj9      = models.TextField(max_length=256, blank=True)
    urun_tanim       = models.TextField(max_length=256, blank=True)
    urun_icerik      = models.TextField(max_length=256, blank=True)
    urun_aciklama    = models.TextField(max_length=256, blank=True)
    urun_mensei      = models.CharField(max_length=256, blank=True)


    class Meta:
        # Table's name
        db_table = "Product"

    def __str__(self) -> str:
        return self.name

    def to_json(self):
        item = model_to_dict(self)
        item['id'] = self.id
        item['text'] = self.name
        item['category'] = self.category.name
        item['quantity'] = 1
        item['total_product'] = 0
        return item