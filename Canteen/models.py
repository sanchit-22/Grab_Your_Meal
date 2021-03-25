from __future__ import unicode_literals
from djongo import models
from bson.objectid import ObjectId

# Create your models here.
class add_item(models.Model):
    _id = ObjectId()
    item_name=models.CharField(max_length=20,null=False)
    category=models.CharField(max_length=50,null=False)
    is_Available=models.CharField(max_length=3,null=False)
    price=models.CharField(max_length=5,default=0)
    current_date=models.DateField()
    image=models.ImageField(upload_to="shop/images", default="shop/images")
    objects=models.DjongoManager()
    def __str__(self):
        return self.item_name