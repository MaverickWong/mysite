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
# import re,shutil
# from PIL  import Image as Image2
from datetime import datetime

# 修正privateDir中的问题
#

# /home/zdl/mysite2/static/picture/a正畸患者照片
base = "/home/zdl/mysite2"

# base = "/Users/wcy/Documents/mysite2"
# /Volumes/张栋梁病例照片/正畸患者照片/唇侧正畸/A/
# dir = "/static/picture/老硬盘照片"
dir = "/static/picture/a正畸患者照片"

zdldir = "/static/picture/zdl"
# path = base+ dir
#/static/picture/zdl/zdl/zdl/zdl/zdl/李娜_7416/
error=[]

persons = Person.objects.all()
for p in persons:
    if p.privateDir:
        dir = p.privateDir

        # 去除 zdl重复问题
        if '/zdl/zdl/' in dir:
            print(dir + '\n')
            while '/zdl/zdl/' in dir:
                dir = dir.replace('/zdl/zdl/', '/zdl/')
            p.privateDir = dir
            p.save()

        if dir[0] == '/':
            print(dir +  ' 删除开头'+'\n')
            dir = dir[1:]
            p.privateDir = dir
            p.save()

        if 'zdl' not in dir:
            if 'a正畸患者照片' not in dir:
                try:
                    print(dir + '\n')
                    dir = dir.replace('static/picture', 'static/picture/zdl')
                    p.privateDir = dir
                    p.save()
                except:
                    error.append(str(p.pk))

print('\n完成，正在生成log文件。。。。')


dt = datetime.now()
time2 = dt.strftime("%m%d-%H%M%S")

fname3 = 'log/log_privDir' + time2 + '.txt'
with open(fname3, 'w+') as f:
    f.write('\n错误********************************************\n')
    # f.write('name' + ' ' + 'id' + ' ' + 'path' + '\n')
    f.write('总计：' + str(len(error)) + '\n')
    for d in error:
        f.write(d + '\n')