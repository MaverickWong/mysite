# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.db.models import ProtectedError
from boards.models import Person, Tag, Post, Image
from record.models import Record
from mysite.settings import BASE_DIR
from datetime import datetime
import os
import json
from PIL import Image as Image2
# from Pillow import Image as Image2


import mimetypes, zipfile
from django.utils.encoding import smart_str
# from django.utils.encoding import escape_uri_path
from linkedcare.syncDB import logIn, get_ortho_record_of_patient, get_baseinfo_of_patient
from linkedcare.getXrayofLinked import getXrayOfperson
import django.dispatch
from django.dispatch import receiver

# Create your views here.
# TODO 高级用户名是zdl

sep = '_'
# 新信号
post_upload_done = django.dispatch.Signal(providing_args=['post_pk'])
person_created = django.dispatch.Signal(providing_args=['person_pk'])


def home(request):
	return HttpResponse('boards, ok')


@login_required()
def down_zip(request, pk):
	"""
    查询person的所有image，根据地址打包所有文件到zip文件
    """
	# todo 下载文件夹可能有两个
	p = Person.objects.get(pk=pk)
	# source_dir = BASE_DIR + '/' + p.privateDir
	output_filename = '/tmp/all.zip'
	zipf = zipfile.ZipFile(output_filename, 'w')  # zip文件

	imgs = p.images.all()
	for img in imgs:
		pathfile = BASE_DIR + img.path  # 要打包的文件
		if os.path.exists(pathfile):
			# 在zip中的相对路径
			relative_path = os.path.basename(os.path.dirname(pathfile))
			arcname = relative_path + os.path.sep + os.path.basename(pathfile)
			zipf.write(pathfile, arcname)
	zipf.close()

	'''
     zipf = zipfile.ZipFile(output_filename, 'w')
    pre_len = len(os.path.dirname(source_dir))
    for parent, dirnames, filenames in os.walk(source_dir):
        for filename in filenames:
            if ('small' in filename) or ( 'medium' in filename):
                # 去除small， medium 文件
                continue
            pathfile = os.path.join(parent, filename) # 要打包的文件
            arcname = pathfile[pre_len:].strip(os.path.sep)  # 在zip中的相对路径
            zipf.write(pathfile, arcname)
    zipf.close()
    '''

	content_type, encoding = mimetypes.guess_type(str(output_filename))
	content_type = content_type or 'application/octet-stream'

	try:
		f = open(output_filename, 'rb')
		response = FileResponse(f, content_type=content_type)
		# response['Content-Disposition'] = 'attachment;filename="example.tar.gz"'
		response['Content-Disposition'] = 'attachment; filename="' + smart_str(p.name) + '.zip"'
		# response['Content-Disposition'] = 'attachment;filename="{0}"'.format(p.name.encode('utf-8'))

		return response
	except IOError:
		return HttpResponse(" 无法打开该文件，请检查文件名 ")


def down_mid_zip(request, pk):
	"""
    查询person的所有image，根据地址打包所有文件到zip文件
    """
	# todo 下载文件夹可能有两个
	p = Person.objects.get(pk=pk)
	# source_dir = BASE_DIR + '/' + p.privateDir
	output_filename = '/tmp/all.zip'
	zipf = zipfile.ZipFile(output_filename, 'w')  # zip文件

	imgs = p.images.all()
	for img in imgs:
		pathfile = BASE_DIR + img.size_m  # 要打包的文件
		if os.path.exists(pathfile):
			# 在zip中的相对路径
			relative_path = os.path.basename(os.path.dirname(pathfile))
			arcname = relative_path + os.path.sep + os.path.basename(pathfile)
			zipf.write(pathfile, arcname)
	zipf.close()

	content_type, encoding = mimetypes.guess_type(str(output_filename))
	content_type = content_type or 'application/octet-stream'

	try:
		f = open(output_filename, 'rb')
		response = FileResponse(f, content_type=content_type)
		# response['Content-Disposition'] = 'attachment;filename="example.tar.gz"'
		response['Content-Disposition'] = 'attachment; filename="' + smart_str(p.name) + '.zip"'
		# response['Content-Disposition'] = 'attachment;filename="{0}"'.format(p.name.encode('utf-8'))

		return response
	except IOError:
		return HttpResponse(" 无法打开该文件，请检查文件名 ")


