from django.contrib import admin
from django.urls import path,include
from User import views
from Canteen import views as C_views
urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.Signup, name='signup'),
    path('signup_validation', views.signup_validation, name='signup_validation'),
    path('login/', views.Login, name='login'),
    path('canteen/', include('Canteen.urls')),
    path('login/webmail_login',views.webmail_login, name="webmail_login"),
    path('webmail_validation',views.webmail_validation, name="webmail_validation"),
    path('ForgotPassword_validation',views.ForgotPassword_validation, name="ForgotPassword_validation"),
    path('login/validate_login', views.validate_login, name='validate_login'),
    path('homeUser', views.homeUser, name='homeUser'),
    path('user_logout', views.user_logout, name='user_logout'),
    path('homeUser/payment_type/', views.payment_type, name='payment_type'),
    #path('login/ForgotPassword',views.ForgotPassword, name="ForgotPassword"),
    
]