from django.urls import path
from accounts.views import UserLoginView, UserRegisterView, deshBoard, logout
from django.contrib.auth import views 
app_name='accounts'

urlpatterns = [
    # Authentication
    path('login/',UserLoginView.as_view(),name='auth-login'),# Auth-Login
    path('register/',UserRegisterView.as_view(), name='auth-register'),# Auth-Register
    path('dashboard/',deshBoard, name='dashboard'),# Auth-Register
    path('logout/',logout, name='logout'),# Auth-Register
]