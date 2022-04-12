from django.shortcuts import render
import time, json
import datetime
import pytz
from django.utils import timezone
from linkedcare.syncDB import logIn, get_headers
from appointment.models import *
from django.shortcuts import render, redirect, reverse, Http404, HttpResponse


# Create your views here.


def home(request):
	# get_appointments_of_date()
	# date = get_date_from_string('2019-04-17')
	fmt = '%Y-%m-%d'

	adate = datetime.datetime.now()
	date_str = adate.strftime(fmt)
	if request.GET.get('date'):
		adate = get_date_from_string(request.GET['date'])
		date_str = adate.strftime(fmt)

	all_appitem = ApptItem.objects.filter(startDateTime__date=adate)

	# 如果数据库没有该日期的数据，则联网查询
	# if all_appitem.count() == 0:
	# 	get_appointments_of_date(adate.strftime(fmt))

	cntx = {'apptItem': all_appitem, 'date_str': date_str}

	return render(request, 'appointment/index.html', context=cntx)


def update_today_appts(request):  # 只刷新当天的预约

	# get_appointments_of_date()
	# date = get_date_from_string('2019-04-17')
	# adate = datetime.date(2019, 4, 16)
	adate = datetime.datetime.now()
	fmt = '%Y-%m-%d'

	# get_appointments_of_date(adate.strftime(fmt), isUpdate=True)
	bdate = adate + datetime.timedelta(days=30)

	all_appitem = ApptItem.objects.filter(startDateTime__date__range=(adate, bdate))
	cntx = {'apptItem': all_appitem}

	return render(request, 'appointment/index.html', context=cntx)


def newRecord(request, personPk):
	if request.method == 'GET':
		return render(request, 'appointment/new.html', {'pk': personPk})
	else:
		# complain = request.POST.get('complain')
		# exam = request.POST.get('exam')
		date = request.POST.get('date')
		note = request.POST.get('comment')

		p = Person.objects.get(pk=personPk)
		# try:
		dt = get_timezone_date_from_string(date)
		new_record = ApptItem.objects.create(startDateTime=dt,
			comment=note,
		                                   )
		new_record.patient = p
		new_record.save()
		# url = reverse('person_detail', kwargs={'pk':personPk}) + '?tab=3'
		# return HttpResponse('保存成功')
		# return redirect(url)

		# todo 保存后应该只返回状态，让前端出通知，不用后面的再查询浪费
		p = Person.objects.get(pk=personPk)
		records = p.apptItems.order_by('createDateTime').reverse()
		return render(request, 'appointment/total.html', {'records': records, 'pk': personPk, 'succeed': 1})


from django import forms
class EditForm(forms.Form):

	# treat = forms.CharField(label='时间', required=True, max_length=512,
	#                         widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 1}))
	time = forms.DateTimeField(label='时间',  required=True, widget=forms.TextInput(attrs={'id':'datetimepicker', 'class': 'form-control'}))
	note = forms.CharField(label='备注', required=True, max_length=128,
	                       widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))


def edit(request, personPk, recordPk):
	# from django.shortcuts import render, redirect, reverse

	if request.method == 'POST':
		edit_form = EditForm(request.POST)

		message = '请检查填写内容'
		if edit_form.is_valid():
			note = edit_form.cleaned_data['note']
			time = edit_form.cleaned_data['time']

			p = ApptItem.objects.get(pk=recordPk)
			p.startDateTime = time
			p.comment = note
			p.save()
			message = '保存成功'
			# todo 保存后刷新
			# return HttpResponse('ok', content_type='Application/json')
			# return redirect('/detail/' + str(personPk), {'msg': message})
			return redirect(reverse('boards:person_detail', args=(str(personPk),)), {'msg': message})
		else:
			return HttpResponse('fuck')

	else:  # get
		p = ApptItem.objects.get(pk=recordPk)
		dt = p.startDateTime
		stime = datetime.datetime(dt.year, dt.month, dt.day, dt.hour+8, dt.minute, dt.second)

		form = EditForm(
			initial={
				'time': stime,
				'note': p.comment,
			}
		)

		return render(request, 'appointment/edit.html', {'form': form, 'pk': recordPk, 'ppk': personPk})



def list_all(request, personPk):
	p = Person.objects.get(pk=personPk)
	# if p.records.count()>0:
	#     return render(request, 'record/total.html', {'records': p.records})
	# else:
	#     return render(request, 'record/total.html')

	appt = p.apptItems.order_by('-createDateTime')

	return render(request, 'appointment/total.html', {'records': appt, 'pk': personPk})


def get_date_from_string(str):  # '2017-10-19'
	'''
	:param str: '2017-10-19'
	:return: datetime.date
	'''
	date_str = str
	fmt = '%Y-%m-%d'

	dt = datetime.datetime.strptime(date_str, fmt)
	# year, month, day = dt[:3]
	a_date = datetime.date(dt.year, dt.month, dt.day)
	# print(a_date, type(a_date))
	return a_date


def get_timezone_date_from_string(str):
	utc = pytz.timezone('Asia/Shanghai')
	dt = datetime.datetime.strptime(str, '%Y-%m-%d %H:%M')
	# atime = datetime.datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, tzinfo=utc)
	atime = datetime.datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)

	tz = timezone.get_default_timezone()
	tz.localize(atime)

	return atime


def get_appointments_of_date(date_str, isUpdate=False):
	# '2017-10-19'
	fmt = '%Y-%m-%d'
	startdate = datetime.datetime.strptime(date_str, fmt)
	oneday = datetime.timedelta(days=1)
	enddate = startdate + oneday
	enddate_str = enddate.strftime(fmt)



	utc = pytz.timezone('Asia/Shanghai')

	newDateforAppoint = DateForAppoint.objects.create(date=startdate)


	newitem = ApptItem.objects.create(linkedApptID=item['appointId'], comment=item['notes'],
				                                  patient=p, patientName=item['patientName'],
				                                  # assistantId=item['assistantId'], assistantName=item['assistantName'],
				                                  dateForAppt=newDateforAppoint,)



	newitem.startDateTime = get_timezone_date_from_string(item['appointDateTime'])
	newitem.save()



	return data
