from django.urls import path

from . import views

urlpatterns = [
    path('', views.asset, name="asset"),
    path('assets/', views.asset, name="asset_list"),
    path('Laptops_data/', views.Laptops_data, name='Laptops_data'),
    path('Mobile_data/', views.Mobile_data, name='Mobile_data'),
]
