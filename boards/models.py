# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


# Create your models here.
from django.db.models import ImageField
from django.utils.html import format_html


# class UserInfo(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     # head_img = models.ImageField()
#     path =  models.CharField(max_length=255, null=True,blank=True) # 个人目录，所有照片存在里面

# 患者信息
class Person(models.Model):
    name = models.CharField(max_length=255, null=True, verbose_name='姓名')
    nameCode = models.CharField(max_length=20, null=True, blank=True, verbose_name='姓名编码')
    # privateId
    idnum = models.CharField(max_length=30, null=True, blank=True, verbose_name='病历号')
    otherPrivateId = models.CharField(max_length=20, null=True, blank=True)
    birth = models.DateField(null=True, blank=True, verbose_name='生日')
    # linedcare- "birth": "1991-12-07T00:00:00",
    sex = models.IntegerField(null=True, blank=True, verbose_name='性别')  # 男1 女2
    comment_label = models.CharField(max_length=64, null=True, blank=True) # 备注，标签，空格分割

    privateDir = models.CharField(max_length=255, null=True, blank=True) # 个人目录，所有照片存在里面
    comment = models.TextField(max_length=2000, null=True, blank=True)  # 备注
    icon = models.TextField(null=True, max_length=100, blank=True)  # 头像path
    isEnd = models.NullBooleanField(null=True, blank=True)  # 是否结束
    startDate = models.DateTimeField(null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, blank=True)
    creatAt = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    doctor = models.CharField(max_length=20, null=True, blank=True, verbose_name='医生') #  zdl
    doctorId = models.IntegerField(null=True, blank=True)
    officeId = models.IntegerField(null=True, blank=True)
    clinic = models.CharField(null=True, max_length=20, blank=True)

    mobile = models.CharField(max_length=20, null=True, blank=True)
    email = models.CharField(max_length=40, null=True, blank=True)
    occupation = models.CharField(max_length=20, null=True, blank=True)
    qq = models.IntegerField(null=True, blank=True)
    weixin = models.CharField(max_length=40, null=True, blank=True)
    identityCard = models.CharField(max_length=20, null=True, blank=True)
    homeAddress = models.CharField(max_length=50, null=True)

    patientType = models.CharField(max_length=20, null=True, blank=True)
    lastVisit = models.DateTimeField(null=True, blank=True)
    lastDoctorId = models.IntegerField(null=True, blank=True)
    linkedcareId = models.IntegerField(null=True, blank=True)

    isBaiduFaceSaved = models.NullBooleanField(null=True, blank=True) # 百度上传

    def link(self):
	    return format_html(
		    '<a href="/detail/{}"> {}</a>', self.pk, self.pk
	    )

    # "name": "\u738b\u5929\u8212A", "nameCode": null, "sex": 2, "birth": "1991-12-07T00:00:00",
    # "mobile": "\u672c\u4eba:15210957869"
    # "email": null, "occupation": null, "qq": null, "weixin": null,
    #  "identityCard": null, "homeAddress": null,
    # "patientType": "\u666e\u901a"
    # "doctorId": null, "nickName": null, "lastVisit": null, "lastDoctorId": null,
    # "tag": null,

    # doctor = models.ForeignKey(User, related_name='persons',  on_delete=models.SET_NULL)
    # total_post = models.IntegerField(null=True)
    def __str__(self):
        return self.name


# 不同复诊阶段
class Post(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    isFirst = models.NullBooleanField(null=True, blank=True)  # 是否初诊
    isLast = models.NullBooleanField(null=True, blank=True)  # 是否结束照
    type = models.IntegerField(null=False, blank=True, verbose_name='类型序号')
        # 0初诊 9结束 23456...
        # 100以上为linkedcare 导出图像
    upLoadTime = models.DateTimeField(auto_now_add=True, blank=True)
    person = models.ForeignKey('Person', related_name='posts', null=True, on_delete=models.SET_NULL, verbose_name='患者')
    comment = models.TextField(max_length=2000, null=True, blank=True, verbose_name='备注')
    st_ctime = models.IntegerField(null=True, blank=True) # 对应文件夹的创建时间，用于自动导入时的排序
    dir = models.CharField(max_length=255, null=True, blank=True, verbose_name='文件夹')

    def __str__(self):
        return str(self.type)


class Image(models.Model):
    name = models.CharField(max_length=255, null=True)
    path = models.TextField(max_length=100, null=True)  # 存放路径
    thumbnail = models.TextField(max_length=100, null=True)  # 缩略图存放路径
    size_m = models.TextField(max_length=100, null=True)  # 中等尺寸缩略图存放路径
    isAvatar = models.NullBooleanField(null=True)
    upLoadTime = models.DateTimeField(auto_now_add=True)
    person = models.ForeignKey('Person', related_name='images', null=True, on_delete=models.SET_NULL)
    post = models.ForeignKey('Post', related_name='images', null=True, on_delete=models.SET_NULL)
    type = models.TextField(null=True)  # 1正面 2微笑 3侧面 4 56...
    comment = models.TextField(max_length=200, null=True)
    st_ctime = models.IntegerField(null=True) # 对应图像的创建时间，，用于自动导入时的排序

    baiduFaceInfo = models.TextField(max_length=2000, null=True)

    # isRotated = models.BooleanField(null=True)

    def img_div(self):
        return format_html(
            '<img style="width:150px;" src="{}"', self.thumbnail
        )

    def __str__(self):
        return self.path


#
class Tag(models.Model):
    type_choice = (
        (1, '总分类'),
        (2, '水平向'),
        (3, '垂直向'),
        (4, '是否拔牙'),
        (5, '矫治器分类'),
        (6, '活动矫治器'),
        (7, '保持器'),
        (8, '患者类型'),
        (9, '主诉'),
        (101, '未分类'),

    )

    name = models.CharField(max_length=30, unique=True, blank=True, verbose_name='标签')
    type = models.IntegerField(null=False, default=1, blank=True, choices=type_choice,
                               verbose_name='类型')  # 0初诊 9结束 23456...
    comment = models.CharField(max_length=100, blank=True, verbose_name='备注')
    images = models.ManyToManyField(Image, related_name='tags', blank=True)
    persons = models.ManyToManyField(Person, related_name='tags', blank=True, verbose_name='患者')
    # color = models.PositiveSmallIntegerField(blank=True, null=True, choices=color_choice)
    color = models.CharField(max_length=8, blank=True, null=True)

    color_choice = (
        (0, 'green'),
        (1, 'red'),
        (2, 'blue'),
        (3, 'yellow')
    )

    def color_div(self):
        if self.color:
            return format_html(
                '<p style="background-color:{};"> {}</p>', self.color, self.color
            )

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
