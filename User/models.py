from __future__ import unicode_literals
from djongo import models

# Create your models here.
class student(models.Model):
	name=models.CharField(max_length=20,null=False)
	password=models.CharField(max_length=20,null=False)
	Phoneno=models.CharField(max_length=20,null=False)
	UserEmail=models.CharField(max_length=50,null=False)
	Payment_due=models.CharField(max_length=10, null=True)
	otp=models.CharField(max_length=10, null=True)
	objects=models.DjongoManager()
	def __str__(self):
		return self.name