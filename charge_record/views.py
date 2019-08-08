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

	totalPrice = forms.FloatField(label='应收总数', required=True)
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

		    # totalPrice = request.POST.get('totalPrice')
		    #     actualPrice = request.POST.get('actualPrice')
		    #     overdue = request.POST.get('overdue')
		    #     comment = request.POST.get('comment')
		    #     discount = request.POST.get('discount')
		    #     discountPrice = request.POST.get('discountPrice')
		    #     payType = request.POST.get('payType')
		    #     # note = request.POST.get('note')

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
			    p = Person.objects.get(pk=personPk)

			    # 更新收费 summary
			    sum = p.charge_summary.first()
			    sum.totalActualPrice = sum.totalActualPrice + float(actualPrice)
			    sum.totalOverdue = sum.totalOverdue + float(overdue)
			    sum.totalPlanPrice = sum.totalPlanPrice + float(totalPrice)
			    sum.save()

			    records = p.charge_orders.order_by('recordCreatedTime').reverse()
			    context = {'records': records, 'pk': personPk, 'succeed': 1, 'summary': sum}
			    return render(request, 'charge_record/total.html', context)

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

	if p.charge_summary.count() == 0:
		s = logIn()

		get_charge_record_of_patient(s, p)

	records = p.charge_orders.order_by('recordCreatedTime').reverse()
	context = {'records': records, 'pk': pk}

	from django.contrib import messages
	messages.add_message(request, messages.INFO, "重复导入")

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
    context = {'record': record}
    return render(request, 'charge_record/printRecord.html', context)
