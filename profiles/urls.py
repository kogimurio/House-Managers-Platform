from django.urls import path
from.import views

urlpatterns = [
    path('profile/',views.profileView, name='employee'),
]