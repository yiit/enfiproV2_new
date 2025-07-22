import json
from datetime import date
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, FloatField, F
from django.db.models.functions import Coalesce
from django.shortcuts import render
from products.models import Product, Category
from sales.models import Sale

def get_anydesk_id_from_file():
    config_path = "/etc/anydesk/system.conf"
    try:
        with open(config_path, 'r') as f:
            for line in f:
                if line.startswith("ad.anynet.id="):
                    return line.strip().split("=")[1]
    except Exception as e:
        print(f"AnyDesk ID okunamadı: {e}")
    return "Bilinmiyor"


@login_required(login_url="/accounts/login/")
def index(request):
    today = date.today()

    year = today.year
    monthly_earnings = []
    
    anydesk_id = get_anydesk_id_from_file()

    # Calculate earnings per month
    for month in range(1, 13):
        earning = Sale.objects.filter(date_added__year=year, date_added__month=month).aggregate(
            total_variable=Coalesce(Sum(F('grand_total')), 0.0, output_field=FloatField())).get('total_variable')
        monthly_earnings.append(earning)

    # Calculate annual earnings
    annual_earnings = Sale.objects.filter(date_added__year=year).aggregate(total_variable=Coalesce(
        Sum(F('grand_total')), 0.0, output_field=FloatField())).get('total_variable')
    annual_earnings = format(annual_earnings, '.2f')

    # AVG per month
    avg_month = format(sum(monthly_earnings)/12, '.2f')

    # Top-selling products
    top_products = Product.objects.annotate(quantity_sum=Sum(
        'saledetail__quantity')).order_by('-quantity_sum')[:3]

    top_products_names = []
    top_products_quantity = []

    for p in top_products:
        top_products_names.append(p.urun_ismi1)
        top_products_quantity.append(p.quantity_sum)

    print(top_products_names)
    print(top_products_quantity)

    context = {
        "active_icon": "dashboard",
        "products": Product.objects.all().count(),
        "categories": Category.objects.all().count(),
        "annual_earnings": annual_earnings,
        "monthly_earnings": json.dumps(monthly_earnings),
        "avg_month": avg_month,
        "top_products_names": json.dumps(top_products_names),
        "top_products_names_list": top_products_names,
        "top_products_quantity": json.dumps(top_products_quantity),
        "anydesk_code": anydesk_id,
    }
    return render(request, "pos/index.html", context)
