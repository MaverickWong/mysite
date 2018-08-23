# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
import json
import os
import re
import urllib

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from boards.models import Person
import os

# Create your views here.
def home(request):
	persons = Person.objects.all()
	return render(request, 'index.html',{'persons': persons})
	#return HttpResponse(response_html)
	#return HttpResponse("hello, board home!")

# def board_topics(request, pk):
# 	board = get_object_or_404(Topics)
	# return render(request, 'topics.html', {'board': board})

# def new(request):
# 	# return render(request, 'upload.html')
# 	return render(request, 'upload/index.html')

# def upfile(request):
# 	#lastUpdateTime记录一下上传时间，如果跟当前时间大于5分钟，要分成不同的组
# 	subject = request.POST['name']
# 	# message = request.POST['ID']
# 	user = User.objects.first()  # TODO: 临时使用一个账号作为登录用户
# 	topic = Person.objects.create(subject=subject)
#
# 	files = request.FILES.getlist('files[]') #类型为mutilist
# 	n = request.POST.get('name')
# 	print(files)
# 	i = 0
# 	for f in files:
# 		ff = open('./upload/' + n + str(i), 'wb+')
# 		print(f.name)
# 		for chunk in f.chunks():
# 			ff.write(chunk)
# 		ff.close()
# 		i=i+1
#
# 	return HttpResponse("received:"+ str(i))

#接收文件
# def upfile(request):
# 	# sava_path = '/static/main/img/cart.png'  # 默认图片
# 	if request.method == 'POST':
# 		files = request.FILES.get('files')  # 获取name标签为file的图片
# 		if files:
# 			print(files)
#
# 		# 图片存放路径
# 		# filename = encryption(str(time.time())) + '.' + files.content_type.split('/')[1]
# 		# sava_path = 'static/main/user_file/' + filename
# 		save_path = os.getcwd() + 'a.jpg'
# 		# 将图片分段读取并写入文件
# 		with open(save_path, 'wb') as f:
# 			for file in files.chunks():
# 				f.write(file)
# 	 			f.flush()
# 		# 将图片路径更新到当前用户的表中
# 		# user = User.objects.filter(token=request.COOKIES.get('token'))
# 		# user.update(icon=sava_path)
# 	# 将上传成功的图片路径返回给页面
# 	return JsonResponse({'status':'200', 'img': save_path})
# def write_blob(data, info):
# 	key = urllib.quote(info['type'].encode('utf-8'), '') + \
# 	      '/' + str(hash(data)) + \
# 	      '/' + urllib.quote(info['name'].encode('utf-8'), '')
# 	try:
# 		memcache.set(key, data, time=EXPIRATION_TIME)
# 	except:  # Failed to add to memcache
# 		return (None, None)
# 	thumbnail_key = None
# 	if IMAGE_TYPES.match(info['type']):
#
# 			img = images.Image(image_data=data)
# 			img.resize(
# 				width=THUMB_MAX_WIDTH,
# 				height=THUMB_MAX_HEIGHT
# 			)
# 			thumbnail_data = img.execute_transforms()
# 			thumbnail_key = key + THUMB_SUFFIX
# 			memcache.set(
# 				thumbnail_key,
# 				thumbnail_data,
# 				time=EXPIRATION_TIME
# 			)
#
# 	return (key, thumbnail_key)


# def upfile(request):
# 	# results = []
# 	# for name, fieldStorage in request.FILES.get('files[]'):
# 	# 	if type(fieldStorage) is unicode:
# 	# 		continue
# 	# 	result = {}
# 	# 	result['name'] = urllib.unquote(fieldStorage.filename)
# 	# 	result['type'] = fieldStorage.type
# 		# result['size'] = self.get_file_size(fieldStorage.file)
# 		# if self.validate(result):
# 		# 	key, thumbnail_key = self.write_blob(
# 		# 		fieldStorage.value,
# 		# 		result
# 		# 	)
# 		# 	if key is not None:
# 		# 		result['url'] = self.request.host_url + '/' + key
# 		# 		result['deleteUrl'] = result['url']
# 		# 		result['deleteType'] = 'DELETE'
# 		# 		if thumbnail_key is not None:
# 		# 			result['thumbnailUrl'] = self.request.host_url + \
# 		# 			                         '/' + thumbnail_key
# 		# 	else:
# 		# 		result['error'] = 'Failed to store uploaded file.'
# 		results.append(result)
# 	return results



def new_person(request):
	# board = get_object_or_404(Board, pk=pk)
	if request.method == 'POST':
		subject = request.POST['name']
		# message = request.POST['ID']
		user = User.objects.first()  # TODO: 临时使用一个账号作为登录用户
		topic = Person.objects.create(subject=subject)
		# post = Post.objects.create(message=message, topic=topic,created_by=user)

		files = request.FILES.getlist('files[]')  # 类型为mutilist
		n = request.POST.get('name')
		print(files)
		i = 0
		for f in files:
			ff = open('./static/picture/' + n, 'wb+')
			print(f.name)
			for chunk in f.chunks():
				ff.write(chunk)
			ff.close()
			i = i + 1

		return redirect('home')  # TODO: redirect to the created topic page

	if request.method == 'GET':
		return render(request, 'upload/index.html')

def person_detail(request,pk):
	p = Person.objects.get(pk=pk)
	name = p.subject
	url = '../static/picture/'+ name

	return render(request, 'detail.html', {'patient':p, 'picurl':url})
	# return HttpResponse('good person')