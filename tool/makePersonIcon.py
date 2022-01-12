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
import re, cv2
from PIL  import Image as Image2
from datetime import datetime
import sys
import dlib
from skimage import io
import face_recognition



# 取出所有Image后，检查image的path，及thumbnail，size_m，如果none，则制作缩略图
#这个版本是按降序处理

# /home/zdl/mysite2/static/picture/a正畸患者照片
base = "/home/zdl/mysite2"
dir = "/static/picture/a正畸患者照片"

# base = "/Users/wcy/Documents/mysite2"
# # /Volumes/张栋梁病例照片/正畸患者照片/唇侧正畸/A/
# dir = "/static/picture/老硬盘照片"

path = base+ dir

detector = dlib.get_frontal_face_detector()

error=[]
imgAddIcon =[]
dels =[]

# persons = Person.objects.filter(name__contains='test')
persons = Person.objects.all()
total = persons.count()
# imgs = Image.objects.all().order_by('-pk')

# 先清空所有icon
# for p in persons:
#     if p.icon:
#         print('del' + str(p.pk) + '\n'   )
#         p.icon = ''
#         p.save()

i = 0
for p in persons:
    i = i + 1
    if not p.icon:
        imgs = p.images.all()
        for img in imgs:
            if not p.icon:
                try:
                    img_path = base + img.thumbnail
                    if os.path.exists(img_path):
                        # 读取图片并识别人脸
                        img2 = face_recognition.load_image_file(img_path)
                        faces = face_recognition.face_locations(img2)

                        # imge = io.imread(img_path)
                        # # 使用detector进行人脸检测 dets为返回的结果
                        # dets = detector(img2, 1)

                        if len(faces) > 0:
                            print('\n  ' + str(len(faces)))

                            print('find faces  ' + p.name + '  ' + str(p.pk))
                            p.icon = img_path.replace(base, '')
                            p.save()
                            continue
                        # face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
                        # # Read the image
                        # image = cv2.imread(img_path)
                        # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                        #
                        # # 检测人脸，返回列表faces
                        # faces = face_cascade.detectMultiScale(
                        #     gray,
                        #     scaleFactor=1.1,
                        #     minNeighbors=5,
                        #     minSize=(80, 80),
                        #     flags=cv2.CASCADE_SCALE_IMAGE
                        #
                        # )
                        # # 增大第四个参数可以提高检测精度, 但也可能会造成遗漏
                        # #  人脸尺寸minSize和maxSize，关键参数，自行设定，随图片尺寸有很大关系，
                        #
                        # # print(len(faces) + faces)
                        # if len(faces)>0 :
                        #     print('find faces  ' + p.name+ '  '+ str(p.pk))
                        #     p.icon = img_path.replace(base, '')
                        #     p.save()
                        #     continue
                except:
                    error.append(img.pk)
            #
            # try:
            #     print('进度：' + str(i*100/total) + '%\n')
            # except:
            #     pass



print('\n缩略图完成，正在生成log文件。。。。')


dt = datetime.now()
time2 = dt.strftime("%m%d-%H%M%S")
#
# fname3 = 'log/log_iconMake' + time2 + '.txt'
# with open(fname3, 'w+') as f:
#
#     f.write('\n错误********************************************\n')
#     # f.write('name' + ' ' + 'id' + ' ' + 'path' + '\n')
#     f.write('总计：' + str(len(error)) + '\n')
#     for d in error:
#         f.write(d + '\n')
#
#     f.write('\n\n\n成功添加******************************************\n')
#     # f.write('name' + ' ' + 'id' + ' ' + 'path' + '\n')
#     f.write('总计：' + str(len(imgAddIcon)) + '\n')
#     for d in imgAddIcon:
#         f.write(str(d) + '\n')
#
#     f.write('\n\n\n删除******************************************\n')
#     # f.write('name' + ' ' + 'id' + ' ' + 'path' + '\n')
#     f.write('总计：' + str(len(dels)) + '\n')
#     for d in dels:
#         f.write(str(d) + '\n')

print('\n完成。。。。')

# imgName= img_path.split('/')[-1]  # 赵云.p0.0186202.jpg
#
# # 图像的目录
# img_post  = img.post # TODO warnning 默认img已经有post信息，此处可能出错
# post_path = base + img_post.dir
#
# small_path = post_path+'/'+ 'small'+ '_'+ imgName
# medium_path = post_path+'/'+ 'medium'+ '_'+ imgName
#
# # 制作缩略图函数
#
# if not img.thumbnail:
#     im = Image2.open(img_path)
#     size = (400, 400)
#     if im:
#     # im = Image.open(infile)
#         im.thumbnail(size)
#         im.save(small_path, "JPEG")
#         img.thumbnail = small_path.replace(base, '')
#         img.save()
#         imgAddIcon.append(img.pk)

#         print('成功制作缩略图：' + img.path + '\n')