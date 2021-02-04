from django.shortcuts import render,HttpResponse,redirect
from django.contrib import messages
from django.contrib import sessions
# Create your views here.

def canteen_login(request):
    return render(request,'canteen/login.html')

def validateLoginCanteen(request):
    if request.method=='POST':
        ID="canteen"
        password="1234"
        loginuserid=request.POST['loginuserid']
        loginuserpass=request.POST['loginuserpass']
        if loginuserid==ID and loginuserpass==password:
            request.session['canteenuserid']='canteen'
            canteenuserid=request.session.get('userid')
            return redirect('/canteen/home')
        else:
            messages.error(request,"invalid login try again")
            return redirect('/canteen')
    else:
        return redirect('/canteen')

def additem(request):
    return HttpResponse("this is Additem page")

def homeCanteen(request):
    canteenuserid=request.session.get('canteenuserid') 
    if canteenuserid=='canteen':
        return render(request,'canteen/home.html',{'canteenuserid': canteenuserid}) 
    else:
        return redirect('canteen')

def removeitem(request):
    return HttpResponse("this is remove item page")

def todaysmenu(request):
    return HttpResponse("this is todaysmenu page")
    
def canteen_logout(request):
    if 'canteenuserid' in request.session:
        del request.session['canteenuserid']
        return redirect ('/canteen')
    else:
        return HttpResponse("404 Bad Request")
