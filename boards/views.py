# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
import json
import os
import re
import json
from PIL import Image as Image2


from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from boards.models import *
from datetime import date, time, datetime
import os


# Create your views here.
def home(request):
	persons = Person.objects.all()
	tags = Tag.objects.all()
	return render(request, 'index.html', {'persons': persons, 'tags':tags})

def test(request):
	return HttpResponse("good")

def search(request):
	s = request.GET['s']
	if s.isnumeric():
		persons = Person.objects.filter(idnum=s)
	else:
		persons = Person.objects.filter(name__contains=s)

	return render(request, 'search.html', {'persons': persons})

def tag_search(request, tag):
	ut = unicode(tag)
	t = Tag.objects.get(name=ut)
	ps= t.persons.all()
	return render(request, 'search.html', {'persons': ps})


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

		# 制作缩略图函数
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
		if post.type ==0 and i ==1:
			person.icon = path
			person.save()
		# 保存到image
		image = Image.objects.create(path=path, thumbnail=iconpath, post=post, person=person)

		# info = {
		# 	"name": path,
		# 	"size": 111,
		# 	"url": '',
		# 	"thumbnailUrl": '',
		# 	"deleteUrl": '',
		# 	"deleteType": "DELETE", }
		#
		# result = {}
		# result["files"] = [{
		# 	"name": '图片',
		# 	"size": 111,
		# 	"url": '',
		# 	"thumbnailUrl": '',
		# 	"deleteUrl": '',
		# 	"deleteType": "DELETE", }]

	return 1


def new_person(request):
	# board = get_object_or_404(Board, pk=pk)
	if request.method == 'POST':

		# message = request.POST['ID']
		# user = User.objects.first()  # TODO: 临时使用一个账号作为登录用户
		name = unicode( request.POST['name'])
		idnum = request.POST['ID']
		tag_list = request.POST['newTags']

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

		# 处理新增tags
		new_tag_list = tag_list.split(' ')
		if new_tag_list:
			for t in new_tag_list:
				tags = Tag.objects.filter(name__contains=t)
				if tags.count() == 1: # 查到一个
					tags[0].persons.add(person)
					tags[0].save()
				elif tags.count() ==0: # 未查到
					tag2 = Tag.objects.create(name=t)
					tag2.persons.add(person)
					tag2.save()

		return redirect('home')  # TODO: redirect to the created topic page

	if request.method == 'GET':
		tags = Tag.objects.all()
		return render(request, 'upload/index.html', {"tags":tags})


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
	# generating json response array
	result = {}
	result["files"]=[{
		"name": '图片',
        "size": 111,
        "url": '',
        "thumbnailUrl": '',
        "deleteUrl": '',
        "deleteType": "DELETE", }]
	# response_data = simplejson.dumps(result)
	result2 = json.dumps(result)
	return HttpResponse(result2,  content_type='application/json')

	# return HttpResponse('{"status":"success"}', content_type='application/json')


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
	return render(request, 'upload/wrong.html',{})
