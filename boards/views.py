# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# from django.core.urlresolvers import reverse
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import ProtectedError
from boards.models import *

from datetime import date, time, datetime
import os
import json
from PIL  import Image as Image2

# Create your views here.
# TODO 高级用户名是zdl

def test(request):
    return HttpResponse("good")

def search(request):
    docname = request.user.username
    s = request.GET['s']
    if s.isnumeric(): # 搜索内容是数字
        if docname == 'zdl':
            persons = Person.objects.filter(idnum__contains=s)
        else:
            persons = Person.objects.filter(idnum__contains=s, doctor=docname)
    else: # 搜索内容不是数字
        if docname == 'zdl':
            persons = Person.objects.filter(name__contains=s)
        else:
            persons = Person.objects.filter(name__contains=s, doctor=docname)

    return render(request, 'search.html', {'persons': persons})

def tag_search(request, tag):
    docname = request.user.username
    ut = str(tag)
    t = Tag.objects.get(name=ut)
    if docname == 'zdl':
        ps = t.persons.all()
    else:
        ps= t.persons.filter(doctor=docname)
    return render(request, 'search.html', {'persons': ps})



def delperson(request, pk):
    p = Person.objects.get(pk=pk)
    p.delete()
    return redirect('home')

# TODO
def delpost(request,ppk,postpk):
    # try:
    po = Post.objects.get(pk=postpk)
    po.delete()
    # except ProtectedError:
    #     err = "无法删除该复诊"
    #     return  HttpResponse(err)
    # pk = int(ppk)
    # return HttpResponseRedirect( reverse('person_detail', args=(ppk)) )
    return redirect('posts', ppk)

# 处理上传文件
def handle_file(request, person, post):
    files = request.FILES.getlist('files[]')  # 类型为mutilist
    # n = request.POST.get('name')
    sep = '_' #  文件名中的分隔符
    results = {}
    results["files"] = []
    print(files)

    i = 0
    for f in files:
        dt = datetime.now()
        time = dt.strftime("%f")

        dir = 'static/picture/' + person.name + sep + str(person.idnum) + '/'
        post.dir = dir # 保存post的文件夹
        post.save()
        # 保存到person作为私人文件夹
        if person.privateDir:
            dir = person.privateDir
        else:
            person.privateDir = dir
            person.save()

        icondir = dir  + 'small' + '/'
        if not os.path.exists(dir):
            os.mkdir(dir)
        if not os.path.exists(icondir):
            os.mkdir(icondir)

        n2 = f.name
        suf = n2.split('.')[-1]
        fname= person.name + sep+ 'S' + str(post.type) + sep + str(i) + time + '.' + suf
        path = dir + fname
        #  static / picture / 张飞_233 / 张飞_S0_041411.jpg
        iconpath = icondir + 'small'+sep + person.name + sep+ 'S' + str(post.type) + sep   +str(i) + time + '.' + suf
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

        pathU = '/' + path
        iconpathU = '/' +iconpath
        if post.type ==0 and i ==1:
            person.icon = iconpathU
            person.save()
        # 保存到image
        image = Image.objects.create(path=pathU, thumbnail=iconpathU, post=post, person=person)

        # 上传后返回信息
        if os.path.exists(path): # 再次确认文件是否保存
            t1 = "文件名称:  " + fname
        else:
            t1 ="服务器保存失败"

        info = {
            "name": t1,
            "size": os.path.getsize(path),
            "url": path,
            "thumbnailUrl": iconpathU,
            "deleteUrl": '',
            "deleteType": "DELETE", }
        results["files"].append(info)

    return results


def new_person(request):
    # board = get_object_or_404(Board, pk=pk)
    if request.method == 'POST':
        docname = request.user.username
        # message = request.POST['ID']
        tag_list = request.POST['newTags']
        name = request.POST['name']
        idnum = request.POST['ID']
        # sex = request.POST['sex']
        # birth = request.POST['nameCode']
        # nameCode=request.POST['nameCode']
        # 设定文件夹
        dir = 'static/picture/' + name + '_' + idnum + '/'

        if Person.objects.filter(name=name, idnum=idnum, doctor=docname).exists():
            return redirect('wrong')
        else:
            person = Person.objects.create(name=name, idnum=idnum, doctor=docname, privateDir=dir)
            # TODO 添加新患者信息
            # person = Person.objects.create(name=name,
            #                                idnum=idnum,
            #                                doctor=docname,
            #                                mobile=request.POST['mobile'],
            #                                nameCode=request.POST['nameCode'],
            #                                email=request.POST['email'],
            #                                QQ=request.POST['QQ'],
            #                                weixin=request.POST['weixin'],
            #                                occupation=request.POST['occupation'],
            #                                identityCard=request.POST['identityCard'],
            #                                homeAddress=request.POST['homeAddress'],
            #                                linkedcareId=request.POST['linkedcareId']
            #                                )


        # post = Post.objects.create(type=0, isFirst=1, person=person)

        # 处理上传文件
        # results = handle_file(request, person, post)

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

        # result2 = json.dumps(results)
        return redirect('person_detail', person.pk)

    if request.method == 'GET':
        tags = Tag.objects.all()
        return render(request, 'upload/newPerson.html', {"tags":tags})


def addpost(request, pk):
    p = Person.objects.get(pk=pk)

    if request.method == 'GET':
        # TODO 应该获取posts总数，然后发到网页内部
        tags = Tag.objects.all()
        print(tags)
        return render(request, 'upload/addpost.html', {'patient': p, "tags":tags})

    if request.method == 'POST':
        # p = Person.objects.get(pk=pk)
        postnum = request.POST.get('postType')
        tag_list = request.POST['newTags']

        # 如果没有，直接新建。如果有，则添加
        # 	isLast = request.POST.get('isLast')
        # 	if isLast:
        # 		newpost = Post.objects.create(type=postnum, isLast=True)
        if postnum.isnumeric():  # 有上传posttype， 往posttype增加image
            i = Post.objects.filter(type=postnum, person=p).count()
            if i ==0:
                post = Post.objects.create(type=postnum, person=p)
            elif i ==1:
                post = Post.objects.get(type=postnum, person=p)
        else:  # 未上传posttype， 新建post
            n= Post.objects.filter(person=p).count()
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


# # 患者详细信息展示
# @login_required()
# def person_detail(request, pk):
#     p = Person.objects.get(pk=pk)
#     name = p.name
#
#     picurl = ''
#     if p.icon:
#         picurl = p.icon
#         print(picurl)
#
#     posts = p.posts
#
#     contex = {'patient': p,  'posts': posts}
#
#     # return render(request, 'detail.html', contex)
#     return render(request, 'detail2.html', contex)
#

# 所有图片post
def posts(request, pk):
	p = Person.objects.get(pk=pk)
	name = p.name

	picurl = ''
	if p.icon:
		picurl = p.icon
		print(picurl)

	posts = p.posts

	contex = {'patient': p,  'posts': posts}

	return render(request, 'detail3.html', contex)

def baseinfo(request,pk):
    p = Person.objects.get(pk=pk)
    return render(request,'baseInfo.html', {'person':p})

def wrong(request):
    return render(request, 'upload/wrong.html',{})
