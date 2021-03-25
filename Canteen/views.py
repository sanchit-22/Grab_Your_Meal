from django.shortcuts import render,HttpResponse,redirect
from django.contrib import messages
from django.contrib import sessions
from datetime import date
from .models import *
from User.models import currentorder
from User.models import previousorder

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
	canteenuserid=request.session.get('canteenuserid') 
	if canteenuserid=='canteen':
		return render(request,'canteen/add_item/add_item.html') 
	else:
		return redirect('canteen')

def adding_item(request):
	name=request.POST.get('name')
	price=request.POST.get('price')
	image=request.FILES.get('image')
	category=request.POST.get('category')
	today=date.today()
	item_data = add_item(item_name = name, is_Available="YES", category=category, price=price, image=image, current_date=today)
	item_data.save()
	
	return redirect('/canteen/home')

def homeCanteen(request):
	canteenuserid=request.session.get('canteenuserid') 
	if canteenuserid=='canteen':
		all_orders=currentorder.objects.all()
		for i in all_orders:
			print(i.order_detail)
		return render(request,'canteen/home.html',{'text':all_orders}) 
	else:
		return redirect('canteen')

def removeitem(request):
	if request.method=='POST':
		idd=request.POST.get('id')
		add_item.objects.filter(id=idd).delete()
	all_items=add_item.objects.all()
	return render(request,'canteen/removeitem.html',context={'liste':all_items})

def todaysmenu(request):
	canteenuserid=request.session.get('canteenuserid')
	allitems=add_item.objects.all()
	return render(request,'canteen/todaymenu/menu.html',context={'liste': allitems, 'canteenuserid': canteenuserid})
	
def canteen_logout(request):
	if 'canteenuserid' in request.session:
		del request.session['canteenuserid']
		return redirect ('/canteen')
	else:
		return HttpResponse("404 Bad Request")

def order_delivered(request):
	idd=request.POST.get('id')
	print("id=")
	print(idd)
	try:
		user=currentorder.objects.get(id__iexact=idd)
	except currentorder.DoesNotExist:
		user = None
	p_id=user.id
	p_todays_id=user.todays_id
	p_usermail=user.usermail
	p_totalcost=user.totalcost
	p_payment_method=user.payment_method
	p_delivery_status=user.delivery_status
	p_Date=user.Date
	p_Username=user.Username
	p_UserRollno=user.UserRollno
	p_order_detail=user.order_detail
	previousorder_data=previousorder(id=p_id, todays_id=p_todays_id, usermail=p_usermail, totalcost=p_totalcost, payment_method=p_payment_method, delivery_status=p_delivery_status, Date=p_Date, Username=p_Username, UserRollno=p_UserRollno, order_detail=p_order_detail)
	previousorder_data.save()
	todelete=currentorder.objects.filter(id=idd).delete()
	return redirect('/canteen/home')