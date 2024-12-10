from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('about_us', views.about_us, name='about_us'),
    path('add-book', views.add_book, name='add_book'),
    path('manage/<int:id>/', views.manage_book, name='manage_book'),
    path('logout', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login')
]