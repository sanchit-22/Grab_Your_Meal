from django.shortcuts import render,HttpResponse

# Create your views here.
def home(request):
    return render(request,'home/index.html')

def Signup(request):
    return HttpResponse("this is Signup page")

def Login(request):
    return HttpResponse("this is Login page")

def Canteen(request):
    return HttpResponse("this is canteen login page")

