from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Kullanıcı Adı",
                "class": "form-control form-control-user"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Kullanıcı Şifresi",
                "class": "form-control form-control-user"
            }
        ))

class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Kullanıcı Adı", "class": "form-control"}))
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={"placeholder": "Email", "class": "form-control"}))
    first_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Ad", "class": "form-control"}))
    last_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Soyad", "class": "form-control"}))
    phone_number = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Telefon No", "class": "form-control"}))
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Şifre", "class": "form-control"}))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Şifre Tekrarı", "class": "form-control"}))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserUpdateForm(forms.ModelForm):
    ROLE_CHOICES = [
        ('user', 'Standart Kullanıcı'),
        ('admin', 'Yönetici'),
    ]

    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        label="Rol",
        widget=forms.Select(attrs={"class": "form-control"})
    )

    username = forms.CharField(
        label="Kullanıcı Adı",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Kullanıcı adı"})
    )
    email = forms.EmailField(
        required=False,
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email adresi"})
    )
    first_name = forms.CharField(
        required=False,
        label="Ad",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Ad"})
    )
    last_name = forms.CharField(
        required=False,
        label="Soyad",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Soyad"})
    )
    password1 = forms.CharField(
        required=False,
        label="Yeni Şifre",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Yeni şifre"}),
    )
    password2 = forms.CharField(
        required=False,
        label="Yeni Şifre Tekrarı",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Yeni şifre tekrarı"}),
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mevcut kullanıcı bilgisine göre rolü başlangıçta seç
        if self.instance:
            if self.instance.is_superuser:
                self.fields['role'].initial = 'admin'
            else:
                self.fields['role'].initial = 'user'

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 or password2:
            if password1 != password2:
                raise forms.ValidationError("Şifreler eşleşmiyor.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password1")

        if password:
            user.set_password(password)

        role = self.cleaned_data.get("role")
        if role == 'admin':
            user.is_staff = True
            user.is_superuser = True
        else:
            user.is_staff = False
            user.is_superuser = False

        if commit:
            user.save()
        return user
