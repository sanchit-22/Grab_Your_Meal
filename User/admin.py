from django.contrib import admin

from .models import student
from .models import currentorder
from .models import previousorder
from .models import cart
# Register your models here.

admin.site.register(student)
admin.site.register(currentorder)
admin.site.register(previousorder)
admin.site.register(cart)