from . import views
from django.urls import path

urlpatterns = [
    path('delete-profile/', views.delete_profile, name='delete_profile'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
]