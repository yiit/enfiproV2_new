from django.urls import path
from . import views

app_name = "database"
urlpatterns = [
    path('export-data/', views.export_data, name='export_data'),
    path('import-data/', views.import_data, name='import_data'),
    path('get-models/', views.get_models, name='get_models'),
    path('data-management/', views.data_management, name='data_management'),
    path('update-remote/', views.update_remote, name='update_remote'),
    path('update/', views.update, name='update'),
]
