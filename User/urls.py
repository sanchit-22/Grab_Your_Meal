from django.contrib import admin
from django.urls import path,include
from User import views
from Canteen import views as C_views
urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.Signup, name='signup'),
    path('login/', views.Login, name='login'),
    path('canteen/', include('Canteen.urls')),
    
]