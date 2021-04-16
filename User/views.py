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
from .models import cart
from django.core.exceptions import ObjectDoesNotExist
from .models import cart
from .models import previousorder
from .models import currentorder
from datetime import date
import string 
from Canteen.models import cashorder
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def home(request):
	return render(request,'user/index.html')

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
		print(allitems)
		print("sdfsdfsf")
		currentorder_id=1
		current_order=currentorder.objects.all()
		for i in current_order:
			max_order_id=int(i.id)
			if max_order_id>currentorder_id:
				currentorder_id=max_order_id
			print(i.id)
		print(currentorder_id)
		previousorder_id=1
		previous_order=previousorder.objects.all()
		for i in previous_order:
			max_order_id=int(i.id)
			if max_order_id>previousorder_id:
				previousorder_id=max_order_id
			print(i.id)
		print(previousorder_id)
		return render(request,'user/store.html',context={'liste': allitems, 'username':username, 'currenorder_id':currentorder_id, 'previousorder_id':previousorder_id}) 
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
		userid=request.session.get('userID')
		try:
			user=student.objects.get(UserEmail__iexact=userid)
		except student.DoesNotExist:
			user = None
		username=user.name
		is_collegeStudent=user.is_collegeStudent
		total=request.POST.get('total')
		print("sdfasfsf")
		print(total)
		college=0
		if is_collegeStudent=="YES":
			college=1
		context={'college':college, 'username':username, 'total':total}
		return render(request,'user/payment_type.html',context)

def order_history(request):
	userid=request.session.get('userID')
	previous_order=[]
	current_order=[]
	college=0
	try:
		user=student.objects.get(UserEmail__iexact=userid)
	except student.DoesNotExist:
		user = None
	if userid:
		is_collegeStudent=user.is_collegeStudent
		if is_collegeStudent=="YES":
			college=1
		username=user.name
		allitems=add_item.objects.all()
		try:
			all_order=previousorder.objects.all()
		except:
			all_order=None
		for alluser in all_order:
			if alluser.usermail==userid:
				previous_order.append(alluser)
		try:
			all_order=currentorder.objects.all()
		except:
			all_order=None
		for alluser in all_order:
			if alluser.usermail==userid:
				current_order.append(alluser)
		print(current_order)
		context={'username':username, 'previous_order':previous_order, 'user':user, 'college':college, 'current_order':current_order}
	return render(request,'user/order_history.html',context)

def prod_description(request):
	userid=request.session.get('userID')
	foodname=request.POST.get('id')
	print(foodname)
	try:
		user=student.objects.get(UserEmail__iexact=userid)
	except student.DoesNotExist:
		user = None
	if userid:
		username=user.name
		try:
			food=add_item.objects.get(item_name__iexact=foodname)
		except add_item.DoesNotExist:
			food = None
		print(food)
		if food:    
			context={'username':username, 'food':food}
			return render(request,'user/prod_description.html',context)
		else:
			return HttpResponse("some error")
	return redirect('/login')

def view_cart(request):
	userid=request.session.get('userID')
	pie=[]
	try:
		user=student.objects.get(UserEmail__iexact=userid)
	except student.DoesNotExist:
		user = None
	if userid:
		username=user.name
		try:
			cart_item=cart.objects.get(user_id__iexact=userid)
		except ObjectDoesNotExist:
			cart_item = None
		if cart_item:
			res=cart_item.itemName
			res2=cart_item.itemQuantity
			print(res)
			print(res2)
			for item_name_list,item_quantity_list in zip(res,res2):
				for name,quantity in zip(res[item_name_list],res2[item_quantity_list]):
					try:
						obj=add_item.objects.get(item_name__iexact=name)
						setattr(obj, "quantity", quantity)
						print(obj.quantity)
						pie.append(obj)
					except ObjectDoesNotExist:
						obj=None
			context={'username':username, 'cart_item':pie}
		else:
			cart_item_empty=1
			context={'username':username,'cart_item_empty':cart_item_empty}
		return render(request,'user/cart.html',context)
	else:
		return redirect('/login')