def down_post_mid_zip(requet, postpk):
	# todo 下载文件夹可能有两个
	p = Post.objects.get(pk=postpk)
	# source_dir = BASE_DIR + '/' + p.privateDir
	output_filename = '/tmp/all.zip'
	zipf = zipfile.ZipFile(output_filename, 'w')  # zip文件

	imgs = p.images.all()
	for img in imgs:
		pathfile = BASE_DIR + img.size_m  # 要打包的文件
		if os.path.exists(pathfile):
			# 在zip中的相对路径
			relative_path = os.path.basename(os.path.dirname(pathfile))
			arcname = relative_path + os.path.sep + os.path.basename(pathfile)
			zipf.write(pathfile, arcname)
	zipf.close()

	content_type, encoding = mimetypes.guess_type(str(output_filename))
	content_type = content_type or 'application/octet-stream'

	try:
		f = open(output_filename, 'rb')
		response = FileResponse(f, content_type=content_type)
		# response['Content-Disposition'] = 'attachment;filename="example.tar.gz"'
		response['Content-Disposition'] = 'attachment; filename="' + str(p.id) + '.zip"'
		# response['Content-Disposition'] = 'attachment;filename="{0}"'.format(p.name.encode('utf-8'))

		return response
	except IOError:
		return HttpResponse(" 无法打开该文件，请检查文件名 ")


def down_post_zip(requet, postpk):
	# todo 下载文件夹可能有两个
	p = Post.objects.get(pk=postpk)
	# source_dir = BASE_DIR + '/' + p.privateDir
	output_filename = '/tmp/all.zip'
	zipf = zipfile.ZipFile(output_filename, 'w')  # zip文件

	imgs = p.images.all()
	for img in imgs:
		pathfile = BASE_DIR + img.path  # 要打包的文件
		if os.path.exists(pathfile):
			# 在zip中的相对路径
			relative_path = os.path.basename(os.path.dirname(pathfile))
			arcname = relative_path + os.path.sep + os.path.basename(pathfile)
			zipf.write(pathfile, arcname)
	zipf.close()

	content_type, encoding = mimetypes.guess_type(str(output_filename))
	content_type = content_type or 'application/octet-stream'

	try:
		f = open(output_filename, 'rb')
		response = FileResponse(f, content_type=content_type)
		# response['Content-Disposition'] = 'attachment;filename="example.tar.gz"'
		response['Content-Disposition'] = 'attachment; filename="' + str(p.id) + '.zip"'
		# response['Content-Disposition'] = 'attachment;filename="{0}"'.format(p.name.encode('utf-8'))

		return response
	except IOError:
		return HttpResponse(" 无法打开该文件，请检查文件名 ")



def get_person_list_from_stringlist(string):
	if string:
		person_list = []
		list = string.split(';')
		list2 = []
		for l in list:  # 去重
			if l not in list2:
				list2.append(l)

		for l in list2:
			p = Person.objects.get(pk=int(l))
			person_list.append(p)
		return person_list
	else:
		return None


def get_last_person_pk_from_stringlist(string):
	if string:
		if string.find(';'):
			list = string.split(';')
			return list[-1]
		else:
			return string
	else:
		return None


@login_required()
def person_detail(request, pk):
	person_list = ''

	# session
	today = datetime.today().strftime('%Y%m%d')
	if request.session.get('date_of_list', None) == today:
		if request.session.get('person_list', None):
			list = request.session['person_list']
			person_list = list + ';' + str(pk)
			request.session['person_list'] = person_list
		else:
			person_list = str(pk)
			request.session['person_list'] = person_list
	else:
		request.session['date_of_list'] = today
		person_list = str(pk)
		request.session['person_list'] = person_list

	today_person_list = get_person_list_from_stringlist(person_list)

	p = Person.objects.get(pk=pk)
	name = p.name

	picurl = ''
	if p.icon:
		picurl = p.icon

	yky = 'https://simaier.linkedcare.cn/#/patient/info/' + str(p.linkedcareId) + '/record'

	posts = p.posts
	num_post = posts.count()
	num_xray = Post.objects.filter(type__gte=99).filter(person=p).count()
	num_record = Record.objects.filter(person=p).count()

	contex = {'patient': p, 'posts': posts, 'first_tab': 0, 'ykyurl': yky,
	          'today_person_list': today_person_list,
	          'num_xray': num_xray, 'num_record': num_record, 'num_post': num_post,
	          }

	if request.GET.get('tab'):
		t = request.GET.get('tab')
		contex = {'patient': p, 'posts': posts, 'first_tab': t,
		          'ykyurl': yky, 'today_person_list': today_person_list,
		          'num_xray': num_xray, 'num_record': num_record, 'num_post': num_post, }

	return render(request, 'boards/detail.html', contex)


