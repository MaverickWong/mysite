#!/usr/bin/python
# -*- coding:utf8 -*-
# 这个一定要，不然会报错，但是错误很明显，容易定位。
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
import django
django.setup()

from aip import AipFace
import base64
import json
import time,random
from mysite.settings import BASE_DIR
from boards.models import *

# pip install baidu-aip


""" 你的 APPID AK SK """
APP_ID = '15944774'
API_KEY = 'XWkA0BtqhrH3u5CyGH1lgwMv'
SECRET_KEY = 'xq5hFIFlbTgzIQFWvFq0NRjXya7zncw8'
# ak = 'SOWwc5QogEB164X8zn6XwKsX'
# access_token = 'KVUtFodjRqU7bECM3ztQIQwtuN6jDGyB'
client = AipFace(APP_ID, API_KEY, SECRET_KEY)


# 将图片编码为base64字符串
def base64_str(filepath):
	f = open(r'%s' % filepath, 'rb')
	pic1 = base64.b64encode(f.read())
	f.close()
	return str(pic1, 'utf-8')


# 人脸检测：检测图片中的人脸并标记出位置信息;
def find_face(imgpath):
	image = base64_str(imgpath)
	imageType = "BASE64"

	# """ 调用人脸检测 """
	# client.detect(image, imageType)

	""" 如果有可选参数 """
	options = {}
	options["face_field"] = "age,landmark"
	options["max_face_num"] = 2
	options["face_type"] = "LIVE"

	""" 带参数调用人脸检测 """
	a = client.detect(image, imageType, options)
	# print(a)
	return a


""" 带参数调用人脸搜索 """


def find_user(imgpath):
	image = base64_str(imgpath)
	imageType = "BASE64"

	groupIdList = "simaier"

	""" 调用人脸搜索 """
	a = client.search(image, imageType, groupIdList)

	# """ 如果有可选参数 """
	# options = {}
	# options["quality_control"] = "NORMAL"
	# options["liveness_control"] = "LOW"
	# # options["user_id"] = "233451"
	# options["max_user_num"] = 3

	# """ 带参数调用人脸搜索 """
	# a= client.search(image, imageType, groupIdList, options)
	# print(a)
	return a

""" 人脸注册到user """


def add_user(imgpath, person ):
	image = base64_str(imgpath)
	imageType = "BASE64"
	groupId = "simaier"

	userId = str(person.pk)

	""" 调用人脸注册 """
	# client.addUser(image, imageType, groupId, userId);

	# """ 如果有可选参数 """
	options = {}
	# options["user_info"] = person.name.encode('utf-8')
	options["quality_control"] = "NORMAL"
	# options["liveness_control"] = "LOW"

	# """ 带参数调用人脸注册 """
	a = client.addUser(image, imageType, groupId, userId, options)
	return a

# def test():
# # 	re = find_face()
# # 	if re['error_code'] == 0:
# # 		print('识别成功')
# # 		if re['error_msg']['face_num'] == 1:
# # 			f = re['error_msg']['face_num']['face_list'][0]
# # 			# angle = f['angle']
# # 			if abs(f['angle']['yaw']) < 20:
# # 				print('识别到正脸，保存')
# # 	else:
# # 		print('pic has no face ')




base = BASE_DIR
# dir = "/static/picture/a正畸患者照片"

persons_new_face = []

error=[]
imgAddIcon =[]
dels =[]


