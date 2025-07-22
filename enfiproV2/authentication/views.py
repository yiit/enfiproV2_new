# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from .forms import LoginForm, SignUpForm
from django.contrib.auth.models import User

from django.http import JsonResponse

from django.contrib.auth import logout


def check_admin_password(request):
    if request.method == "POST":
        password = request.POST.get("password")
        User = get_user_model()
        admin_users = User.objects.filter(is_staff=True)

        for admin in admin_users:
            user = authenticate(username=admin.username, password=password)
            if user:
                return JsonResponse({"success": True})

        return JsonResponse({"success": False})
    
    return JsonResponse({"success": False})



def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                msg = 'Hatalı Kullanıcı Adı yada Şifre!'
        else:
            msg = 'Hata Oluştu!.'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})


def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()  # Kullanıcıyı doğrudan veritabanına kaydeder
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            messages.success(request, 'Kullanıcı başarıyla oluşturuldu. Giriş yapabilirsiniz.', extra_tags="success")
            return redirect('authentication:login')
        else:
            msg = 'Form Hatalı!'
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})

# Kullanıcıları Listeleme
def user_list(request):
    users = User.objects.all()
    return render(request, 'accounts/user_list.html', {'users': users})

# Yeni Kullanıcı Ekleme
from django.contrib import messages  # mesajları göstermek için bu önemli!

def add_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        role = request.POST.get("role")  # 👈 Rol seçimini al

        if form.is_valid():
            user = form.save(commit=False)  # Kaydetme, önce kullanıcıyı al

            # 👇 Role göre yetki ver
            if role == "admin":
                user.is_staff = True
                user.is_superuser = True
            else:
                user.is_staff = False
                user.is_superuser = False

            user.save()  # Yetkileri verdikten sonra kaydet
            messages.success(request, '✅ Yeni kullanıcı başarıyla eklendi.', extra_tags="success")
            return redirect('authentication:user_list')
        else:
            messages.error(request, '❌ Form Hatalı! Lütfen kontrol edin.', extra_tags="danger")
    else:
        form = SignUpForm()

    return render(request, "accounts/add_user.html", {"form": form})



# Kullanıcı Silme
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    messages.success(request, 'Kullanıcı başarıyla silindi.', extra_tags="success")
    return redirect('authentication:user_list')


# Kullanıcı Güncelleme
from .forms import UserUpdateForm

def update_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            role = form.cleaned_data.get('role')  # Rolü al
            user = form.save(commit=False)

            # Role göre yetki ata
            if role == 'admin':
                user.is_staff = True
                user.is_superuser = True
            else:
                user.is_staff = False
                user.is_superuser = False

            user.save()
            messages.success(request, '✅ Kullanıcı başarıyla güncellendi.')
            return redirect('authentication:user_list')
    else:
        form = UserUpdateForm(instance=user)

    return render(request, 'accounts/update_user.html', {'form': form, 'user': user})
