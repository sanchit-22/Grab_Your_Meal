from django.contrib import admin

from .models import student
from .models import currentorder
from .models import previousorder
# Register your models here.

admin.site.register(student)
admin.site.register(currentorder)
admin.site.register(previousorder)
