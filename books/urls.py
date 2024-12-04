from . import views
from django.urls import path

urlpatterns = [
    path('', views.about_us, name='about_us'),
    path('logout', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name="login")
]