#!/usr/bin/python
# -*- coding: UTF-8 -*-
import mysite
# 这个一定要，不然会报错，但是错误很明显，容易定位。
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
import django
django.setup()
# django版本大于1.7时需要这两句

from datetime import datetime
import time
import requests
import json
import sys
import random
from boards.models import *
from linkedcare.syncDB import logIn, getTokenFromSession
from mysite.settings import  BASE_DIR

agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3418.2 Safari/537.36"


# s= logIn()


suf = 'jpg'
sep = '_'

# base = "/Users/wcy/Documents/mysite2"
# base = "/home/zdl/mysite2"
base = BASE_DIR
# inputDir = '/static/待导入图像'
picDir = base + '/static/picture'
# /Volumes/张栋梁病例照片/正畸患者照片/唇侧正畸/A/
# dir = "/static/picture/老硬盘照片"
# dir = "/static/picture/a正畸患者照片"

# linkedcareId = 432349
UrlGetApptList = "https://api.linkedcare.cn:9001/api/v1/appointment-record/patient/"
# https: // api.linkedcare.cn: 9001 / api / v1 / appointment - record / patient / 432349

UrlGetImage = "https://api.linkedcare.cn:9001/api/v1/imaging?appointmentId="
# https://api.linkedcare.cn:9001/api/v1/imaging?appointmentId=1222210
# s = logIn()

# 从cookie中获取token
token = None
# token = getTokenFromSession(s)
# 组装header
headers =None
# headers = {'authority': 'api.linkedcare.cn:9001',
#            "authorization": "bearer " + token, "access_token": token,
#            # "clientId":"7c378f28-6bc8-4c1a-a40e-3ba38a0b48fd",
#            "origin": "https://simaier.linkedcare.cn",
#            'Connection': 'keep-alive', 'user-agent': agent,
#            'referer': 'https://simaier.linkedcare.cn/',
#            'content-type': 'application/json;charset=UTF-8'
#            }


def getXrayOfperson(s, person):
    token = getTokenFromSession(s)
    headers = get_header_use_token(token)
    if not person.linkedcareId:
        print('get_xray: 此患者无linkedcareId\n')
    else:
        print('get_xray: 正在导入此患者 %s\n' %(person.name))
        # 获取预约列表
        re = s.get(UrlGetApptList + str(person.linkedcareId), headers=headers)
        # json  {id: 1222594, officeId: 124, startTime: "2018-11-10T15:30:00", endTime: "2018-11-10T16:00:00",…}

        # person = Person.objects.get(linkedcareId=linkedcareId)
        # privDir = picDir + '/' + person.name + '_' + str(person.idnum) + '/'
        if person.privateDir:
            if person.privateDir[0] == '/':
                dir = base + person.privateDir
                if not dir[-1] =='/': # 补漏洞。。
                    dir = dir+'/'
            else:
                dir = base + '/' + person.privateDir
                if not dir[-1] == '/':
                    dir = dir + '/'

        else:
            dir = picDir + '/' + person.name + '_' + str(person.idnum) + '/'
            person.privateDir = dir.replace(base, '')  # 图片相对地址 /static/picture/xxx/xxx
            person.save()

        if not os.path.exists(dir):
            os.mkdir(dir)
        apptList = json.loads(re.content.decode('utf-8'))
        # str = re.text
        # apptList =json.loads(str)
        i2 = 0
        if apptList:
            for appt in apptList:
                apptId = appt['id']  # 提取预约id
                # startTime: "2018-11-10T15:30:00"
                time = appt['startTime'].split('T')[0]

                # 根据预约id找相对应的图片list
                reImgList = s.get(UrlGetImage + str(apptId), headers=headers)
                imgList = json.loads(reImgList.content.decode('utf-8'))
                if imgList:
                    # type100以上 表示linkdedcare导入
                    #  重复检查，如果已经下载此x线，则取消
                    n = Post.objects.filter(name__contains=time, person=person).count()
                    if n>0:
                        continue
                    #检查现在xray的post 数目
                    n2 = Post.objects.filter(person=person, type__gte=100).count()

                    post = Post.objects.create(name=time, comment=time, type=100 + i2 +n2, person=person)
                    i2 = i2+1

                    for imgItem in imgList:
                        # 准备文件名及路径
                        dt = datetime.now()
                        times = dt.strftime("%f")
                        datestr = dt.strftime("%Y%m%d")
                        # 文件名   张飞_20180101_S0_041411.jpg
                        fname = person.name + sep + datestr + sep + 'S' + str(post.type) + sep + times + '.' + suf
                        # 相对全路径 static / picture / 张飞_233 / 张飞_20180101_041411.jpg
                        path = dir + fname
                        iconpath = dir + 'small' + fname
                        mediumpath = dir + 'medium' + fname

                        # 开始下载保存
                        fullImgUrl = imgItem['fullImageUrl']
                        medimImgUrl = imgItem['mediumSizeImageUrl']
                        logoUrl = imgItem['thumbnailUrl']

                        try:  # 下载
                            print('开始下载\n')
                            data = s.get(fullImgUrl).content  # 音乐的二进制数据
                            with open(path, 'wb') as f:
                                f.write(data)
                            data = s.get(medimImgUrl).content  # 音乐的二进制数据
                            with open(mediumpath, 'wb') as f:
                                f.write(data)
                            data = s.get(logoUrl).content  # 音乐的二进制数据
                            with open(iconpath, 'wb') as f:
                                f.write(data)
                            path = path.replace(base, '')
                            iconpath = iconpath.replace(base, '')
                            mediumpath = mediumpath.replace(base, '')

                            newImg = Image.objects.create(name=fname, post=post, person=person, path=path, size_m=mediumpath,
                                                          thumbnail=iconpath)
                            print('创建img%s  患者：%s' %(str(newImg.pk), person.name))

                        except Exception as e:
                            print(e + person.name)

def get_header_use_token(token):
    header = {'authority': 'api.linkedcare.cn:9001',
               "authorization": "bearer " + token, "access_token": token,
               # "clientId":"7c378f28-6bc8-4c1a-a40e-3ba38a0b48fd",
               "origin": "https://simaier.linkedcare.cn",
               'Connection': 'keep-alive', 'user-agent': agent,
               'referer': 'https://simaier.linkedcare.cn/',
               'content-type': 'application/json;charset=UTF-8'
               }
    return header

def mainfunc():
    s = logIn()
    token = getTokenFromSession(s)
    headers = get_header_use_token(token)

    persons  = Person.objects.all()
    total = persons.count()
    i = 0

    for p in persons:
        i = i+1
        if p.linkedcareId:
            # type100以上 表示linkdedcare导入
            n = Post.objects.filter(type__gt=20, person=p).count()
            if n > 0:
                continue
            # time.sleep(random.randint(1, 5))
            getXrayOfperson(s, p)
        print('\n第 %s个， total %s' %(str(i), str(total) ))


if __name__ == '__main__':
    pass
