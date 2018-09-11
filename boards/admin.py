# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *

# Register your models here.

# admin.site.register(Board)
admin.site.register(Person)
admin.site.register(Post)
admin.site.register(Image)
admin.site.register(Tag)