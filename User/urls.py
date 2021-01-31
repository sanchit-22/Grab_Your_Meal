from django.contrib import admin
from django.urls import path
from User import views
urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.Signup, name='signup'),
    path('login/', views.Login, name='login'),
    path('canteen/', views.Canteen, name='canteen'),
]