from django.urls import path
from .import views

urlpatterns = [
    path('registration/', views.registerView, name='register'),
    path('login/', views.loginView, name='login'),
]