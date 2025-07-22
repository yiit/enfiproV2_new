from django.contrib import admin
from .models import Sale, SaleDetail, PrintLog

# Mevcut modelleri kayıt edin
admin.site.register(Sale)
admin.site.register(SaleDetail)

# PrintLog modeli için özelleştirilmiş admin arayüzü
@admin.register(PrintLog)
class PrintLogAdmin(admin.ModelAdmin):
    list_display = (
        'timestamp', 'user', 'customer_name1', 'product_name', 'weight', 'file_path'
    )
    search_fields = ('user__username', 'customer_name1', 'product_name', 'weight')
