# tasarim/forms.py
from django import forms
from .models import EtiketTasarim

class EtiketTasarimForm(forms.ModelForm):
    class Meta:
        model = EtiketTasarim
        fields = ['adi', 'tasarim']