@login_required()
def today_person_detail(request):
	# session
	today = datetime.today().strftime('%Y%m%d')
	if request.session.get('date_of_list', None) == today:
		person_list = request.session['person_list']
	else:
		# request.session['date_of_list'] = today
		person_list = ''

	today_person_list = get_person_list_from_stringlist(person_list)
	i = get_last_person_pk_from_stringlist(person_list)
	if i:
		p = Person.objects.get(pk=int(i))
	else:
		p = Person.objects.first()

	posts = p.posts
	num_xray = Post.objects.filter(type__gte=99).filter(person=p).count()

	contex = {'patient': p, 'posts': posts, 'first_tab': 0,
	          'today_person_list': today_person_list,
	          'num_xray': num_xray,
	          }

	if request.GET.get('tab'):
		t = request.GET.get('tab')
		contex = {'patient': p, 'posts': posts, 'first_tab': t,
		          'today_person_list': today_person_list,
		          'num_xray': num_xray, }

	return render(request, './boards/detail.html', contex)


@login_required()
def person_detail_without_sidebar(request, pk):
	p = Person.objects.get(pk=pk)
	picurl = ''
	if p.icon:
		picurl = p.icon

	yky = 'https://simaier.linkedcare.cn/#/patient/info/' + str(p.linkedcareId) + '/record'

	posts = p.posts

	contex = {'patient': p, 'posts': posts, 'first_tab': 0, 'ykyurl': yky}

	if request.GET.get('tab'):
		t = request.GET.get('tab')
		contex = {'patient': p, 'posts': posts, 'first_tab': t,
		          'ykyurl': yky}

	return render(request, 'boards/detail.html', contex)


@login_required()
def delperson(request, pk):
	p = Person.objects.get(pk=pk)
	p.delete()
	return redirect('home')


# TODO
@login_required()
def delpost(request, ppk, postpk):
	# try:
	po = Post.objects.get(pk=postpk)
	po.delete()
	# except ProtectedError:
	#     err = "无法删除该复诊"
	#     return  HttpResponse(err)
	# pk = int(ppk)
	# return HttpResponseRedirect( reverse('person_detail', args=(ppk)) )
	return redirect('posts', ppk)


def save_upload_file_make_logo(file, dir):
	# 保存文件
	logoPath = dir + 'logo.jpg'
	if os.path.exists(logoPath):
		ff = open(logoPath, 'wb+')
		for chunk in file.chunks():
			ff.write(chunk)
		ff.close()

		# 制作缩略图函数
		im = Image2.open(logoPath)
		ssize = (400, 400)
		if im:
			try:
				im.thumbnail(ssize)
				im.save(logoPath, "JPEG")
				return logoPath
			except IOError:
				print("cannot create logo")
				# print(IOError)
				return False


