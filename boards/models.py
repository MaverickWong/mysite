# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Person(models.Model):
	name = models.CharField(max_length=255)
	idnum = models.IntegerField(null=True)
	clinic = models.CharField(null=True, max_length=20)
	birth = models.DateField(null=True)
	sex = models.IntegerField(null=True)# 男1 女2
	comment = models.TextField(max_length=2000, null=True)
	icon = models.TextField(null=True, max_length=100)
	isEnd = models.NullBooleanField(null=True)  # 是否结束
	startDate = models.DateTimeField(null=True)
	last_updated = models.DateTimeField(auto_now_add=True)
	# total_post = models.IntegerField(null=True)
	def __str__(self):
		return self.name


# 不同复诊阶段
class Post(models.Model):
	name = models.CharField(max_length=255,null=True)
	isFirst = models.NullBooleanField(null=True)  # 是否初诊
	isLast = models.NullBooleanField(null=True)  # 是否结束照
	type = models.IntegerField(null=False)  # 0初诊 9结束 23456...
	upLoadTime = models.DateTimeField(auto_now_add=True)
	person = models.ForeignKey('Person', related_name='posts')
	comment = models.TextField(max_length=2000, null=True)

	def __str__(self):
		return str(self.type)


class Image(models.Model):
	name = models.CharField(max_length=255,null=True)
	path = models.TextField(max_length=100, null=True)  # 存放路径
	thumbnail = models.TextField(max_length=100, null=True)  # 缩略图存放路径
	isAvatar = models.NullBooleanField(null=True)
	upLoadTime = models.DateTimeField(auto_now_add=True)
	person = models.ForeignKey('Person', related_name='images')
	post = models.ForeignKey('Post', related_name='images')
	type = models.TextField(null=True)  # 1正面 2微笑 3侧面 4 56...
	comment = models.TextField(max_length=2000, null=True)

	def __str__(self):
		return self.path


#
class Tag(models.Model):
	name = models.CharField(max_length=30, unique=True)
	type = models.IntegerField(null=False, default=1)  # 0初诊 9结束 23456...
	comment = models.CharField(max_length=100)
	images = models.ManyToManyField(Image, related_name='tags')
	persons = models.ManyToManyField(Person, related_name='tags')

	def __str__(self):
		return self.name

# class Post(models.Model):
#     message = models.TextField(max_length=4000)
#     topic = models.ForeignKey(Topic, related_name='posts')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(null=True)
#     created_by = models.ForeignKey(User, related_name='posts')
#     updated_by = models.ForeignKey(User, null=True, related_name='+')

#     def __str__(self):
# 		return self.message