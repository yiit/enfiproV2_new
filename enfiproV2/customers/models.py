from django.db import models
from products.models import Product ,Category

class Customer(models.Model):
    STATUS_CHOICES = (  # new
        ("ACTIVE", "Aktif"),
        ("INACTIVE", "Pasif")
    )

    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256, blank=True, null=True)
    address = models.TextField(max_length=256, blank=True, null=True)
    email = models.EmailField(max_length=256, blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=100,
        verbose_name="Status of the customer",
    )
    category = models.ForeignKey(Category, related_name="customer_category", on_delete=models.CASCADE, db_column='category')

    class Meta:
        db_table = 'Customers'

    def __str__(self) -> str:
        return self.first_name + " " + self.last_name

    def get_full_name(self):
        return self.first_name 
        #+ " " + self.last_name

    def to_select2(self):
        item = {
            "label": self.get_full_name(),
            "value": self.id
        }
        return item
