from django.shortcuts import render, redirect
from django.http import HttpResponse  # Bu satırı ekleyin!
from .models import EtiketTasarim
from .forms import EtiketTasarimForm
from .utils import tasarimi_tspl_cevir  # Fonksiyonu içe aktarıyoruz

def tasarim_anasayfa(request):
    # Örnek: Basit bir HttpResponse döndürür.
    return HttpResponse("Tasarım Ana Sayfası")

def tasarim_olustur(request):
    if request.method == 'POST':
        form = EtiketTasarimForm(request.POST)
        if form.is_valid():
            tasarim = form.cleaned_data['tasarim']
            tspl_tasarim = tasarimi_tspl_cevir(tasarim)
            form.instance.tasarim = tspl_tasarim
            form.save()
            return redirect('tasarim_listesi')
    else:
        form = EtiketTasarimForm()
    return render(request, 'tasarim/tasarim_olustur.html', {'form': form})

def tasarim_listesi(request):
    tasarimlar = EtiketTasarim.objects.all()
    return render(request, 'tasarim/tasarim_listesi.html', {'tasarimlar': tasarimlar})
