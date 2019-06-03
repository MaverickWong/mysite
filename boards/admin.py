# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *

# Register your models here.
import sys;

# reload(sys);
# sys.setdefaultencoding("utf8")


class PersonAdmin(admin.ModelAdmin):
	list_display = ('name', 'link', 'idnum', 'post_num', 'privateDir', 'doctor', 'birth', 'sex', 'comment', 'get_tags',)
	search_fields = ('name', 'idnum',)
    list_filter = ('last_updated',)
    date_hierarchy = 'last_updated'
    ordering = ('-last_updated',)
    fields = ('name', 'idnum', 'privateDir', 'nameCode', 'isEnd','startDate','mobile','occupation','birth', 'sex', 'comment', 'doctor')

    def post_num(self, obj):
        #  统计post数目
        return str(obj.posts.count())

    post_num.short_description = '上传次数'

    def sex(self, obj):
        if obj.sex == 1:
            return '男'
        if obj.sex == 2:
            return '女'

    sex.short_description = '性别'

    def get_tags(self, obj):
        tags = ''
        for t in obj.tags.all():
            tags = t.name + ', ' + tags
        return tags
    get_tags.short_description = '标签'
    # get_tags.admin_order_field = 'person__tag'


class PostAdmin(admin.ModelAdmin):
	list_display = ('person', 'type', 'upLoadTime', 'name', 'isFirst', 'comment')
    raw_id_fields = ('person',)
    search_fields = ('person__name','name', 'type')  # 搜索外健时指明外键的field


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'comment','type', )
    # filter_horizontal = ('images','persons')
    fields = ('name', 'type', 'comment',)
    search_fields = ('name', 'type')
    ordering = ('type',)


class ImageAdmin(admin.ModelAdmin):
    search_fields = ('name','path')
    list_display = ('person', 'name', 'type','comment','path','post', 'img_div')
    raw_id_fields = ('person',)


# admin.site.register(Board)
admin.site.register(Person, PersonAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Tag, TagAdmin)