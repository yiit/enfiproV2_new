from django.db import models
import django.utils.timezone
from customers.models import Customer
from products.models import Product, Category
from django.contrib.auth.models import User


class Sale(models.Model):
    date_added = models.DateTimeField(default=django.utils.timezone.now)
    customer = models.ForeignKey(
        Customer, models.DO_NOTHING, db_column='customer')
    sub_total = models.FloatField(default=0)
    grand_total = models.FloatField(default=0)
    tax_amount = models.FloatField(default=0)
    tax_percentage = models.FloatField(default=0)
    amount_payed = models.FloatField(default=0)
    amount_change = models.FloatField(default=0)

    class Meta:
        db_table = 'Sales'

    def __str__(self) -> str:
        return "Sale ID: " + str(self.id) + " | Grand Total: " + str(self.grand_total) + " | Datetime: " + str(self.date_added)

    def sum_items(self):
        details = SaleDetail.objects.filter(sale=self.id)
        return sum([d.quantity for d in details])


class SaleDetail(models.Model):
    sale = models.ForeignKey(
        Sale, models.DO_NOTHING, db_column='sale')
    product = models.ForeignKey(
        Product, models.DO_NOTHING, db_column='product')
    price = models.FloatField()
    quantity = models.IntegerField()
    total_detail = models.FloatField()

    class Meta:
        db_table = 'SaleDetails'

    def __str__(self) -> str:
        return "Detail ID: " + str(self.id) + " Sale ID: " + str(self.sale.id) + " Quantity: " + str(self.quantity)



class PrintLog(models.Model):
    # Kullanıcı bilgileri
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Kullanıcı")

    # Müşteri bilgileri
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Müşteri")
    customer_name1 = models.CharField(max_length=255, blank=True, null=True, verbose_name="Müşteri Adı 1")
    customer_name2 = models.CharField(max_length=255, blank=True, null=True, verbose_name="Müşteri Adı 2")
    customer_address = models.TextField(blank=True, null=True, verbose_name="Müşteri Adresi")

    # Ürün bilgileri
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Ürün")
    product_category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Ürün Kategorisi")
    product_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Ürün Adı")
    product_code = models.CharField(max_length=255, blank=True, null=True, verbose_name="Ürün Kodu")
    product_barkod = models.CharField(max_length=255, blank=True, null=True, verbose_name="Ürün Barkodu")
    product_stt = models.CharField(max_length=255, blank=True, null=True, verbose_name="Son Tüketim Tarihi")

    # Diğer bilgiler
    #weight = models.CharField(max_length=255, blank=True, null=True, verbose_name="Ağırlık")
    weight = models.FloatField(null=True, blank=True)  # Değiştirilen alan
    topnet = models.CharField(max_length=100, null=True, blank=True)
    custom_text = models.CharField(max_length=255, blank=True, null=True, verbose_name="Özel Metin")
    serial_number = models.CharField(max_length=255, blank=True, null=True, verbose_name="Seri No")
    date_text = models.CharField(max_length=255, blank=True, null=True, verbose_name="Üretim Tarihi")
    time_text = models.CharField(max_length=255, blank=True, null=True, verbose_name="Saat")
    paket_sayisi = models.CharField(max_length=255, blank=True, null=True, verbose_name="Paket Sayısı")
    toplam_paket_sayisi = models.CharField(max_length=255, blank=True, null=True, verbose_name="Toplam Paket Sayısı")

    # Mesajlar ve içerik
    msg1 = models.TextField(blank=True, null=True, verbose_name="Mesaj 1")
    msg2 = models.TextField(blank=True, null=True, verbose_name="Mesaj 2")
    msg3 = models.TextField(blank=True, null=True, verbose_name="Mesaj 3")
    msg4 = models.TextField(blank=True, null=True, verbose_name="Mesaj 4")
    msg5 = models.TextField(blank=True, null=True, verbose_name="Mesaj 5")
    msg6 = models.TextField(blank=True, null=True, verbose_name="Mesaj 6")
    msg7 = models.TextField(blank=True, null=True, verbose_name="Mesaj 7")
    msg8 = models.TextField(blank=True, null=True, verbose_name="Mesaj 8")
    msg9 = models.TextField(blank=True, null=True, verbose_name="Mesaj 9")
    icerik = models.TextField(blank=True, null=True, verbose_name="İçerik")

    # Dosya ve zaman bilgileri
    file_path = models.CharField(max_length=255, blank=True, null=True, verbose_name="Dosya Yolu")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Zaman Damgası")

    def __str__(self):
        return f"PrintLog {self.id} - {self.timestamp}"
