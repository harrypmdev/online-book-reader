from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('about_us/', views.about_us, name='about_us'),
    path('add-book/', views.add_book, name='add_book'),
    path('delete-book/<int:id>/', views.delete_book, name='delete_book'),
    path('delete-profile/', views.delete_profile, name='delete_profile'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('manage/<int:id>/', views.manage_book, name='manage_book'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
]