#!/usr/bin/python
# -*- coding:utf8 -*-
# 这个一定要
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
import django
django.setup()
# django版本大于1.7时需要这两句

import requests
from linkedcare.syncDB import logIn
from mysite.settings import BASE_DIR

# def sendImg(img_path, img_name, img_type='image/jpeg'):
# 	"""
# 	:param img_path:图片的路径
# 	:param img_name:图片的名称
# 	:param img_type:图片的类型,这里写的是image/jpeg，也可以是png/jpg
# 	"""
# 	url = 'https://api.linkedcare.cn:9201/api/v1/image-upload?appointmentId=1833516&categoryId=1' # 自己想要请求的接口地址
#
# 	with open(img_path + img_name, "rb")as f_abs：# 以2进制方式打开图片
# 	body = {
# 	# 有些上传图片时可能会有其他字段,比如图片的时间什么的，这个根据自己的需要
#
# 	'camera_code': (None, "摄像头1"),
#
# 	'image_face': (img_name, f_abs, img_type)
# 	# 图片的名称、图片的绝对路径、图片的类型（就是后缀）
#
# 	"time":(None, "2019-01-01 10:00:00")
#
# 	}
# 	# 上传图片的时候，不使用data和json，用files
# 	response = requests.post(url=url, files=body).json
# 	return response





# multiple_files = [
#  ('images', ('foo.png', open('foo.png', 'rb'), 'image/png')),
#  ('images', ('bar.png', open('bar.png', 'rb'), 'image/png'))]
# r = requests.post(url, files=multiple_files)


if __name__=='__main__':
	# 上传图片
	# res = sendImg(img_path, img_name) # 调用sendImg方法
	# print(res)

	files = [
		('images', ('logo.png', open(BASE_DIR + '/logo.png', 'rb'), 'image/png')),
	]
	payload = {
		'appointmentId':1833516,
		'categoryId':1,
		'files':files
	}

	s = logIn()
	url = 'https://api.linkedcare.cn:9201/api/v1/image-upload?appointmentId=1833516&categoryId=1'
	# url = 'https://api.linkedcare.cn:9201/api/v1/image-upload'

	r = s.post(url=url, data=files)

	print(r.content)