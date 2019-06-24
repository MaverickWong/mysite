from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, FileResponse
from boards.models import Person, Tag, Post, Image
from record.models import Record
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from mysite.settings import BASE_DIR
# import dramatiq

import socket

from linkedcare.syncDB import get_patients_fill_DB, logIn, get_baseinfo_of_patient, add_id_for_person
from linkedcare.getXrayofLinked import getXrayOfperson
from datetime import datetime
from mysite.settings import STATICFILES_DIRS


# @login_required()
def show_home(request):
	return render(request, 'show-index2.html')


@login_required()
def home(request):
	get_client_ip(request)  # 记录ip地址

	docname = request.user.username
	if request.user.is_authenticated:
		if docname == 'zdl':  # 用户名为zdl时，可以查看所有患者[:16]
			persons = Person.objects.order_by('pk').reverse()
			total_person_num = Person.objects.all().count()

		else:  # 只能看该医生的患者
			persons = Person.objects.filter(doctor=docname).order_by('pk')
			total_person_num = Person.objects.filter(doctor=docname).count()

		# 分页
		page = request.GET.get('page', 1)
		paginator = Paginator(persons, 10)
		try:
			topics = paginator.page(page)
		except PageNotAnInteger:
			# fallback to the first page
			topics = paginator.page(1)
		except EmptyPage:
			# probably the user tried to add a page number
			# in the url, so we fallback to the last page
			topics = paginator.page(paginator.num_pages)

		tgroups = []
		for i in range(10):
			tgroup = Tag.objects.filter(type=i)
			tgroups.append(tgroup)
		# tgroups.append(Tag.objects.filter(type=101)) # 添加101其他
		tags = Tag.objects.filter(type=101)

		total_posts_num = Post.objects.all().count()
		total_img_num = Image.objects.all().count()
		tag_count = Tag.objects.all().count()
		total_record_num = Record.objects.all().count()

		contx = {'persons': topics,
		         'total_person_num': total_person_num, 'total_posts_num': total_posts_num,
		         'total_img_num': total_img_num, 'total_record_num': total_record_num,
		         'tgroups': tgroups, 'tags': tags, 'tag_islink': True}

		return render(request, 'index.html', contx)
	else:
		return redirect('login')


def bad(request):
	''' 升级维护用 '''
	return render(request, '404.html')


def summary_index(request):
	docname = request.user.username
	if request.user.is_authenticated:
		if docname == 'zdl':  # 用户名为zdl时，可以查看所有患者[:16]
			total_person_num = Person.objects.all().count()

		else:  # 只能看该医生的患者
			total_person_num = Person.objects.filter(doctor=docname).count()

		# tags = Tag.objects.all()
		total_posts_num = Post.objects.all().count()
		total_img_num = Image.objects.all().count()
		tag_count = Tag.objects.all().count()

		contx = {'total_person_num': total_person_num, 'total_posts_num': total_posts_num,
		         'total_img_num': total_img_num, 'tag_count': tag_count, 'tag_islink': True}
		return render(request, 'index.html', contx)
	else:
		return redirect('login')


def get_host_ip(request):
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(('8.8.8.8', 80))
		ip = s.getsockname()[0]
	finally:
		s.close()

	return HttpResponse(ip)

# from mysite.tasks import mytask
#
# # 所有post统计
# def allposts(request):
#     mytask.delay(2,3)
#     return render(request, 'log_counPostNum0219-152149.html')

# 实验 dramatiq 异步任务
# import dramatiq
# from tasklist.models import Task
def allposts(request):
	# mytask(2,3)
	return render(request, 'log_counPostNum0219-152149.html')


from celery import shared_task

# @dramatiq.actor
# @shared_task
# def sync_db_worker():
#     get_patients_fill_DB(20)
#     return None
from .tasks import sync_db_worker


#  从易看牙同步患者基本信息
def syncDB(request):
	sync_db_worker.delay()
	# get_patients_fill_DB(20)
	return redirect('home')


#  从易看牙同步患者基本信息
def sync_xray_of_linkedcare_for_person(request, pk):
	s = logIn()
	p = Person.objects.get(pk=pk)

	get_baseinfo_of_patient(s, p)
	getXrayOfperson(s, p)
	# uwsgi.reload

	return redirect('boards:person_detail', pk)


def get_client_ip(request):
	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	if x_forwarded_for:
		ip = x_forwarded_for.split(',')[0]
	else:
		ip = request.META.get('REMOTE_ADDR')

	dt = datetime.now()
	t = dt.strftime("%m.%d-%H:%M:%S")
	file = BASE_DIR + '/log/ip.txt'
	with open(file, 'a+') as f:
		f.write('%s\t\t %s\n' % (ip, t))
	return ip


def baidu_sdk(request):
	# find_user(file1path)
	persons = Person.objects.all().order_by('pk').reverse()


def importFolders(request):
	"""
    导入图像文件夹
    """
	import readFoldersWithNameIdDate

	fname = readFoldersWithNameIdDate.start()
	import mimetypes

	content_type, encoding = mimetypes.guess_type(str(fname))
	content_type = content_type or 'application/octet-stream'
	try:
		f = open(fname, 'rb')
		response = FileResponse(f, content_type=content_type)
		response['Content-Disposition'] = 'attachment;filename="111.txt"'
		return response

	except IOError:
		return HttpResponse(" 无法打开记录文件，请手工检查图像是否导入 ")