def add_itemtocart(request):
	item=request.POST.get('item')
	quantity=request.POST.get('quantity')
	quantity_int=int(quantity)
	if quantity_int>0:
		print(item)
		print(quantity)
		userid=request.session.get('userID')
		try:
			user=student.objects.get(UserEmail__iexact=userid)
		except student.DoesNotExist:
			user = None
		if userid:
			username=user.name
			try:
				cart_item=cart.objects.get(user_id__iexact=userid)
			except ObjectDoesNotExist:
				cart_item = None
			if cart_item:
				pie=[]
				res=cart_item.itemName
				res2=cart_item.itemQuantity
				print(res)
				print(res2)
				for item_name_list,item_quantity_list in zip(res,res2):
					print(res[item_name_list])
					print(res2[item_quantity_list])
					res[item_name_list].append(item)
					res2[item_quantity_list].append(quantity)
					print(res[item_name_list])
					print(res2[item_quantity_list])
				json={'item_name':res[item_name_list]}
				json2={'item_quantity':res2[item_quantity_list]}
				print(json)
				second=cart(user_id=userid, itemName=json, itemQuantity=json2)
				second.save()
				context={'username':username}
			elif not cart_item:
				list1=[]
				list2=[]
				list1.append(item)
				list2.append(quantity)
				json={'item_name':list1}
				json2={'item_quantity':list2}
				second=cart(user_id=userid, itemName=json, itemQuantity=json2)
				second.save()
				return HttpResponse("successfully added go to the Cart to order")
		else:
			return redirect('/login')
	else:
		return redirect('/homeUser')
	return HttpResponse("successfully added go to the Cart to order")

def pay(request):
	userid=request.session.get('userID')
	try:
		user=student.objects.get(UserEmail__iexact=userid)
	except student.DoesNotExist:
		user = None
	username=user.name
	userrollno=user.UserRollno
	type_pay=request.POST.get('type')
	total=request.POST.get('total')
	print(type_pay)
	item_list=request.session.get('item_list')
	quantity_list=request.session.get('item_quantity')
	price_list=request.session.get('item_price')
	json={'name':item_list, 'cost':price_list, 'Quantity':quantity_list}
	today=date.today()
	total_pay=int(total)
	if item_list:
		if type_pay=="paylater":
			payment_due=user.Payment_due
			payment_due=int(payment_due)
			payment_due=payment_due+total_pay
			currentorder_id=1
			previousorder_id=1
			current_order=currentorder.objects.all()
			previous_order=previousorder.objects.all()
			for i in current_order:
				max_order_id=int(i.id)
				if max_order_id>currentorder_id:
					currentorder_id=max_order_id
				print(i.id)
			for i in previous_order:
				max_order_id=int(i.id)
				if max_order_id>previousorder_id:
					previousorder_id=max_order_id
				print(i.id)
			currentorder_id=currentorder_id+1
			previousorder_id=previousorder_id+1
			currentorder_id=max(previousorder_id,currentorder_id)
			example=currentorder(id=currentorder_id ,todays_id=currentorder_id, usermail=userid, totalcost=total, payment_method="paylater", delivery_status="no", Date=today, Username=username , UserRollno=userrollno, order_detail=json)
			example.save()
			user.Payment_due=str(payment_due)
			user.save()
			if 'item_list' in request.session:
				del request.session['item_list']
			if 'item_quantity' in request.session:
				del request.session['item_quantity']
			if 'item_price' in request.session:
				del request.session['item_price']
			cart.objects.filter(user_id=userid).delete()
			context={'username':username}
			return render(request,'user/paylater.html',context)


		elif type_pay=="paypal":
			request.session['total']=total
			context={'total':total}
			return render(request,'user/paypal.html',context)

		elif type_pay=="cash":
			letters = string.ascii_letters
			letters=''.join(random.choice(letters) for i in range(10))
			print(letters)
			request.session['autogenerate']=letters
			example=cashorder(autogenerated_key=letters ,usermail=userid, totalcost=total, payment_method="CASH", delivery_status="no", Date=today, Username=username , UserRollno=userrollno, order_detail=json)
			example.save()
			context={'autogenerate':letters,'username':username}
			if 'item_list' in request.session:
				del request.session['item_list']
			if 'item_quantity' in request.session:
				del request.session['item_quantity']
			if 'item_price' in request.session:
				del request.session['item_price']
			cart.objects.filter(user_id=userid).delete()
			return render(request,'user/cash.html',context)
		else:
			return redirect('/homeUser')
	else:
		return redirect('/homeUser')

