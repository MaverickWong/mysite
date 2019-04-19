from django.shortcuts import render
import time, json
import datetime
import pytz

from linkedcare.syncDB import logIn, get_headers
from appointment.models import *


# Create your views here.


def home(request):
	# get_appointments_of_date()
	# date = get_date_from_string('2019-04-17')
	fmt = '%Y-%m-%d'

	adate = datetime.datetime.now()
	if request.GET.get('date'):
		adate = get_date_from_string(request.GET['date'])

	all_appitem = ApptItem.objects.filter(startDateTime__date=adate)

	# 如果数据库没有该日期的数据，则联网查询
	if all_appitem.count() == 0:
		get_appointments_of_date(adate.strftime(fmt))

	cntx = {'apptItem': all_appitem}

	return render(request, 'appointment/index.html', context=cntx)


def update_today_appts(request):  # 只刷新当天的预约

	# get_appointments_of_date()
	# date = get_date_from_string('2019-04-17')
	# adate = datetime.date(2019, 4, 16)
	adate = datetime.datetime.now()
	fmt = '%Y-%m-%d'

	get_appointments_of_date(adate.strftime(fmt), isUpdate=True)

	all_appitem = ApptItem.objects.filter(startDateTime__date=adate)
	cntx = {'apptItem': all_appitem}

	return render(request, 'appointment/index.html', context=cntx)


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
	dt = datetime.datetime.strptime(str, '%Y-%m-%dT%H:%M:%S')
	atime = datetime.datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, tzinfo=utc)
	return atime


def get_appointments_of_date(date_str, isUpdate=False):
	# '2017-10-19'
	fmt = '%Y-%m-%d'
	startdate = datetime.datetime.strptime(date_str, fmt)
	oneday = datetime.timedelta(days=1)
	enddate = startdate + oneday
	enddate_str = enddate.strftime(fmt)

	url = 'https://api.linkedcare.cn:9001/api/v1/dashboard/appt-work?doctorId=913&endTime=%s&startTime=%s' % (
		enddate_str, date_str)

	s = logIn()
	headers = get_headers(s)

	r = s.get(url, headers=headers)

	# totalcount = eval(r.content)["totalCount"]
	data = json.loads(r.content.decode('utf-8'))
	print('患者')
	# print('按照 %s 共搜到 %d 个' % (searchString, data['totalCount']))
	if len(data) > 0:
		utc = pytz.timezone('Asia/Shanghai')

		newDateforAppoint = DateForAppoint.objects.create(date=startdate)
		for item in data:
			items = ApptItem.objects.filter(linkedApptID=item['appointId'])
			num = items.count()
			if num == 0:
				ps = Person.objects.filter(linkedcareId=item['patientId'])
				if ps.count() == 0:
					p = Person.objects.create(name=item['patientName'], linkedcareId=item['patientId'],
					                          idnum=item['privateId'], nameCode=item['patientNameCode'])
				else:
					p = ps[0]

				newitem = ApptItem.objects.create(linkedApptID=item['appointId'], comment=item['notes'],
				                                  patient=p, patientName=item['patientName'],
				                                  dateForAppt=newDateforAppoint,
				                                  isFirstVisit=item['isFirstVisit'],
				                                  isCharged=item['hasChargeOrder'],
				                                  isCheckedIn=item['isCheckedIn'], checkInType=item['checkInType'],
				                                  isFinished=item['isCompleted'], isLeft=item['isLeft'],
				                                  isFail=item['isFailed'], isPending=item['isPending'],
				                                  isConfirmed=item['isConfirmed'], isSeated=item['isSeated'],
				                                  isCancel=item['isCancelled']

				                                  )

				# 修改时间 #'2018-07-29T09:48:37'
				if item['appointDateTime']:
					# dt = datetime.datetime.strptime(item['appointDateTime'], '%Y-%m-%dT%H:%M:%S')
					# ctime = datetime.datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, tzinfo=utc)
					newitem.startDateTime = get_timezone_date_from_string(item['appointDateTime'])
					newitem.save()
				if item['checkInTime']:
					newitem.checkInTime = get_timezone_date_from_string(item['checkInTime'])
					newitem.save()
				if item['seatTime']:
					newitem.seatTime = get_timezone_date_from_string(item['seatTime'])
					newitem.save()

				print('保存预约记录%s' % (item['appointDateTime']))

			elif num == 1 and isUpdate:
				appt = items.first()
				items.update(isFirstVisit=item['isFirstVisit'], isCheckedIn=item['isCheckedIn'],
				             isFinished=item['isCompleted'], isLeft=item['isLeft'],
				             isPending=item['isPending'],
				             isSeated=item['isSeated'],
				             )

	return data
