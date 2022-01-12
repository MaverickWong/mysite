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
from PIL import ExifTags
from mysite.settings import BASE_DIR

# goo
# 取出所有Image后，检查image的方向，调整旋转。
# TODO bug，有些口内照片会被误旋转

# /home/zdl/mysite2/static/picture/a正畸患者照片
base = BASE_DIR

# dir = "/static/picture/老硬盘照片"
# dir = "/static/picture/a正畸患者照片"
# path = base+ dir

error=[]
imgAddIcon =[]
dels =[]


def rotate_img_degree(img, degree):
    ''' 旋转img对象的小图中图，到degree 度数 '''
    # 中图
    mpath = base + img.size_m
    img_m = Image2.open(mpath)
    img_m = img_m.rotate(degree, expand=True)
    img_m.save(mpath, "JPEG")
    # 缩略图
    spath = base + img.thumbnail
    img_s = Image2.open(spath)
    img_s = img_s.rotate(degree, expand=True)
    img_s.save(spath, "JPEG")

    print(img.person)


def rotate_auto_imgs(imgs):
    total = imgs.count()
    i = 0
    for img in imgs:
        # if img.
        i = i + 1
        try:
            img_path = base + img.path  # 图像path
            if os.path.exists(img_path):
                # img.show()
                img2 = Image2.open(img_path)
                try:
                    for orientation in ExifTags.TAGS.keys():
                        if ExifTags.TAGS[orientation] == 'Orientation': break

                    exif = dict(img2._getexif().items())
                    if exif[orientation] == 3:
                        rotate_img_degree(img, 180)

                    elif exif[orientation] == 6:
                        rotate_img_degree(img, 270)

                    elif exif[orientation] == 8:
                        rotate_img_degree(img, 90)

                except:
                    pass

        except:
            error.append(img.pk)

            print('进度：' + str(i) + '/' + str(total) + '\n')

    # print('\n完成。。。。')


if __name__ == '__main__':
    pass
    imgs = Image.objects.filter(type=1)
    rotate_auto_imgs(imgs)

# ['result']['face_list'][0]
'''
{"timestamp": 1554552442, "error_msg": "SUCCESS", "cached": 0, "result": {"face_list": [{"angle": {"roll": 12.89, "yaw": -86.14, "pitch": 10.7}, "face_probability": 0.95, "age": 23, "landmark72": [{"x": 301.88, "y": 451.75}, {"x": 315.33, "y": 512.07}, {"x": 333.73, "y": 573.23}, {"x": 363.77, "y": 632.6}, {"x": 416.33, "y": 686.46}, {"x": 480.79, "y": 718.33}, {"x": 542.41, "y": 727.57}, {"x": 558.61, "y": 679.69}, {"x": 569.46, "y": 635.36}, {"x": 578.11, "y": 589.4}, {"x": 580.77, "y": 541.11}, {"x": 577.93, "y": 493.23}, {"x": 576.23, "y": 445.82}, {"x": 498.2, "y": 453.1}, {"x": 506.13, "y": 444.88}, {"x": 515.57, "y": 439.72}, {"x": 524.33, "y": 440.98}, {"x": 528.82, "y": 452.19}, {"x": 523.47, "y": 457.61}, {"x": 515.45, "y": 459.06}, {"x": 506.7, "y": 457.25}, {"x": 520.3, "y": 448.65}, {"x": 482.65, "y": 411.71}, {"x": 498.42, "y": 394.25}, {"x": 516.55, "y": 385.97}, {"x": 535.33, "y": 387.52}, {"x": 548.98, "y": 405.53}, {"x": 532.98, "y": 403.36}, {"x": 516.45, "y": 403.37}, {"x": 499.69, "y": 405.97}, {"x": 562, "y": 453.4}, {"x": 563.17, "y": 447.28}, {"x": 567.93, "y": 443.65}, {"x": 573.7, "y": 445.75}, {"x": 571.78, "y": 453.25}, {"x": 571.13, "y": 457.14}, {"x": 566.17, "y": 456.64}, {"x": 563.16, "y": 455.75}, {"x": 569.72, "y": 451.17}, {"x": 564.27, "y": 412.7}, {"x": 565.92, "y": 404.32}, {"x": 569.03, "y": 399.17}, {"x": 571.9, "y": 400.59}, {"x": 572.11, "y": 406.79}, {"x": 569.7, "y": 408.55}, {"x": 567.39, "y": 410.19}, {"x": 566.32, "y": 411.65}, {"x": 533.9, "y": 458.38}, {"x": 538.61, "y": 495.57}, {"x": 541.09, "y": 533.14}, {"x": 544.11, "y": 570.1}, {"x": 568.05, "y": 577.08}, {"x": 584.48, "y": 560.52}, {"x": 604.18, "y": 543.01}, {"x": 589.13, "y": 514.16}, {"x": 568.37, "y": 484.92}, {"x": 548.95, "y": 454.8}, {"x": 586.78, "y": 524.91}, {"x": 537.27, "y": 636.81}, {"x": 553.7, "y": 620.58}, {"x": 572.93, "y": 611.67}, {"x": 572.21, "y": 621.76}, {"x": 570.03, "y": 631.51}, {"x": 566.82, "y": 643.54}, {"x": 567.32, "y": 654.24}, {"x": 551.37, "y": 647.97}, {"x": 552.24, "y": 630.48}, {"x": 568.1, "y": 627.5}, {"x": 562.39, "y": 630.47}, {"x": 561.86, "y": 634.29}, {"x": 566.34, "y": 637.07}, {"x": 552.74, "y": 636.36}], "face_token": "74f54e8fc6bd58a8ec9d01c09726be0a", "landmark": [{"x": 520.3, "y": 448.65}, {"x": 569.72, "y": 451.17}, {"x": 586.78, "y": 524.91}, {"x": 561.1, "y": 633.16}], "location": {"top": 385.82, "width": 302, "left": 302.25, "rotation": 0, "height": 341}}], "face_num": 1}, "log_id": 304592845524421141, "error_code": 0}
'''
