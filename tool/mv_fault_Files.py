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
import re,shutil
from PIL  import Image as Image2
from datetime import datetime

# 取出所有Image后，检查image的path,有一批path因为遗漏'/'导致目录出现错误，此脚本改正path错误，
#

# /home/zdl/mysite2/static/picture/a正畸患者照片
base = "/home/zdl/mysite2"

# base = "/Users/wcy/Documents/mysite2"
# /Volumes/张栋梁病例照片/正畸患者照片/唇侧正畸/A/
# dir = "/static/picture/老硬盘照片"
dir = "/static/picture/a正畸患者照片"

zdldir = "/static/picture/zdl"
# path = base+ dir
#


error=[]
added =[]
dels =[]


imgs = Image.objects.all().order_by('-pk')
total = imgs.count()
i = 0
for img in imgs:
    i=i+1
    try:
        # 贮备图像名
        img_path = img.path
        person = img.person

        # 检查img路径里是否含有 a正畸患者，如果有则不动这个
        if 'a正畸患者' in img_path:
            continue
        elif "/static/picture/zdl" in img_path:
            continue
        else:  # 没有，则改变到 zdl文件夹
            img_path = img_path.replace('/static/picture', zdldir)
            img.path = img_path
            img.thumbnail = img.thumbnail.replace('/static/picture', zdldir)
            img.size_m = img.size_m.replace('/static/picture', zdldir)
            img.save()

            pdir = person.privateDir
            new = pdir.replace('/static/picture', zdldir)
            person.privateDir = new
            person.save()

            added.append(img_path)

    except:
        error.append(str(img.pk))

    try:
        print('进度：' + str(i*100/total) + '%\n')
    except:
        pass



# error=[]
# added =[]
# dels =[]
#
#
# imgs = Image.objects.all().order_by('-pk')
# total = imgs.count()
# i = 0
# for img in imgs:
#     i=i+1
#     try:
#         # 贮备图像名
#         img_path = img.path
#         person = img.person
#
#         #  # 检查开头是否有 '/'
#         if not img_path[0] == '/':
#             if not os.path.exists(base + '/' + img_path):
#                 continue
#         else:
#             if not os.path.exists(base + img_path):
#                 continue
#
#         fullname = img_path.split('/')[-1]
#         index = fullname.count(person.name)
#         if index > 1:
#             privdir = person.privateDir
#             if privdir[0] == '/':  # 检查开头是否有 '/'，如果有，则去除
#                 privdir = privdir[1:]
#                 person.privateDir = privdir
#                 person.save()
#                 # icondir = dir  + 'small' + '/'
#             if not privdir[-1] == '/':  # 检查末尾是否有 '/'，如果没有，添加
#                 privdir = privdir + '/'
#                 person.privateDir = privdir
#                 person.save()
#
#             if not img_path[0] == '/':  # 检查开头是否有 '/'
#                 img_path = '/' + img_path
#             img_path = base + img_path
#
#             if os.path.exists(img_path):
#                 pnme_in_pdir = privdir.split('/')[-2]
#                 old_imgName = img_path.split('/')[-1]  # 赵云赵云.p0.0186202.jpg   或者  赵云small
#                 new_imgnme = old_imgName
#
#                 new_path = base + '/' + privdir + new_imgnme
#                 print('移动\n')
#                 print(img_path + '\n' + new_path)
#                 shutil.move(img_path, new_path)
#                 if os.path.exists(new_path):
#                     img.path = new_path.replace(base, '')
#                     img.save()
#
#                 added.append(img_path)
#
#
#     except:
#         error.append(str(img.pk))
#
#     try:
#         print('进度：' + str(i*100/total) + '%\n')
#     except:
#         pass
#


print('\n完成，正在生成log文件。。。。')


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
    f.write('总计：' + str(len(added)) + '\n')
    for d in added:
        f.write(str(d) + '\n')

    # f.write('\n\n\n删除******************************************\n')
    # # f.write('name' + ' ' + 'id' + ' ' + 'path' + '\n')
    # f.write('总计：' + str(len(dels)) + '\n')
    # for d in dels:
    #     f.write(str(d) + '\n')

print('\n完成。。。。')
