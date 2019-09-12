from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404


# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from boards.models import *
# from record.models import *
from charge_record.models import *
from django import forms


# Create your views here.

def all_orders(request, personPk):
	"""
	获取该患者 所有 收费记录
	:param request:
	:param personPk:
	:return:
	"""
	p = Person.objects.get(pk=personPk)

	records = p.charge_orders.order_by('recordCreatedTime').reverse()
	sum = p.charge_summary.first()

	# from django.contrib import messages
	# messages.add_message(request, messages.INFO, "Your Message")

	context = {'records': records, 'pk': personPk, 'summary': sum}
	return render(request, 'charge_record/total.html', context)


class AddForm(forms.Form):
	# name = forms.CharField(label='物品名称', required=True, max_length=100,
	#                        widget=forms.TextInput(attrs={'class': 'form-control'}))

	totalPrice = forms.FloatField(label='应收总数', error_messages={
		'invalid': '请输入数字',
		'required': '不能为空',
	})
	actualPrice = forms.FloatField(label='实收', required=True)
	overdue = forms.FloatField(label='欠费', required=True)
	discount = forms.FloatField(label='折扣百分比', required=False)
	discountPrice = forms.FloatField(label='折扣价格', required=False)

	comment = forms.CharField(label='备注', required=False, max_length=200)
	payType = forms.CharField(label='支付类型', required=True, max_length=10, widget=forms.TextInput(attrs={}))


def new_record(request, personPk):
	"""
	新建收费记录
	:param request:
	:param personPk:
	:return:
	"""
	if request.method == 'GET':
		form = AddForm()
		return render(request, 'charge_record/new.html', locals())

	else:  # post
		register_form = AddForm(request.POST)

		# register_form = forms.RegisterForm(request.POST)
		message = '请检查填写内容'
		if register_form.is_valid():
			totalPrice = register_form.cleaned_data['totalPrice']
			actualPrice = register_form.cleaned_data['actualPrice']
			discount = register_form.cleaned_data['discount']
			overdue = register_form.cleaned_data['overdue']
			comment = register_form.cleaned_data['comment']
			discountPrice = register_form.cleaned_data['discountPrice']
			payType = register_form.cleaned_data['payType']
			# endTime = register_form.cleaned_data['endTime']

			p = Person.objects.get(pk=personPk)
			if 1:
				newOrder = ChargeOrder.objects.create(doctor=request.user,
				                                      totalPrice=float(totalPrice),
				                                      actualPrice=float(actualPrice),
				                                      overdue=float(overdue),
				                                      comments=comment,
				                                      isImported=False, person=p,
				                                      discountPrice=discountPrice,
				                                      discount=discount,
				                                      payType=payType,
				                                      doctorName=str(request.user),
				                                      )

				# todo 保存后应该只返回状态，让前端出通知，不用后面的再查询浪费
				# p = Person.objects.get(pk=personPk)

				# 更新收费 summary
				sum = p.charge_summary.first()
				if not sum:
					sum = ChargeSummary.objects.create(totalOverdue=0, person=p,
					                                   totalPlanPrice=0, totalActualPrice=0,
					                                   totalAdvacePrice=0)

				sum.totalActualPrice = sum.totalActualPrice + float(actualPrice)
				sum.totalOverdue = sum.totalOverdue + float(overdue)
				sum.totalPlanPrice = sum.totalPlanPrice + float(totalPrice)
				sum.save()

				records = p.charge_orders.order_by('recordCreatedTime').reverse()
				context = {'records': records, 'pk': personPk, 'succeed': 1, 'summary': sum}
				# return render(request, 'charge_record/total.html', context)
				return redirect('boards:person_detail', personPk)

	# except:
	#     p = Person.objects.get(pk=personPk)
	#     records = p.charge_orders.order_by('recordCreatedTime').reverse()
	# sum = p.charge_summary.first()
	#     context = {'records': records, 'pk': personPk, 'succeed': 0, 'summary':sum}
	#     return render(request, 'charge_record/total.html', context)

	# context = {'succeed':0, 'pk':personPk}
	# return render(request, 'charge_record/result.html', context)
	# return HttpResponse('保存失败,请重新输入！')


