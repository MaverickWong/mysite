# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect

from boards.models import *

from datetime import date, time, datetime
import os
import json
from PIL import Image as Image2

# Create your views here.
@login_required()
def home(request):
	if request.user.is_authenticated:
		persons = Person.objects.all()
		tags = Tag.objects.all()
		return render(request, 'index.html', {'persons': persons, 'tags':tags})
	else:
		return redirect('login')

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

def delperson(request, pk):
	p = Person.objects.get(pk=pk)
	p.delete()
	return redirect('home')

def delpost(request,ppk,postpk):
	po = Post.objects.get(pk=postpk)
	po.delete()
	# pk = int(ppk)
	# return HttpResponseRedirect( reverse('person_detail', args=(ppk)) )
	return redirect('person_detail', ppk)


def handle_file(request, person, post):
	files = request.FILES.getlist('files[]')  # 类型为mutilist
	# n = request.POST.get('name')
	results = {}
	results["files"] = []
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
		fname= person.name + '.p' + str(post.type) + '.' + str(i) + time + '.' + suf
		path = dir + fname
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
			size = (400, 400)
			if im:
				try:
					# im = Image.open(infile)
					im.thumbnail(size)
					im.save(iconpath, "JPEG")
				except IOError:
					print("cannot create thumbnail")

		pathU = '../' + path
		iconpath = '../' +iconpath
		if post.type ==0 and i ==1:
			person.icon = iconpath
			person.save()
		# 保存到image
		image = Image.objects.create(path=pathU, thumbnail=iconpath, post=post, person=person)

		# 上传后返回信息
		if os.path.exists(path): # 再次确认文件是否保存
			t1 = "文件名称:  " + fname
		else:
			t1 ="服务器保存失败"

		info = {
			"name": t1,
			"size": os.path.getsize(path),
			"url": pathU,
			"thumbnailUrl": iconpath,
			"deleteUrl": '',
			"deleteType": "DELETE", }
		results["files"].append(info)

	return results


def new_person(request):
	# board = get_object_or_404(Board, pk=pk)
	if request.method == 'POST':

		# message = request.POST['ID']
		# user = User.objects.first()  # TODO: 临时使用一个账号作为登录用户
		name = unicode( request.POST['name'])
		idnum = request.POST['ID']
		tag_list = request.POST['newTags']

		if Person.objects.filter(name=name, idnum=idnum).exists():
			return redirect('wrong')
		else:
			person = Person.objects.create(name=name, idnum=idnum)

		post = Post.objects.create(type=0, isFirst=1, person=person)

		# 处理上传文件
		results = handle_file(request, person, post)

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

		result2 = json.dumps(results)
		return HttpResponse(result2, content_type='application/json')

	if request.method == 'GET':
		tags = Tag.objects.all()
		return render(request, 'upload/index.html', {"tags":tags})


def addpost(request, pk):
	p = Person.objects.get(pk=pk)

	if request.method == 'GET':
		# TODO 应该获取posts总数，然后发到网页内部
		tags = Tag.objects.all()
		print(tags)
		return render(request, 'upload/addpost.html', {'patient': p}, {"tags":tags})

	if request.method == 'POST':
		# p = Person.objects.get(pk=pk)
		postnum = request.POST.get('postType')
		tag_list = request.POST['newTags']

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
		results = handle_file(request, p, post)

	# 	# post数目相等时，不创建新post，只更新最后post
	# 	if postnum == p.posts.count():
	# 		post = p.posts.last()
	# 		#更新post的图片 handleFile(request, person)
		# 处理新增tags
		new_tag_list = tag_list.split(' ')
		if new_tag_list:
			for t in new_tag_list:
				tags = Tag.objects.filter(name__contains=t)
				if tags.count() == 1:  # 查到一个
					tags[0].persons.add(p)
					tags[0].save()
				elif tags.count() == 0:  # 未查到
					tag2 = Tag.objects.create(name=t)
					tag2.persons.add(p)
					tag2.save()

		result2 = json.dumps(results)
		return HttpResponse(result2,  content_type='application/json')

	# return HttpResponse('{"status":"success"}', content_type='application/json')


# 患者详细信息展示
@login_required()
def person_detail(request, pk):
	p = Person.objects.get(pk=pk)
	name = p.name

	picurl = ''
	if p.icon:
		picurl = p.icon
		print(picurl)

	posts = p.posts

	contex = {'patient': p,  'posts': posts}

	return render(request, 'detail.html', contex)


def wrong(request):
	return render(request, 'upload/wrong.html',{})
