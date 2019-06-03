from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from boards.models import *


# Create your views here.


# 搜索首页
def search_index(request):
	tgroups = []
	for i in range(10):
		tgroup = Tag.objects.filter(type=i)
		tgroups.append(tgroup)
	# tgroups.append(Tag.objects.filter(type=101)) # 添加101其他
	tags = Tag.objects.filter(type=101)
	contx = {'tgroups': tgroups, 'tag_islink': True, 'tags': tags}
	return render(request, './search/index_search_patients.html', contx)


# 单个 tag 搜索
def tag_search(request, tag):
	docname = request.user.username
	ut = str(tag)
	# t = Tag.objects.get(name=ut)
	t = get_object_or_404(Tag, name=ut)
	if docname == 'zdl':
		ps = t.persons.all()
	else:
		ps = t.persons.filter(doctor=docname)

	ps = ps.order_by('pk')
	total = ps.count()
	page = request.GET.get('page', 1)

	persons = get_paginator(ps, page)

	return render(request, './search/search_result.html', {'persons': persons, 'total': total})


# 多tag 相交搜索
def super_search(request):
	docname = request.user.username
	s = request.GET['s']
	if s == '':
		return redirect('home')
	else:
		# persons = search_person_with_str(s, docname)
		list = s.split(' ')  # 按空格分割关键词
		persons = Person.objects.all()

		for i in list:
			tags = Tag.objects.filter(name=i)
			if tags.count() == 1:
				qts = tags[0].persons.all()
				persons = persons.intersection(qts)

	total = persons.count()

	return render(request, './search/search_result.html', {'persons': persons, 'total': total})


# 搜索框推荐
def search_suggest(request):
	docname = request.user.username
	docname = 'zdl'  # 为了测试，anyone可以搜索所有zdl
	s = request.GET['s']
	if s == '':
		persons = Person.objects.none()
	else:
		persons = search_person_with_str(s, docname)

	data = []
	for p in persons:
		data.append({'name': p.name, 'idnum': p.idnum, 'pnum': p.posts.count(), 'pk': p.pk})

	res = {"code": 200,
	       "redirect": "",
	       "value": data
	       }
	return JsonResponse(res)


# return HttpResponse(json.dumps(res), content_type="application/json")


# 组装paginator, 返回persons
def get_paginator(queryset, page):
	paginator = Paginator(queryset, 5)
	try:
		p = paginator.page(page)
	except PageNotAnInteger:
		# fallback to the first page
		p = paginator.page(1)
	except EmptyPage:
		# probably the user tried to add a page number
		# in the url, so we fallback to the last page
		p = paginator.page(paginator.num_pages)

	return p


# 搜索框输入字符串，先判断是否tag，及人名
def search_person_with_str(s, docname):  # 搜索字符串和医生名字
	if s.isnumeric():  # 搜索内容是数字
		if docname == 'zdl':
			persons = Person.objects.filter(idnum__contains=s)
		else:
			persons = Person.objects.filter(idnum__contains=s, doctor=docname)
	elif s == '':
		persons = Person.objects.none()

	else:
		list = s.split(' ')  # 按空格分割关键词
		if docname == 'zdl':
			pt = persons = Person.objects.all()
			pts = Person.objects.none()
			for i in list:
				qn = Person.objects.filter(name__contains=i)
				if qn.count() > 0:
					persons = persons.intersection(qn)
					continue
				# persons = Person.objects.filter(name__contains=s)
				tags = Tag.objects.filter(name__contains=i)
				for t in tags:
					qts = t.persons.all()
					pts = pts.union(qts)
				if pts.count() > 0:
					pt = pt.intersection(pts)

			if pt.count() > 0 and (not pt.count() == Person.objects.all().count()):
				if persons.count() > 0:
					persons = persons.intersection(pt)
				else:
					persons = persons.union(pt)
			elif persons.count() == Person.objects.all().count():
				persons = Person.objects.none()
		#     persons = persons

		else:
			persons = Person.objects.all()
			for i in list:
				q = Person.objects.filter(name__contains=i, doctor=docname)
				persons = persons.intersection(q)
	# persons = Person.objects.filter(name__contains=s, doctor=docname)
	return persons


def get_tag_groups():
	tgroups = []
	for i in range(10):
		tgroup = Tag.objects.filter(type=i)
		tgroups.append(tgroup)
	return tgroups


''' 下面两个可能用不到'''


# 搜索框搜索
def navbar_search(request):
	docname = request.user.username
	s = request.GET['s']
	if s == '':
		return redirect('home')
	else:
		persons = search_person_with_str(s, docname)

	if persons.count() == 1:
		return redirect('person_detail', persons.first().pk)
	else:
		ps = persons.order_by('pk')
		total = ps.count()
		page = request.GET.get('page', 1)

		persons = get_paginator(ps, page)
		return render(request, 'search\search_result.html', {'persons': persons, 's': s, 'total': total})


def s_search(request):
	tgroups = get_tag_groups()
	tags = Tag.objects.all()

	return render(request, 'search/s_search.html', {'tags': tags, 'tgroups': tgroups})
