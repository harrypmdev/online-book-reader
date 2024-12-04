from . import views
from django.urls import path

urlpatterns = [
    path('', views.about_us, name='about_us'),
    path('register/', views.register, name='register'),
]