# 处理上传文件
def handle_file(request, person, post):
	docname = request.user.username
	files = request.FILES.getlist('files[]')  # 类型为mutilist
	# n = request.POST.get('name')
	sep = '_'  # 文件名中的分隔符

	# 返回结果
	results = {}
	results["files"] = []
	# print(files)

	dt = datetime.now()
	times = dt.strftime("%f")
	datestr = dt.strftime("%Y%m%d")
	year_month_str = dt.strftime("%Y%m")  # b+ year_month_str + '/'
	# static / picture / 张飞_233 /
	dir = 'static/picture/' + docname + '/' + person.name + sep + str(person.idnum) + '/'
	post.dir = dir  # 保存post的文件夹
	post.save()
	# 保存到person作为私人文件夹
	if person.privateDir:
		if person.privateDir[-1] == '/':  # 检查末尾是否有 '/'，如果没有，添加
			dir = person.privateDir + year_month_str + '/'
		else:
			dir = person.privateDir + '/' + year_month_str + '/'
	else:
		person.privateDir = dir
		person.save()

	if dir[0] == '/':  # 检查开头是否有 '/'，如果有，则去除
		dir = dir[1:]
	# icondir = dir  + 'small' + '/'
	if not dir[-1] == '/':  # 检查末尾是否有 '/'，如果没有，添加
		dir = dir + '/'

	# TODO 相对目录有时容易出问题
	dir = os.path.join(BASE_DIR, dir)

	icondir = dir
	mediumdir = dir
	if not os.path.exists(dir):
		os.makedirs(dir)
	if not os.path.exists(icondir):
		os.makedirs(icondir)
	if not os.path.exists(mediumdir):
		os.makedirs(icondir)

	i = 0
	for f in files:
		# 文件名及路径
		n2 = f.name
		suf = n2.split('.')[-1]
		# suf = 'jpg'
		# 文件名   张飞_20180101_S0_041411.jpg
		fname = person.name + sep + datestr + sep + 'S' + str(post.type) + sep + str(i) + times + '.' + suf
		# 相对全路径 static / picture / 张飞_233 / 张飞_20180101_041411.jpg
		path = dir + fname
		iconpath = icondir + 'small_' + fname
		mediumpath = mediumdir + 'medium_' + fname

		# 保存文件
		ff = open(path, 'wb+')
		for chunk in f.chunks():
			ff.write(chunk)
		ff.close()
		i = i + 1

		# 制作缩略图函数
		if os.path.exists(path):
			# im = Image2.open(path)
			# ssize = (400, 400)
			# msize = (1200, 1200)
			# if im:
			# 	try:
			# 		im.thumbnail(msize)
			# 		im.save(mediumpath)
			# 		im.thumbnail(ssize)
			# 		im.save(iconpath)
			#
			# 	except IOError:
			# 		print("cannot create thumbnail")

			# 2020.12.25增加图像旋转
			im = Image2.open(path)
			from PIL import ExifTags
			if im:
				try:
					for orientation in ExifTags.TAGS.keys():
						if ExifTags.TAGS[orientation] == 'Orientation':
							break

					exif = dict(im._getexif().items())
					if exif[orientation] == 3:
						im = im.rotate(180, expand=True)

					elif exif[orientation] == 6:
						im = im.rotate(270, expand=True)

					elif exif[orientation] == 8:
						im = im.rotate(90, expand=True)
				except:
					print("cannot rotate")

				ssize = (400, 400)
				msize = (1200, 1200)
				try:
					im.thumbnail(msize)
					im.save(mediumpath)
					im.thumbnail(ssize)
					im.save(iconpath)

				except IOError:
					print("cannot create thumbnail")

		# 制作url，及保存到数据库
		path = path.replace(BASE_DIR, '')
		iconpath = iconpath.replace(BASE_DIR, '')
		mediumpath = mediumpath.replace(BASE_DIR, '')

		if not path[0] == '/':  # 检查开头是否有 '/'，如果有，则去除
			pathU = '/' + path
		else:
			pathU = path
		if not iconpath[0] == '/':  # 检查开头是否有 '/'，如果有，则去除
			iconpathU = '/' + iconpath
		else:
			iconpathU = iconpath
		if not mediumpath[0] == '/':  # 检查开头是否有 '/'，如果有，则去除
			mediumpathU = '/' + mediumpath
		else:
			mediumpathU = mediumpath

		# 保存到image
		image = Image.objects.create(path=pathU, thumbnail=iconpathU, post=post, person=person, size_m=mediumpathU)

		# 添加头像
		# if post.type ==0 and i ==1:
		#     person.icon = iconpathU
		#     person.save()
		# if dir[0] == '/': #  检查开头是否有 '/'，如果有，则去除
		#     dir = dir[1:]

		path = BASE_DIR + path
		# 返回上传信息
		if os.path.exists(path):  # 再次确认文件是否保存
			t1 = "上传成功:  " + fname
		else:
			t1 = "服务器保存失败"
		info = {
			"name": t1,
			"size": os.path.getsize(path),
			"url": path,
			"thumbnailUrl": iconpathU,
			"deleteUrl": '',
			"deleteType": "DELETE", }
		results["files"].append(info)

	return results