def find_face_of_persons(persons):
	total = persons.count()
	i = 0
	for p in persons:
		print('开始 %s %d 第 %d 个，共 %d 个' % (p.name, p.pk, i, total))

		i = i + 1
		if not p.isBaiduFaceSaved:  #  先检查是否已存到百度
			imgs = p.images.all()
			for img in imgs:
				# if not p.icon:
				try:
					img_path = base + img.size_m
					if os.path.exists(img_path):
						# 读取图片并识别人脸
						time.sleep(0.5)
						re = find_face(img_path)
						if re['error_code'] == 0:
							print('识别成功 第 %d 个，共 %d 个' %(i, total))
							if re['result']['face_num'] == 1:
								f = re['result']['face_list'][0]
								# angle = f['angle']
								if abs(f['angle']['yaw']) < 20:
									print('识别到 %s 正脸，保存' %( p.name ))
									img.baiduFaceInfo = json.dumps(re)
									img.type = 1 # 正面
									img.save()

									# 注册
									time.sleep(0.5)
									add_user(img_path, p)

									p.isBaiduFaceSaved = True
									p.icon = img.thumbnail
									p.save()

									persons_new_face.append(p)


								elif abs(f['angle']['yaw']) > 70:
									img.baiduFaceInfo = json.dumps(re)
									img.type = 2 # 侧面
									img.save()
									p.isBaiduFaceSaved = True
									p.save()

						else:
							print('pic has no face ')
							p.isBaiduFaceSaved = True
							p.save()

				except:
					error.append(img.pk)
		else:
			print('已经有百度识别记录，pass')


from PIL import Image as Image2


def correct_face_oritation_of_persons(persons):
	total = len(persons)
	i = 0
	for p in persons:
		i = i + 1
		imgs = p.images.all()
		for img in imgs:
			if img.type == '1':
				# try:
				info = json.loads(img.baiduFaceInfo)
				f = info['result']['face_list'][0]
				angle = f['angle']['roll']
				print(angle)
				if angle > 0:
					print('270旋转 %s %d 第 %d 个人，共 %d 个' % (p.name, p.pk, i, total))
					rotate_img_degree(img, 270)
				if angle < 0:
					rotate_img_degree(img, 90)
					print('90旋转 %s %d 第 %d 个人，共 %d 个' % (p.name, p.pk, i, total))

			# except:
			# 	error.append(img.pk)


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


if __name__ == '__main__':
	# file1path = './pic/6.jpg'
	# file2path = './pic/2.jpg'
	print('start')
	# res = faceRec(file1path, file2path)
	# add_user(file1path)
	# find_face(file1path)
	# find_user(file1path)

	persons = Person.objects.all().order_by('pk').reverse()
	find_face_of_persons(persons)

# p = Person.objects.get(pk=5373)
# p2 = Person.objects.get(pk=8067)
#
# persons_new_face.append(p)
# persons_new_face.append(p2)
#
# correct_face_oritation_of_persons(persons_new_face)

