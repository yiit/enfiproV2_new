from django.urls import path
from .views import login_view, register_user, user_list, delete_user, add_user, update_user, check_admin_password
from django.contrib.auth.views import LogoutView

app_name = "authentication"
urlpatterns = [
    path('accounts/login/', login_view, name="login"),
    path('accounts/register/', register_user, name="register"),
    path('accounts/logout/', LogoutView.as_view(), name="logout"),
    path('accounts/user_list/', user_list, name='user_list'),
    path('accounts/add_user/', add_user, name='add_user'),
    path('accounts/delete_user/<int:user_id>/', delete_user, name='delete_user'),
    path('update_user/<int:user_id>/', update_user, name='update_user'),  # Kullanıcı Güncelleme
    # urls.py
    path("check-admin-password/", check_admin_password, name="check_admin_password"),

]