from django.contrib import admin
from .models import ToDoList, item

# Register your models here.
admin.site.register(ToDoList)
admin.site.register(item)
