#!/usr/bin/python
# -*- coding:utf8 -*-

import os
from boards.models import *

def is_img(ext):
  ext = ext.lower()
  if ext in ['jpg', 'png', 'jpeg', 'bmp']:
    return True
  else:
    return False

# /Volumes/张栋梁病例照片/正畸患者照片/唇侧正畸/A/
base = "/Users/Wang/mysite2/static/test"

allpatients = []
repeated = []
added = []
created = []


def start():
	for root, dirs, files in os.walk(base):
		# if not dirs:
		post = root.split('/')[-1]
		p = root.split('/')[-2]
		print("\n" +p + "  " + post)

		pnum = Person.objects.filter(name__contains=p).count()
		if pnum == 0:
			newP = Person.objects.create(name=p, comment=p)
			created.append(p)
		elif pnum ==1:
			newP = Person.objects.get(name=p)
			added.append(p)
		elif pnum >1:
			repeated.append(p)
			print("\n发现重复患者： %s" %p)
			continue
			
		# if Post.objects.filter(name=post)
		newPost = Post.objects.create(name=post, person=newP, type=1, comment=post)

		for file in files:
			# print("File:%s,  %s" %(file, root))fro
			ext = file.split('.')[-1]
			if is_img(ext):
				print("创建image：%s post：%s 患者：%s" %(file, post, p))
				newImg = Image.objects.create(name=file, post=newPost, person=newP, path=root)

	with open('a.txt', 'w+') as f:
		f.write('\n\n\n重复患者**************************************\n')
		for line in repeated:
			f.write(line+'\n')
		f.write('\n\n\n新建患者**************************************\n')
		for line in created:
			f.write(line + '\n')
		f.write('\n\n\n直接添加图片的患者*****************************\n')
		for line in added:
			f.write(line + '\n')
		f.close()

#  walk的结果：root， dirs， filenames
# 假设根据阶段分文件夹，则将第一个抛弃后，新建post，image，加到person
#
# az = [] # a-z 所有字母文件夹
# for a, b, c in os.walk(base):
# 	az.append(b)
# azdir = az[0]
# # print(az[0])

# for az1 in azdir:
# 	azpath= base +'/' +az1
# 	allP= [] # 所有患者文件夹
# 	for a, b, c in os.walk(azpath):
# 		allP.append(b)
# 	persons = allP[0]
# 	print(allP[0])
#
# 	for p in persons:
# 		# 创建新person的model
# 		# personM = Person.models.create(name=p)
# 		print("\n\n\n患者：%s \n" %p)
# 		t = [] # 所有posts文件夹
# 		personDir = azpath+ '/' + p # 患者文件夹全路径
# 		for a, b, c in os.walk(personDir):
# 			# print(b)
# 			t.append(b)
# 		posts = t[0]
# 		# print(posts)
#
# 		for po in posts:
# 			podir = personDir + '/' +po
# 			# postM = Post.models.creat(name=po, person=personM)
# 			print("post：%s" %po)
# 			print(os.path.getctime(podir))
# 			files = [] # post文件夹内部所有图像文件
# 			for a, b, c in os.walk(podir):
# 				files.append(c)
# 			files = files[0]
# 			for file in files:
# 				# print(img)
# 				ext = file.split('.')[-1]
# 				if is_img(ext): # 验证是否图像文件
# 					imgpath = podir + '/' +file
# 					# 缩略图
# 					# imgM = Images.models.creat(name=img, path=imgpath, person=personM)
# 					print("创建image：%s post：%s 患者：%s" %(file, po, p))
# 					# print(os.path.getctime(imgpath))
#
