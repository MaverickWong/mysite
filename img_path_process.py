#!/usr/bin/python
# -*- coding:utf8 -*-
# 这个一定要，不然会报错，但是错误很明显，容易定位。
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
import django
django.setup()
# django版本大于1.7时需要这两句

# python3 -u /home/zdl/mysite2/readfiles.py
#

from boards.models import *
import re
from PIL  import Image as Image2
from datetime import datetime

# 取出所有Image后，检查image的path，及thumbnail，size_m，
# 如果没有，则制作缩略图
#这个版本是按降序处理

# /home/zdl/mysite2/static/picture/a正畸患者照片
base = "/home/zdl/mysite2"

# base = "/Users/wcy/Documents/mysite2"
# /Volumes/张栋梁病例照片/正畸患者照片/唇侧正畸/A/
# dir = "/static/picture/老硬盘照片"
dir = "/static/picture/a正畸患者照片"

path = base+ dir



error=[]
imgAddIcon =[]
dels =[]


imgs = Image.objects.all().order_by('-pk')
total = imgs.count()
i = 0
for img in imgs:
    i=i+1
    try:
        # 图像名


            # 制作缩略图函数
        if not img.thumbnail[0] == '/': #  检查开头是否有 '/'，如果没有，则添加
            img.thumbnail = '/' + img.thumbnail
            img.save()
        if not img.size_m[0] == '/':
            img.size_m = '/'+ img.size_m
        if not img.path[0] =='/':
            img.path = '/'+ img.path


    except:
        error.append(img.pk)

    try:
        print('进度：' + str(i*100/total) + '%\n')
    except:
        pass



print('\n缩略图完成，正在生成log文件。。。。')


dt = datetime.now()
time2 = dt.strftime("%m%d-%H%M%S")

fname3 = 'log/log_iconMake' + time2 + '.txt'
with open(fname3, 'w+') as f:

    f.write('\n错误********************************************\n')
    # f.write('name' + ' ' + 'id' + ' ' + 'path' + '\n')
    f.write('总计：' + str(len(error)) + '\n')
    for d in error:
        f.write(d + '\n')

    f.write('\n\n\n成功添加******************************************\n')
    # f.write('name' + ' ' + 'id' + ' ' + 'path' + '\n')
    f.write('总计：' + str(len(imgAddIcon)) + '\n')
    for d in imgAddIcon:
        f.write(str(d) + '\n')

    f.write('\n\n\n删除******************************************\n')
    # f.write('name' + ' ' + 'id' + ' ' + 'path' + '\n')
    f.write('总计：' + str(len(dels)) + '\n')
    for d in dels:
        f.write(str(d) + '\n')

print('\n完成。。。。')
