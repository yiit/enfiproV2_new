from django.urls import path
from . import views


app_name = "sales"
urlpatterns = [
    # List sales
    path('', views.sales_list_view, name='sales_list'),
    # Add sale
    path('add', views.sales_add_view, name='sales_add'),
    # Details sale
    path('details/<str:sale_id>',
         views.sales_details_view, name='sales_details'),
    # Sale receipt PDF
    path("pdf/<str:sale_id>",
         views.receipt_pdf_view, name="sales_receipt_pdf"),

    path('print/', views.print_file, name='print_file'),
    path('label/', views.print_label, name='print_label'),
    #path('get_products/', views.get_products_by_customer, name='get_products'),
    path('get_products/', views.get_all_products, name='get_products'),
    path('get_product/', views.get_product, name='get_product'),
    path('get_customer_info/', views.get_customer_info, name='get_customer_details'),
    path('logs/', views.print_log_list, name='print_log_list'),
    path('logs/report/', views.print_log_report, name='print_log_report'),
    path('update_adet_gramaj/', views.update_adet_gramaj, name='update_adet_gramaj'),
]
