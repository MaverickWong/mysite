# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
import json
import os
import re
from PIL import Image as Image2


from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from boards.models import *
from datetime import date, time, datetime
import os


# Create your views here.
def home(request):
	persons = Person.objects.all()
	return render(request, 'index.html', {'persons': persons})

def search(request):
	s = request.GET['s']
	if s.isnumeric():
		persons = Person.objects.filter(idnum=s)
	else:
		persons = Person.objects.filter(name__contains=s)

	return render(request, 'search.html', {'persons': persons})

# def board_topics(request, pk):
# 	board = get_object_or_404(Topics)
# return render(request, 'topics.html', {'board': board})

# def new(request):
# 	# return render(request, 'upload.html')
# 	return render(request, 'upload/index.html')


def handle_file(request, person, post):
	files = request.FILES.getlist('files[]')  # 类型为mutilist
	# n = request.POST.get('name')

	print(files)
	i = 0
	for f in files:
		dt = datetime.now()
		time = dt.strftime("%f")

		dir = 'static/picture/' + person.name + str(person.idnum) + '/'
		icondir = 'static/picture/' + person.name + str(person.idnum) + '/' + 'small' + '/'
		if not os.path.exists(dir):
			os.mkdir(dir)
		if not os.path.exists(icondir):
			os.mkdir(icondir)

		n2 = f.name
		suf = n2.split('.')[-1]
		path = dir + person.name + '.p' + str(post.type) + '.' + str(i) + time + '.' + suf
		iconpath = icondir + person.name + '.p' + str(post.type) + '.' + 'small'+'.' +str(i) + time + '.' + suf
		ff = open(path, 'wb+')
		# ff.name
		print(path)
		print(f.name)
		for chunk in f.chunks():
			ff.write(chunk)
		ff.close()
		i = i+1

		# 缩略图函数
		if os.path.exists(path):
			im= Image2.open(path)
			size = (800, 600)
			if im:
				try:
					# im = Image.open(infile)
					im.thumbnail(size)
					im.save(iconpath, "JPEG")
				except IOError:
					print("cannot create thumbnail")

		path = '../' + path
		iconpath = '../' +iconpath
		if i==0:
			person.icon = path
			person.save()
		image = Image.objects.create(path=path, thumbnail=iconpath, post=post, person=person)


	return 1


def new_person(request):
	# board = get_object_or_404(Board, pk=pk)
	if request.method == 'POST':

		# message = request.POST['ID']
		# user = User.objects.first()  # TODO: 临时使用一个账号作为登录用户
		name = request.POST['name']
		idnum = request.POST['ID']
		if Person.objects.filter(name=name, idnum=idnum).exists():
			# person = Person.objects.get(name=name, idnum=idnum)
			return redirect('wrong')
		else:
			person = Person.objects.create(name=name, idnum=idnum)

		post = Post.objects.create(type=0, isFirst=1, person=person)

		# n = Post.objects.get(person=person).count()
		# post = Post.objects.create(type=n + 1, person=person)
		# post = Post.objects.get(type=0, isFirst=1, person=person)
		# if not post:
		# post = Post.objects.create(type=0, isFirst=1, person=person)
		# 处理上传文件
		handle_file(request, person, post)

		return redirect('home')  # TODO: redirect to the created topic page

	if request.method == 'GET':
		return render(request, 'upload/index.html')


def addpost(request, pk):
	p = Person.objects.get(pk=pk)

	if request.method == 'GET':
		# TODO 应该获取posts总数，然后发到网页内部

		return render(request, 'upload/addpost.html', {'patient': p})

	if request.method == 'POST':
		# p = Person.objects.get(pk=pk)
		postnum = request.POST.get('postType')

		# 如果没有，直接新建。如果有，则添加
		# 	isLast = request.POST.get('isLast')
		# 	if isLast:
		# 		newpost = Post.objects.create(type=postnum, isLast=True)
		if postnum.isnumeric():  # 有上传posttype， 往posttype增加image
			post = Post.objects.get(type=postnum, person=p)
		else:  # 未上传posttype， 新建post
			n= Post.objects.filter(person=p).count()
			# n = p.posts.count()
			post = Post.objects.create(type=n + 1, person=p)
		# Image保存生成path
		handle_file(request, p, post)

	# 	# post数目相等时，不创建新post，只更新最后post
	# 	if postnum == p.posts.count():
	# 		post = p.posts.last()
	# 		#更新post的图片 handleFile(request, person)

	return HttpResponse("good " + pk)


# 患者详细信息展示
def person_detail(request, pk):
	p = Person.objects.get(pk=pk)
	name = p.name

	picurl = ''
	if p.icon:
		picurl = p.icon
		print(picurl)

	posts = p.posts

	contex = {'patient': p, 'picurl': picurl, 'posts': posts}

	return render(request, 'detail.html', contex)


def wrong(request):
	return HttpResponse('wrong.html')
