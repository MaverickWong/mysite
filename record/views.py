# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from boards.models import *
from record.models import *
from django import forms
from linkedcare.syncDB import logIn, get_ortho_record_of_patient


# Create your views here.


def total(request, personPk):
	p = Person.objects.get(pk=personPk)
	# if p.records.count()>0:
	#     return render(request, 'record/total.html', {'records': p.records})
	# else:
	#     return render(request, 'record/total.html')

	records = p.records.order_by('-createdAt')

	return render(request, 'record/total.html', {'records': records, 'pk': personPk})


def newRecord(request, personPk):
	if request.method == 'GET':
		return render(request, 'record/new.html', {'pk': personPk})
	else:
		complain = request.POST.get('complain')
		exam = request.POST.get('exam')
		treat = request.POST.get('treat')
		note = request.POST.get('note')

		p = Person.objects.get(pk=personPk)
		# try:
		new_record = Record.objects.create(doctor=request.user,
		                                   exam=exam,
		                                   complain=complain,
		                                   treatmentPlan=treat,
		                                   note=note,
		                                   )
		new_record.person = p
		new_record.save()
		# url = reverse('person_detail', kwargs={'pk':personPk}) + '?tab=3'
		# return HttpResponse('保存成功')
		# return redirect(url)

		# todo 保存后应该只返回状态，让前端出通知，不用后面的再查询浪费
		p = Person.objects.get(pk=personPk)
		records = p.records.order_by('createdAt').reverse()
		return render(request, 'record/total.html', {'records': records, 'pk': personPk, 'succeed': 1})
	# except:
	# 	# return HttpResponse('保存失败')
	# 	p = Person.objects.get(pk=personPk)
	# 	records = p.records.order_by('createdAt').reverse()
	# 	return render(request, 'record/total.html', {'records': records, 'pk': personPk, 'succeed': 0})


def delRecord(request, personPk, recordPk):
	record = Record.objects.get(pk=recordPk)
	record.delete()

	p = Person.objects.get(pk=personPk)
	records = p.records.order_by('createdAt').reverse()

	return render(request, 'record/total.html', {'records': records, 'pk': personPk})


class EditForm(forms.Form):
	exam = forms.CharField(label='检查（512字）', required=False, max_length=512,
	                       widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
	treat = forms.CharField(label='处置（512字）', required=True, max_length=512,
	                        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))

	note = forms.CharField(label='医嘱（128字）', required=False, max_length=128,
	                       widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
# idnum = forms.CharField(label='病历号', required=True, max_length=30)
# linkedcareId = forms.IntegerField(label='易看牙后台序号', required=False)


def editRecord(request, personPk, recordPk):
	if request.method == 'POST':
		edit_form = EditForm(request.POST)

		message = '请检查填写内容'
		if edit_form.is_valid():
			note = edit_form.cleaned_data['note']
			treat = edit_form.cleaned_data['treat']
			exam = edit_form.cleaned_data['exam']

			# linkedcareId = edit_form.cleaned_data['linkedcareId']

			p = Record.objects.get(pk=recordPk)
			p.treatmentPlan = treat
			p.note = note
			p.exam = exam
			# p.doctor = request.user
			# p.linkedcareId = linkedcareId
			# task.startTime=startTime

			p.save()
			message = '保存成功'
			# todo 保存后刷新
			# return HttpResponse('ok', content_type='Application/json')
			# return redirect('/detail/' + str(personPk), {'msg': message})
			return redirect(reverse('boards:person_detail', args=(str(personPk),)), {'msg': message})

	else:  # get
		p = Record.objects.get(pk=recordPk)
		form = EditForm(
			initial={
				'treat': p.treatmentPlan,
				'note': p.note,
				'exam': p.exam,
			}
		)

		return render(request, 'record/edit.html', {'form': form, 'pk': recordPk, 'ppk': personPk})


def importRecord(request, personPk):
	s = logIn()
	p = Person.objects.get(pk=personPk)
	get_ortho_record_of_patient(s, p)
	message = '导入成功'
	return redirect(reverse('boards:person_detail', args=(str(personPk),)), {'msg': message})
