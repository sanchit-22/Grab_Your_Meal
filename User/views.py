from django.shortcuts import render,HttpResponse
import random
from .models import student
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request,'home/index.html')

def Signup(request):
    return render(request,'signup.html')

def Login(request):
    return render(request,'login.html')

def webmail_login(request):
    return render(request,'webmail_login.html')

def webmail_validation(request):
    get_otp=request.POST.get('OTP')
    if get_otp:
        get_email=request.POST['webmail']
        user=student.objects.get(UserEmail__iexact=get_email)
        if get_otp==user.otp:
            return HttpResponse("success")
        else:
            return render(request,'enterOTP.html',{ 'webmail' : get_email})
    else:    
        email=request.POST['webmail']
        usr_otp=random.randint(100000,999999)
        usr_otp=str(usr_otp)
        try:
            user=student.objects.get(UserEmail__iexact=email)
        except student.DoesNotExist:
            user = None
        if user!=None:
            mess=f"Hello,\nYour OTP is {usr_otp}\n"
            send_mail(
                "Welcome to GrabYourMeal-Verify your email",
                mess,
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False
            )
            user.otp=usr_otp
            user.save()
            print(user.otp)
            return render(request,'enterOTP.html',{ 'webmail' : email})
            print("fajsfhadsfn")
        else:
            messages.error(request,'webmail not correct')
            return render(request,'webmail_login.html')
