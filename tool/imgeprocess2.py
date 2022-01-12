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
from mysite.settings import  BASE_DIR

# 取出所有Image后，检查image的path，及thumbnail，size_m，
# 如果没有，则制作缩略图

# /home/zdl/mysite2/static/picture/a正畸患者照片
base = BASE_DIR
# base = "/home/zdl/mysite2"
# base = "/Users/wcy/Documents/mysite2"

# /Volumes/张栋梁病例照片/正畸患者照片/唇侧正畸/A/
# dir = "/static/picture/老硬盘照片"
dir = "/static/picture/a正畸患者照片"
path = base+ dir

# log
error = []
imgAddIcon =[]
dels = []


def processImg(img, base=base):
    """
    为img对象生成缩略图
    :param img: boards.Image对象
    :param base: mysite地址
    :return: 无
    """
    try:
        # 图像名
        img_path = img.path
        if not img_path[0] == '/':
            img_path = '/' + img_path
        img_path= base + img.path

        if os.path.exists(img_path):

            imgName= img_path.split('/')[-1]  # 赵云.p0.0186202.jpg
            # if imgName[0] == '.':
            #         dels.append(str(img.pk))
            #         print("删除 "+ str(img.pk))
            #
            #         img.delete()
            #         continue

            # 图像的目录
            # img_post  = img.post # TODO warnning 默认img已经有post信息，此处可能出错
            # post_path = base + img_post.dir
            post_path = base + '/'+ img.person.privateDir

            small_path = post_path + 'small'+ '_'+ imgName
            medium_path = post_path + 'medium'+ '_'+ imgName

            # 制作缩略图函数
            if not img.thumbnail:
                im = Image2.open(img_path)
                size = (400, 400)
                if im:
                # im = Image.open(infile)
                    im.thumbnail(size)
                    im.save(small_path, "JPEG")
                    small_path2 = small_path.replace(base, '')
                    if small_path2[0] == '/':
                        img.thumbnail = small_path2
                    else:
                        img.thumbnail = '/'+ small_path2
                    img.save()
                    imgAddIcon.append(img.pk)

            if not img.size_m:
                im = Image2.open(img_path)
                sizem = (1200, 1200)
                if im:
                    im.thumbnail(sizem)
                    im.save(medium_path, "JPEG")
                    medium_path2 = medium_path.replace(base, '')
                    # medium_path2 = medium_path2.replace('//', '/')
                    if medium_path2[0] == '/':
                        img.size_m = medium_path2
                    else:
                        img.size_m = '/'+ medium_path2
                    img.save()
                    print('成功制作缩略图：' + img.path + '\n')

            # 检查开头是否有 '/'，如果没有，则添加
            # if not img.thumbnail[0] == '/':
            #     img.thumbnail = '/' + img.thumbnail
            #     img.save()
            # if not img.size_m[0] == '/':
            #     img.size_m = '/' + img.size_m
            # if not img.path[0] == '/':
            #     img.path = '/' + img.path
            #     img.save()

    except:
        error.append(img.pk)



def allPic():
    imgs = Image.objects.all().order_by('-pk')
    total = imgs.count()
    i = 0
    for img in imgs:
        i=i+1
        img_path = base + img.path
        if os.path.exists(img_path):

            imgName = img_path.split('/')[-1]  # 赵云.p0.0186202.jpg
            # 如果该文件开头为。则退出循环
            if imgName[0] == '.':
                dels.append(str(img.pk))
                print("删除 " + str(img.pk))

                img.delete()
                continue

        processImg(img)
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
            f.write(str(d) + '\n')

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


if __name__=='__main__':
    allPic()
