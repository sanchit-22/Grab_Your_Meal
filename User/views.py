from django.shortcuts import render,HttpResponse,redirect
import random
from .models import student
from Canteen.models import add_item
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
from collections import defaultdict
from django import template

# Create your views here.
def home(request):
    return render(request,'home/index.html')

def Signup(request):
    return render(request,'signup.html')

def signup_validation(request):
	fname = request.POST.get('fname')
	email = request.POST.get('email')
	number= request.POST.get('number')
	password = request.POST.get('password')

	student_data = student(name = fname,UserEmail = email, password = password, Phoneno=number, is_collegeStudent="NO")
	student_data.save()
	return redirect('/login')

def Login(request):
    return render(request,'login.html')

def validate_login(request):
    if request.method=='POST':
        ID=request.POST.get('username')
        password=request.POST.get('password')
        print(ID)
        print(password)
        try:
            user=student.objects.get(UserEmail__iexact=ID)
        except student.DoesNotExist:
            user = None
        
        if user:
            loginuserpass=user.password
            if loginuserpass==password:
                request.session['userID']=ID
                userid=request.session.get('userID')
                return redirect('/homeUser')
            else:
                return redirect('/login')
        else:
            messages.error(request,"invalid login try again")
            return redirect('/login')
    else:
        return redirect('/login')

def homeUser(request):
    userid=request.session.get('userID')
    try:
        user=student.objects.get(UserEmail__iexact=userid)
    except student.DoesNotExist:
        user = None
    if userid:
        username=user.name
        allitems=add_item.objects.all()
        return render(request,'home/store.html',context={'liste': allitems, 'username':username}) 
        #return HttpResponse("testing")
    else:
        return redirect('/login')

def user_logout(request):
    if 'userID' in request.session:
        del request.session['userID']
        return redirect ('/login')
    else:
        return HttpResponse("404 Bad Request")

def webmail_login(request):
    return render(request,'webmail_login.html')

def webmail_validation(request):
#    get_otp=request.POST.get('OTP')
#    if get_otp:
#        get_email=request.POST['webmail']
#        user=student.objects.get(UserEmail__iexact=get_email)
#        if get_otp==user.otp:
#            return HttpResponse("success")
#        else:
#            return render(request,'enterOTP.html',{ 'webmail' : get_email})
#    else:    
#        email=request.POST['webmail']
#        usr_otp=random.randint(100000,999999)
#        usr_otp=str(usr_otp)
#        try:
#            user=student.objects.get(UserEmail__iexact=email)
#        except student.DoesNotExist:
#            user = None
#        if user!=None and user.is_collegeStudent=="YES":
#            mess=f"Hello,\nYour OTP is {usr_otp}\n"
#            send_mail(
#                "Welcome to GrabYourMeal-Verify your email",
#                mess,
#                settings.EMAIL_HOST_USER,
#                [email],
#                fail_silently=False
#            )
#            user.otp=usr_otp
#            user.save()
#            print(user.otp)
#            return render(request,'enterOTP.html',{ 'webmail' : email})
#            print("fajsfhadsfn")
#        elif user!=None and user.is_collegeStudent=="NO":
#            messages.error(request,'This service is only available for IIITG student in case some difficulty contact canteen manager')
#            return render(request,'webmail_login.html')
#
#        else:
#            messages.error(request,'webmail not correct')
#            return render(request,'webmail_login.html')
    return HttpResponse("not implemented yet")

def ForgotPassword_validation(request):
    print("dfsdffdsf")
    password1="00"
    password2="00"
    get_otp=request.POST.get('OTP')
    password1=request.POST.get('password1')
    password2=request.POST.get('password2')
    email=request.POST.get('webmail')
    if get_otp:
        print("get_otp")
        get_email=request.POST.get('webmail')
        user=student.objects.get(UserEmail__iexact=get_email)
        if get_otp==user.otp:
            context={'webmail' : get_email , 'to_openpassword': True}
            return render(request,'ForgotPassword_validation.html',context)
        else:
            context={'webmail' : get_email , 'to_openotp': True, 'message':"OTP not correct"}
            return render(request,'ForgotPassword_validation.html',context)
    elif password1:
        if password2==password1:
            print("equal")
            get_email=request.POST.get('webmail')
            user=student.objects.get(UserEmail__iexact=get_email)
            user.password=password2
            user.otp="0"
            user.save()
            context={'message': "Your password has been succesfully updated"}
            return redirect('/login')
        elif password1!=password2:
            print("not equal")
            context={'message': "password does not match try again"}
            return redirect('/login')

    else:    
        print("else")
        usr_otp=random.randint(100000,999999)
        print(usr_otp)
        usr_otp=str(usr_otp)
        try:
            user=student.objects.get(UserEmail__iexact=email)
        except student.DoesNotExist:
            user = None
        if user!=None:
            mess=f"Hello,\nYour OTP is {usr_otp}\n"
            print(mess)
            print(type(email))
            msg=EmailMessage('Welcome to GrabYourMeal-Verify your password', mess, to=[email])
            msg.send()
            user.otp=usr_otp
            user.save()
            print(user.otp)
            context={'webmail' : email , 'to_openotp': True}
            return render(request,'ForgotPassword_validation.html',context)
        else:
            messages.error(request,'Email not correct')
            context={'webmail' : email , 'to_openemail': True}
            return render(request,'ForgotPassword_validation.html',context)

def payment_type(request):
    my_orders=request.session.get('userID')
    print(my_orders)
    for key, value in request.session.items():
        print('{} => {}'.format(key, value))
    return render(request,'home/payment_type.html')