def import_record(request, pk):
	from linkedcare.syncDB import get_charge_record_of_patient, logIn
	p = Person.objects.get(pk=pk)

	# if p.charge_summary.count() == 0:
	s = logIn()
	get_charge_record_of_patient(s, p)

	records = p.charge_orders.order_by('recordCreatedTime').reverse()
	context = {'records': records, 'pk': pk}

	from django.contrib import messages
	messages.add_message(request, messages.INFO, "完成导入")

	return redirect('boards:person_detail', pk)


def print_record(request, recordPk):
	"""
	打印患者收费单
	:param request:
	:param recordPk:
	:return:
	"""
	# record = ChargeOrder.objects.get(pk=recordpk)
	record = get_object_or_404(ChargeOrder, pk=recordPk)
	p = record.person
	context = {'record': record, 'patient': p}

	return render(request, 'charge_record/printRecord.html', context)


''' API 方法
'''

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from django.http import QueryDict
from rest_framework import permissions

from .serializer import ChargeOrderSerializer

from rest_framework.request import Request


def get_parameter_dic(request, *args, **kwargs):
	if isinstance(request, Request) == False:
		return {}

	query_params = request.query_params
	if isinstance(query_params, QueryDict):
		query_params = query_params.dict()
	result_data = request.data
	if isinstance(result_data, QueryDict):
		result_data = result_data.dict()

	if query_params != {}:
		return query_params
	else:
		return result_data


# 方法 1
class ChargeOrderView(APIView):
	def get(self, request, format=None):
		# dict = request.query_params.dict()
		params = get_parameter_dic(request).get('id')

		order = ChargeOrder.objects.first()
		try:
			if dict['id']:
				id = dict['id']
				order = ChargeOrder.objects.get(pk=id)
		except:
			pass

		serializer = ChargeOrderSerializer(order)
		return Response(serializer.data)


# 方法 2
from rest_framework.viewsets import ModelViewSet
from collections import OrderedDict, namedtuple
from rest_framework import pagination


class UserPagination(pagination.PageNumberPagination):
	'''自定义分页'''
	page_size = 10

	def get_paginated_response(self, data):
		return Response(OrderedDict([
			('totalCount', self.page.paginator.count),
			('pageIndex', self.page.number),
			('pageCount', self.page.paginator.num_pages),
			('pageSize', self.page_size),

			('next', self.get_next_link()),
			('previous', self.get_previous_link()),

			('items', data)
		]))


# 测试2 自定义分页
class testViewSet(ModelViewSet):
	serializer_class = ChargeOrderSerializer
	pagination_class = UserPagination

	def get_queryset(self):
		return ChargeOrder.objects.all()

	def list(self, request, *args, **kwargs):
		status = request.query_params.get("status")  # 自己加了个参数status，控制分页的数量
		items = self.get_queryset()
		if status == '1':
			self.paginator.page_size = items.count()

		page = self.paginate_queryset(items)
		serializer = self.get_serializer(page, many=True)
		return self.get_paginated_response(serializer.data)


class ChargeOrderViewSet(ModelViewSet):
	queryset = ChargeOrder.objects.all()
	serializer_class = ChargeOrderSerializer
	pagination_class = UserPagination
	permission_classes = [permissions.IsAuthenticated]


def login(request):
	from django.http import JsonResponse
	import json

	a = {
		'name': 'super_admin',
		'user_id': '1',
		'access': ['super_admin', 'admin'],
		'token': 'super_admin',
		'avatar': 'https://file.iviewui.com/dist/a0e88e83800f138b94d2414621bd9704.png'
	}

	return JsonResponse(json.dumps(a), safe=False)