@login_required()
def new_person(request):
	# board = get_object_or_404(Board, pk=pk)
	if request.method == 'POST':
  
		docname = request.user.username
		# message = request.POST['ID']
		tag_list = request.POST['newTags']
		name = request.POST['name']
		idnum = request.POST['ID']
		# birth = request.POST['nameCode']
		# nameCode=request.POST['nameCode']
		# 设定文件夹
		try:
			sex = request.POST['sex']
		except:
			sex = 0

		# dir = 'static/picture/' + name + '_' + idnum + '/'
		# 根据每个医生user名生成文件夹

		docDir = 'static/picture/' + docname + '/'
		# docDir = doc.encode('utf-8')
		if not os.path.exists(docDir):
			os.makedirs(docDir)
		#  创建privateDir
		# privateDir = docDir + name + sep + str(idnum) + '/'
		privateDir = docDir + name + sep + str(idnum) + '/'

		if not os.path.exists(privateDir):
			os.makedirs(privateDir)

		if Person.objects.filter(name=name, idnum=idnum, doctor=docname).exists():
			return redirect('boards:wrong')
		else:
			person = Person.objects.create(name=name, idnum=idnum, doctor=docname, privateDir=privateDir)
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
			try:
				person.mobile = request.POST['mobile']
				person.save()
				person.nameCode = request.POST['nameCode']
				person.save()
				person.email = request.POST['email']
				person.save()
				person.QQ = request.POST['QQ']
				person.save()
				person.weixin = request.POST['weixin']
				person.save()
				person.occupation = request.POST['occupation']
				person.save()
				person.identityCard = request.POST['identityCard']
				person.save()
				person.homeAddress = request.POST['homeAddress']
				person.save()
				person.linkedcareId = request.POST['linkedcareId']
				person.save()
				person.sex = request.POST['sex']
				person.save()
			except:
				pass

		# post = Post.objects.create(type=0, isFirst=1, person=person)

		# 处理上传图像，当做logo
		files = request.FILES.getlist('files[]')  # 类型为mutilist
		if files:
			# logoPath = privateDir + 'logo.jpg'
			path = save_upload_file_make_logo(files[0], privateDir)
			if path:
				person.icon = path
				person.save()

		# 处理新增tags
		new_tag_list = tag_list.split(' ')
		if new_tag_list:
			for t in new_tag_list:
				tags = Tag.objects.filter(name=t)
				if tags.count() == 1:  # 查到一个
					tags[0].persons.add(person)
					tags[0].save()
				elif tags.count() == 0:  # 未查到
					tag2 = Tag.objects.create(name=t, type=101)
					tag2.persons.add(person)
					tag2.save()

		#  发送新建患者信号
		person_created.send(new_person, person_pk=person.pk)
		# result2 = json.dumps(results)
		return redirect('boards:person_detail', person.pk)

	if request.method == 'GET':
		tgroups = []
		for i in range(10):
			tgroup = Tag.objects.filter(type=i)
			tgroups.append(tgroup)
		tags = Tag.objects.all()
		return render(request, 'boards/newPerson.html', {'tgroups': tgroups, "tags": tags})


# 新建患者之后，导入患者信息，x线，病历等后续
@receiver(person_created, sender=new_person)
def person_created_todo(sender, **kwargs):
	# person_pk = kwargs['person_pk']
	# p = Person.objects.get(pk=person_pk)
	#
	# print('新建患者完成后开始导入其他信息')
	# s = logIn()
	# get_baseinfo_of_patient(s, p)
	# get_ortho_record_of_patient(s, p)
	# getXrayOfperson(s, p)

	return None


# 上传x线功能
def addpost_xray(request, pk):
	"""
        添加x线图片post
        :param request:
        :param pk:
        :return:
        """
	p = Person.objects.get(pk=pk)

	if request.method == 'GET':
		# TODO 应该获取posts总数，然后发到网页内部
		tags = Tag.objects.all()
		# print(tags)
		return render(request, 'boards/addpost_xray.html', {'patient': p})

	if request.method == 'POST':
		# p = Person.objects.get(pk=pk)
		postnum = request.POST.get('postType')
		tag_list = request.POST['newTags']
		comment = request.POST['comment']

		# 如果没有，直接新建
		if postnum.isnumeric():  # 有上传posttype， 往post type增加image
			i = Post.objects.filter(type=postnum, person=p, type__gte=100).count()
			if i == 0:
				post = Post.objects.create(type=postnum, person=p, comment=comment, name=comment)
			elif i == 1:
				post = Post.objects.get(type=postnum, person=p, comment=comment, name=comment)
		else:  # 未上传posttype， 新建post，type+1
			n = Post.objects.filter(person=p, type__gte=100).count()
			post = Post.objects.create(type=100 + n + 1, person=p, comment=comment, name=comment)
		# Image保存生成path
		results = handle_file(request, p, post)

		# 处理新增tags
		new_tag_list = tag_list.split(' ')
		if new_tag_list:
			add_tag_from_string_for_person(new_tag_list, p)

		result2 = json.dumps(results)
		return HttpResponse(result2, content_type='application/json')


