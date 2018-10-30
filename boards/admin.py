# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *

# Register your models here.
import sys;

# reload(sys);
# sys.setdefaultencoding("utf8")

class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'idnum', 'birth', 'sex', 'comment', 'doctor', 'tags')
    search_fields = ('name', 'idnum')
    list_filter = ('last_updated',)
    date_hierarchy = 'last_updated'
    ordering = ('-last_updated',)
    fields = ('name', 'idnum', 'nameCode', 'isEnd','startDate','mobile','occupation','birth', 'sex', 'comment', 'doctor')

    # def get_tags(self, obj):
    #     return obj.tags
    # get_tags.short_description = 'TAG'
    # get_tags.admin_order_field = 'person__tag'


class PostAdmin(admin.ModelAdmin):
    list_display = ('name', 'isFirst','type', 'comment')

class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'comment','type', )
    filter_horizontal = ('images','persons')

# admin.site.register(Board)
admin.site.register(Person, PersonAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Image)
admin.site.register(Tag, TagAdmin)