def checkout(request):
		userid=request.session.get('userID')
		try:
			user=student.objects.get(UserEmail__iexact=userid)
		except student.DoesNotExist:
			user = None
		username=user.name
		is_collegeStudent=user.is_collegeStudent
		college=0
		if is_collegeStudent=="YES":
			college=1
		item_list=[]
		item_quantity=[]
		total=0
		item_list=request.POST.getlist('item_list[]')
		item_quantity=request.POST.getlist('item_quantity[]')
		d = {}
		l = len(item_list)
		for i in range(0,l):
			key = item_list[i]
			val = int(item_quantity[i])
			if val==0:
				continue
			if item_list[i] in d:
				d[key] = val + d[key]
			else:
				d[key] = val

		item_list = d.keys()
		item_quantity = d.values()

		#updated list 
		print(item_list)
		print(item_quantity)
		list_item=[]
		list_quantity=[]
		list_price=[]
		for item,quantity in zip(item_list,item_quantity):
			try:
				item_object=add_item.objects.get(item_name__iexact=item)
			except item_object.DoesNotExist:
				item_object=None
			price=item_object.price
			list_item.append(item)
			list_quantity.append(quantity)
			list_price.append(price)
			quantity=int(quantity)
			total=total+quantity*(int(price))
		request.session['item_list']=list_item
		request.session['item_quantity']=list_quantity
		request.session['item_price']=list_price
		print(total)
		context={'college':college, 'price':total, 'username':username}
		return render(request,'user/checkout.html',context)

def ordercompleted(request):
	userid=request.session.get('userID')
	try:
		user=student.objects.get(UserEmail__iexact=userid)
	except student.DoesNotExist:
		user = None
	username=user.name
	userrollno=user.UserRollno
	type_pay=request.POST.get('type')
	total=request.session.get('total')
	print(type_pay)
	item_list=request.session.get('item_list')
	quantity_list=request.session.get('item_quantity')
	price_list=request.session.get('item_price')
	json={'name':item_list, 'cost':price_list, 'Quantity':quantity_list}
	today=date.today()
	total_pay=int(total)
	currentorder_id=1
	previousorder_id=1
	current_order=currentorder.objects.all()
	previous_order=previousorder.objects.all()
	for i in current_order:
		max_order_id=int(i.id)
		if max_order_id>currentorder_id:
			currentorder_id=max_order_id
		print(i.id)
	for i in previous_order:
		max_order_id=int(i.id)
		if max_order_id>previousorder_id:
			previousorder_id=max_order_id
		print(i.id)
	currentorder_id=currentorder_id+1
	previousorder_id=previousorder_id+1
	currentorder_id=max(previousorder_id,currentorder_id)
	example=currentorder(id=currentorder_id ,todays_id=currentorder_id, usermail=userid, totalcost=total, payment_method="CARD", delivery_status="no", Date=today, Username=username , UserRollno=userrollno, order_detail=json)
	example.save()
	if 'item_list' in request.session:
		del request.session['item_list']
	if 'item_quantity' in request.session:
		del request.session['item_quantity']
	if 'item_price' in request.session:
		del request.session['item_price']
	cart.objects.filter(user_id=userid).delete()
	return redirect('/homeUser')