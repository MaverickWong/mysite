#!/usr/bin/python
# -*- coding:utf8 -*-
# 这个一定要，不然会报错，但是错误很明显，容易定位。
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
import django
django.setup()
# django版本大于1.7时需要这两句


from boards.models import *
import re
from PIL  import Image as Image2
from datetime import datetime

#
# 取出所有Image后，检查image的path，及thumbnail，size_m，
# 如果none，则制作缩略图
# 删除'.'开头的非图像文件
#
#


# python3 -u /home/zdl/mysite2/readfiles.py
# /home/zdl/mysite2/static/picture/a正畸患者照片
base = "/home/zdl/mysite2"

# base = "/Users/wcy/Documents/mysite2"
# /Volumes/张栋梁病例照片/正畸患者照片/唇侧正畸/A/
# dir = "/static/picture/老硬盘照片"
dir = "/static/picture"

# path = base+ dir



error=[]
imgAddIcon =[]
dels =[]


imgs = Image.objects.all()
total = imgs.count()
i = 0
for img in imgs:
    i=i+1
    try:
        # 图像名
        img_path= base +  img.path
        if os.path.exists(img_path):
            # 删除.开头的非图像文件
            imgName= img_path.split('/')[-1]  # 赵云.p0.0186202.jpg
            if imgName[0] == '.':
                    dels.append(str(img.pk))
                    print("删除 "+ str(img.pk))

                    img.delete()
                    continue
            # 图像的目录
            img_post  = img.post # TODO warnning 默认img已经有post信息，此处可能出错
            post_path = base + img_post.dir
            if post_path[-1] == '/':
                small_path = post_path+ 'small'+ '_'+ imgName
                medium_path = post_path+ 'medium'+ '_'+ imgName
            else:
                small_path = post_path + '/' + 'small' + '_' + imgName
                medium_path = post_path + '/' + 'medium' + '_' + imgName

            # 制作缩略图函数

            if not img.thumbnail:
                im = Image2.open(img_path)
                size = (400, 400)
                if im:
                # im = Image.open(infile)
                    im.thumbnail(size)
                    im.save(small_path, "JPEG")
                    img.thumbnail = small_path.replace(base, '')
                    img.save()
                    imgAddIcon.append(img.pk)
            if not img.size_m:
                im = Image2.open(img_path)
                sizem = (1200, 1200)
                if im:
                    im.thumbnail(sizem)
                    im.save(medium_path, "JPEG")
                    img.size_m = medium_path.replace(base, '')
                    img.save()
                    print('成功制作缩略图：' + img.path + '\n')

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
