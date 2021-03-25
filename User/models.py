from __future__ import unicode_literals
from djongo import models
from bson.objectid import ObjectId
# Create your models here.
class student(models.Model):
	name=models.CharField(max_length=20,null=False)
	password=models.CharField(max_length=20,null=False)
	Phoneno=models.CharField(max_length=20,null=False)
	UserEmail=models.CharField(max_length=50,null=False)
	Payment_due=models.CharField(max_length=10, null=True)
	otp=models.CharField(max_length=10, null=True)
	is_collegeStudent=models.CharField(max_length=3,null=False)
	objects=models.DjongoManager()
	def __str__(self):
		return self.name

class currentorder(models.Model):
	id= models.CharField(max_length=20,primary_key=True, serialize=False)
	todays_id=models.CharField(max_length=20,null=False)
	usermail=models.CharField(max_length=50,null=False)
	totalcost=models.CharField(max_length=50,null=False)
	payment_method=models.CharField(max_length=50,null=False)
	delivery_status=models.CharField(max_length=50,null=False)
	Date=models.CharField(max_length=50,null=True)
	Username=models.CharField(max_length=50,null=False)
	UserRollno=models.CharField(max_length=50,null=True)
	order_detail=models.JSONField()
	def __str__(self):
		return self.Username

class previousorder(models.Model):
	id= models.CharField(max_length=20,primary_key=True, serialize=False)
	todays_id=models.CharField(max_length=20,null=False)
	usermail=models.CharField(max_length=50,null=False)
	totalcost=models.CharField(max_length=50,null=False)
	payment_method=models.CharField(max_length=50,null=False)
	delivery_status=models.CharField(max_length=50,null=False)
	Date=models.CharField(max_length=50,null=True)
	Username=models.CharField(max_length=50,null=False)
	UserRollno=models.CharField(max_length=50,null=True)
	order_detail=models.JSONField()
	def __str__(self):
		return self.Username