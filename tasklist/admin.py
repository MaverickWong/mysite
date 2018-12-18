from django.contrib import admin
from tasklist.models import *
# Register your models here.

class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'comment', 'group',)



admin.site.register(Task, TaskAdmin)
