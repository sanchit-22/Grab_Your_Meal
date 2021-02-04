from django.contrib import admin
from django.urls import path,include
from Canteen import views
urlpatterns = [
    path('', views.canteen_login, name='canteen'),
    path('validate_login', views.validateLoginCanteen, name='validate_login'),
    path('home', views.homeCanteen, name='home'),
    path('additem',views.additem, name='additem'),
    path('removeitem',views.removeitem, name='removeitem'),
    path('todaysmenu',views.todaysmenu, name='todaysmenu'),
    path('canteen_logout',views.canteen_logout, name='logout'),
]