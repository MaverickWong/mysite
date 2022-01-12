#!/usr/bin/python
# -*- coding:utf8 -*-
# 这个一定要，不然会报错，但是错误很明显，容易定位。
import os
from typing import TextIO

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
import django

django.setup()
# django版本大于1.7时需要这两句


from boards.models import *
from datetime import datetime


'''
# 读取所有患者的post总数,记录5个以上的人
# 直接生成网页

# python3 -u /home/zdl/mysite2/readfiles.py
'''


# /home/zdl/mysite2/static/picture/a正畸患者照片
base = "/home/zdl/mysite2"
dir = "/static/picture/a正畸患者照片"

# base = "/Users/wcy/Documents/mysite2"
# # /Volumes/张栋梁病例照片/正畸患者照片/唇侧正畸/A/
# dir = "/static/picture/老硬盘照片"

path = base + dir

all = []

# persons = Person.objects.filter(name__contains='test')
persons = Person.objects.all()

i = 0
for p in persons:
	i = i + 1
	n = p.posts.count()
	if n > 5:
		all.append({'id': p.pk, 'name': p.name, 'num': n})

print('\n正在生成log文件。。。。')

dt = datetime.now()
time2 = dt.strftime("%m%d-%H%M%S")

fname3 = 'log/log_counPostNum' + time2 + '.html'

with open(fname3, 'w+') as f:  # type: TextIO
	f.write('<!DOCTYPE html><html><body>')
	# f.write('\n\n\n成功添加******************************************\n')
	f.write('<table><tr><th>id</th><th>name</th><th>num</th></tr> ')
	# f.write('name' + ' ' + 'id' + ' ' + 'path' + '\n')

	for item in all:
		f.write('<tr><td>%d</td> <td><a href="/detail/%d/"> %s </a></td> <td>%d</td></tr> '
		        % (item['id'], item['id'], item['name'], item['num'] ) )
		f.write('\n')

	f.write('</table></body></html>')
print('\n完成。。。。')