'''
先上传图片，并检查是否有人脸，如果有则加入user，id,并保存图片检测信息，更新logo

第一次上传照片后，人脸检测，如果有，则注册add，并标记logo
非第一次上传，都先检查是否已有logo，如果没有，人脸检测

侧脸 yaw 快90
{'error_code': 0, 'error_msg': 'SUCCESS', 'log_id': 304592844779512281, 'timestamp': 1554477951, 'cached': 0, 
	'result': {'face_num': 1, 'face_list': [{'face_token': '5b9e7afb641ad8b8a8424c73ab1307c3', 'location': {'left': 241.92, 'top': 106.79, 'width': 82, 'height': 94, 'rotation': 92}, 'face_probability': 0.91, 'angle': {'yaw': -76.15, 'pitch': 9.13, 'roll': 104.65}, 'age': 23, 'landmark': [{'x': 220.72, 'y': 166.16}, {'x': 219.56, 'y': 179.13}, {'x': 199.95, 'y': 182.87}, {'x': 170.41, 'y': 175.54}], 'landmark72': [{'x': 223.82, 'y': 105.75}, {'x': 207.14, 'y': 108.08}, {'x': 190.15, 'y': 111.9}, {'x': 173.38, 'y': 119.02}, {'x': 157.83, 'y': 132.66}, {'x': 148.1, 'y': 149.67}, {'x': 144.83, 'y': 166.44}, {'x': 157.68, 'y': 172.59}, {'x': 169.78, 'y': 176.87}, {'x': 182.54, 'y': 179.87}, {'x': 195.83, 'y': 180.86}, {'x': 209.28, 'y': 180.77}, {'x': 222.51, 'y': 180.76}, {'x': 220.18, 'y': 160.09}, {'x': 221.9, 'y': 162.31}, {'x': 223.22, 'y': 164.9}, {'x': 222.81, 'y': 167.35}, {'x': 220.16, 'y': 168.6}, {'x': 218.55, 'y': 166.99}, {'x': 218.27, 'y': 164.74}, {'x': 218.81, 'y': 162.33}, {'x': 220.72, 'y': 166.16}, {'x': 233.18, 'y': 156.25}, {'x': 237.69, 'y': 160.75}, {'x': 239.55, 'y': 165.89}, {'x': 238.59, 'y': 171.05}, {'x': 233.57, 'y': 174.55}, {'x': 234.45, 'y': 170.23}, {'x': 234.84, 'y': 165.53}, {'x': 234.46, 'y': 160.92}, {'x': 219.46, 'y': 176.87}, {'x': 220.77, 'y': 177.4}, {'x': 221.57, 'y': 178.71}, {'x': 220.98, 'y': 180.14}, {'x': 219.3, 'y': 179.63}, {'x': 218.2, 'y': 179.27}, {'x': 218.27, 'y': 177.94}, {'x': 218.67, 'y': 177.08}, {'x': 219.56, 'y': 179.13}, {'x': 231.48, 'y': 178.24}, {'x': 233.96, 'y': 178.82}, {'x': 235.71, 'y': 179.87}, {'x': 235.32, 'y': 180.68}, {'x': 233.64, 'y': 180.65}, {'x': 233.3, 'y': 179.96}, {'x': 232.67, 'y': 179.29}, {'x': 232.08, 'y': 178.76}, {'x': 218.45, 'y': 169.56}, {'x': 208.21, 'y': 170.43}, {'x': 197.88, 'y': 170.82}, {'x': 187.71, 'y': 171.18}, {'x': 186.1, 'y': 177.5}, {'x': 190.31, 'y': 181.61}, {'x': 195.22, 'y': 186.99}, {'x': 203.04, 'y': 183.11}, {'x': 211.08, 'y': 178.06}, {'x': 219.21, 'y': 173.41}, {'x': 199.95, 'y': 182.87}, {'x': 169.59, 'y': 169.48}, {'x': 174.23, 'y': 173.85}, {'x': 176.7, 'y': 179.23}, {'x': 173.31, 'y': 178.68}, {'x': 170.63, 'y': 177.61}, {'x': 167.27, 'y': 176.64}, {'x': 164.28, 'y': 176.74}, {'x': 166.25, 'y': 172.73}, {'x': 171.25, 'y': 173.54}, {'x': 172.28, 'y': 177.84}, {'x': 171.14, 'y': 175.69}, {'x': 169.98, 'y': 175.24}, {'x': 169.21, 'y': 176.95}, {'x': 169.59, 'y': 173.3}]}]}}
正脸 yaw 比较小
{'error_code': 0, 'error_msg': 'SUCCESS', 'log_id': 305486844781999091, 'timestamp': 1554478200, 'cached': 0, 'result': {'face_num': 1, 'face_list': [{'face_token': 'efd781bf2c64ba8629805e41d87b8f1b', 'location': {'left': 738.52, 'top': 263.32, 'width': 295, 'height': 290, 'rotation': 90}, 'face_probability': 1, 'angle': {'yaw': 5.53, 'pitch': 9.43, 'roll': 87.7}, 'age': 25, 'landmark': [{'x': 686.85, 'y': 345.9}, {'x': 685.22, 'y': 465.29}, {'x': 605.96, 'y': 402.01}, {'x': 541.85, 'y': 404.43}], 'landmark72': [{'x': 692.73, 'y': 262.75}, {'x': 646.03, 'y': 266.31}, {'x': 598.51, 'y': 272.83}, {'x': 551.14, 'y': 283.8}, {'x': 502.94, 'y': 312.05}, {'x': 462.28, 'y': 355.92}, {'x': 446.38, 'y': 403.61}, {'x': 459.93, 'y': 452.56}, {'x': 497.65, 'y': 499.52}, {'x': 545.84, 'y': 531.34}, {'x': 593.79, 'y': 544.14}, {'x': 641.53, 'y': 552.53}, {'x': 689.46, 'y': 557.77}, {'x': 684.68, 'y': 315.99}, {'x': 693.51, 'y': 329.7}, {'x': 695.8, 'y': 344.39}, {'x': 691.37, 'y': 358.45}, {'x': 678.33, 'y': 369.94}, {'x': 677.28, 'y': 356.94}, {'x': 676.85, 'y': 342.42}, {'x': 679.75, 'y': 327.92}, {'x': 686.85, 'y': 345.9}, {'x': 715.63, 'y': 291.85}, {'x': 735.21, 'y': 309.61}, {'x': 738.11, 'y': 331.98}, {'x': 734.65, 'y': 353.83}, {'x': 719.55, 'y': 373.41}, {'x': 720.95, 'y': 352.39}, {'x': 722.96, 'y': 331.5}, {'x': 721.35, 'y': 311.38}, {'x': 677.34, 'y': 438.61}, {'x': 689.82, 'y': 450.28}, {'x': 694.1, 'y': 464.31}, {'x': 691.67, 'y': 479.25}, {'x': 682.55, 'y': 492.87}, {'x': 677.77, 'y': 480.7}, {'x': 675.61, 'y': 465.98}, {'x': 675.82, 'y': 451.83}, {'x': 685.22, 'y': 465.29}, {'x': 718.92, 'y': 433.76}, {'x': 733.09, 'y': 454.03}, {'x': 735.56, 'y': 475.82}, {'x': 732.2, 'y': 498.22}, {'x': 713.65, 'y': 516.72}, {'x': 718.84, 'y': 496.69}, {'x': 720.33, 'y': 475.83}, {'x': 719.52, 'y': 454.9}, {'x': 675.62, 'y': 386.69}, {'x': 649.49, 'y': 381.13}, {'x': 623.03, 'y': 375.26}, {'x': 596.26, 'y': 364.98}, {'x': 592.37, 'y': 383.6}, {'x': 591.97, 'y': 422.4}, {'x': 595.22, 'y': 442.17}, {'x': 622.3, 'y': 432.3}, {'x': 648.48, 'y': 426.88}, {'x': 674.9, 'y': 421.63}, {'x': 605.96, 'y': 402.01}, {'x': 550.39, 'y': 350.9}, {'x': 559.97, 'y': 375.52}, {'x': 559.23, 'y': 403.59}, {'x': 559.7, 'y': 433.54}, {'x': 549.48, 'y': 460.75}, {'x': 522.19, 'y': 437.84}, {'x': 511.18, 'y': 403.37}, {'x': 523.18, 'y': 370.87}, {'x': 551.16, 'y': 376.46}, {'x': 548.79, 'y': 403.65}, {'x': 550.89, 'y': 432.76}, {'x': 534.66, 'y': 432.93}, {'x': 529.91, 'y': 403.65}, {'x': 535.12, 'y': 376.21}]}]}}
错误
{'error_code': 222202, 'error_msg': 'pic not has face', 'log_id': 305486844790905701, 'timestamp': 1554479090, 'cached': 0, 'result': None}
注册 adduser
{'error_code': 0, 'error_msg': 'SUCCESS', 'log_id': 305486845159375501, 'timestamp': 1554515937, 'cached': 0, 'result': {'face_token': 'efd781bf2c64ba8629805e41d87b8f1b', 'location': {'left': 738.52, 'top': 263.32, 'width': 295, 'height': 290, 'rotation': 90}}}
{'error_code': 222202, 'error_msg': 'pic not has face', 'log_id': 304592845167125582, 'timestamp': 1554516712, 'cached': 0, 'result': None}

finduser
{'error_code': 0, 'error_msg': 'SUCCESS', 'log_id': 304569245172118411, 'timestamp': 1554517211, 'cached': 0, 'result': {'face_token': 'efd781bf2c64ba8629805e41d87b8f1b', 'user_list': [{'group_id': 'person', 'user_id': 'user1', 'user_info': 'abc', 'score': 41.308052062988}]}}
{'error_code': 0, 'error_msg': 'SUCCESS', 'log_id': 304592845176160941, 'timestamp': 1554517616, 'cached': 0, 'result': {'face_token': 'efd781bf2c64ba8629805e41d87b8f1b', 'user_list': [{'group_id': 'group1', 'user_id': 'user1', 'user_info': '', 'score': 100}]}}

'''
