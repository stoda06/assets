from django.urls import path
from . import views

urlpatterns = [
    path('', views.asset,name="asset"),
    path('assets/', views.asset,name="asset"),
    path('Laptops_data/', views.Laptops_data,name='Laptops_data'),
    path('Mobile_data/', views.Mobile_data,name='Mobile_data'),
    path('laptop_configuration/', views.laptop_configuration, name='laptop_configuration'),
    path('MAC_Laptops_data/', views.MAC_Laptops_data,name='MAC_Laptops_data'),
]
