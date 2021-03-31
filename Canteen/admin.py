from django.contrib import admin

from .models import add_item
from .models import cashorder
# Register your models here.

admin.site.register(add_item)
admin.site.register(cashorder)