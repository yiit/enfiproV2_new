# tasarim/models.py
from django.db import models

class EtiketTasarim(models.Model):
    adi = models.CharField(max_length=255)
    tasarim = models.TextField()  # TSPL formatında tasarım verisi
    olusturulma_tarihi = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.adi