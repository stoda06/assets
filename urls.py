from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from rest_framework.authtoken.views import ObtainAuthToken

urlpatterns = [
    #path('your_api/', views.YourApiView.as_view(), name='your_api'),
    path('', views.asset, name="asset"),
    path('assets/', views.asset, name="asset"),
    path('start_vm/', views.start_vm, name='start_vm'),
    path('Laptops_data/', views.Laptops_data, name='Laptops_data'),
    #path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('Mobile_data/', views.Mobile_data, name='Mobile_data'),
    #path('laptop_configuration/', views.laptop_configuration, name='laptop_configuration'),
    #path('MAC_Laptops_data/', views.MAC_Laptops_data, name='MAC_Laptops_data'),
    #path('add_system_info/', views.add_system_info, name='add_system_info'),
    #path('api-token-auth/', ObtainAuthToken.as_view(), name='api-token-auth'),
   # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    #path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]

