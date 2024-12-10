from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='about_us'),
    path('add-book', views.add_book, name="add_book"),
    path('home/', views.home, name='home'),
    path('logout', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login')
]