# return HttpResponse("暂未开放上传x线功能")


def addpost(request, pk):
	"""
    添加普通图片post
    :param request:
    :param pk:
    :return:
    """
	p = Person.objects.get(pk=pk)

	if request.method == 'GET':
		# TODO 应该获取posts总数，然后发到网页内部
		# tgroups = []
		# for i in range(10):
		#     tgroup = Tag.objects.filter(type=i)
		#     tgroups.append(tgroup)
		tags = Tag.objects.all()
		# print(tags)
		return render(request, 'boards/addpost.html', {'patient': p, "tags": tags})

	if request.method == 'POST':
		# p = Person.objects.get(pk=pk)
		postnum = request.POST.get('postType')
		tag_list = request.POST['newTags']
		comment = request.POST['comment']

		# 如果没有，直接新建
		if postnum.isnumeric():  # 有上传posttype， 往post type增加image
			i = Post.objects.filter(type=postnum, person=p).count()
			if i == 0:
				post = Post.objects.create(type=postnum, person=p, comment=comment, name=comment)
			elif i == 1:
				post = Post.objects.get(type=postnum, person=p, comment=comment, name=comment)
		else:  # 未上传posttype， 新建post，type+1
			n = Post.objects.filter(person=p).count()
			post = Post.objects.create(type=n + 1, person=p, comment=comment, name=comment)
		# Image保存生成path
		results = handle_file(request, p, post)

		# 处理新增tags
		new_tag_list = tag_list.split(' ')
		if new_tag_list:
			add_tag_from_string_for_person(new_tag_list, p)

		result2 = json.dumps(results)

		# 发送完成信号，进行后续处理
		post_upload_done.send(addpost, post_pk=post.pk)

		return HttpResponse(result2, content_type='application/json')


# return HttpResponse('{"status":"success"}', content_type='application/json')


@receiver(post_upload_done, sender=addpost)
def post_upload_done_func(sender, **kwargs):
	'''
    上传后处理函数，
    :param sender: 
    :param kwargs: 
    :return: 
    '''
	print('upload done!')


def add_tag_from_string_for_person(new_tag_list, p):
	for t in new_tag_list:
		if not t == '':
			tags = Tag.objects.filter(name=t)
			if tags.count() == 1:  # 查到一个
				tags[0].persons.add(p)
				tags[0].save()
			elif tags.count() == 0:  # 未查到
				tag2 = Tag.objects.create(name=t, type=101)
				tag2.persons.add(p)
				tag2.save()


@login_required()
def posts(request, pk):
	"""
    获取所有患者的所有 普通post
    :param request:
    :param pk:
    :return:
    """
	p = Person.objects.get(pk=pk)
	name = p.name

	picurl = ''
	if p.icon:
		picurl = p.icon
		print(picurl)

	posts = p.posts.filter(type__lte=99).order_by('-type')
	contex = {'patient': p, 'posts': posts}

	return render(request, 'boards/posts_in_detail.html', contex)


def posts_xray(request, pk):
	"""
    # 所有x线post（原易看牙导入图像）
    :param request:
    :param pk:
    :return:
    """
	p = Person.objects.get(pk=pk)
	name = p.name

	picurl = ''
	if p.icon:
		picurl = p.icon
		print(picurl)

	posts = p.posts.filter(type__gte=100)
	contex = {'patient': p, 'posts': posts, 'isXray': True}

	return render(request, 'boards/posts_in_detail.html', contex)


def wrong(request):
	return render(request, 'boards/wrong.html', {})


def get_tag_groups():
	tgroups = []
	for i in range(10):
		tgroup = Tag.objects.filter(type=i)
		tgroups.append(tgroup)
	return tgroups


def add_tag_for_person(request, pk):
	if request.method == 'POST':
		p = get_object_or_404(Person, pk=pk)
		# postnum = request.POST.get('postType')
		tag_list = request.POST['s']
		# comment = request.POST['comment']

		# 处理新增tags
		new_tag_list = tag_list.split(' ')
		if new_tag_list:
			add_tag_from_string_for_person(new_tag_list, p)

		return redirect('boards:person_detail', pk)

	else:
		p = get_object_or_404(Person, pk=pk)
		tgroups = get_tag_groups()
		tags = Tag.objects.all()

		return render(request, 'tag/add_tag.html', {'patient': p, 'tags': tags, 'tgroups': tgroups})
