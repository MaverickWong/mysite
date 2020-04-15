#!/usr/bin/python
# -*- coding: UTF-8 -*-
import mysite
# 这个一定要，不然会报错，但是错误很明显，容易定位。
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
import django

django.setup()
# django版本大于1.7时需要这两句

import pytz
from datetime import datetime
import requests
import json
import sys
from boards.models import *
from record.models import Record
from mysite.settings import BASE_DIR

agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3418.2 Safari/537.36"

account = "zhangdongliang"
passwd = "hehe58761678"


# officeId 劲松122 华贸124 禾禾 326

def test():
	print('tesst')


# 开始
def logIn(officeId=122, userId=745):
	'''
    先判断是否有cookie保存，如果有，则用cookie登录。
    如果没有cookie，则调用用户名登录，并保存cookie
    :param officeId: 劲松122 华贸124 禾禾 326
    :param userId: 没用 5103
    :return:
    '''

	# targetURL = 'http://simaier.linkedcare.cn/'
	targetURL = 'http://bjhhkq.linkedcare.cn/'

	# 设置头UA
	headers = {
		"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"}

	# 开启一个session会话
	session = requests.session()

	# 设置请求头信息
	session.headers = headers

	# 申明一个用于存储手动cookies的字典
	manual_cookies = {}

	if os.path.exists("manual_cookies.txt"):

		with open("manual_cookies.txt", 'r', encoding='utf-8') as frcookie:
			cookies_txt = frcookie.read().strip(';')  # 读取文本内容
			# 手动分割添加cookie
			for item in cookies_txt.split(';'):
				name, value = item.strip().split('=', 1)  # 用=号分割，分割1次
				manual_cookies[name] = value  # 为字典cookies添加内容

		# 将字典转为CookieJar：
		cookiesJar = requests.utils.cookiejar_from_dict(manual_cookies, cookiejar=None, overwrite=True)

		# 将cookiesJar赋值给会话
		session.cookies = cookiesJar

		# 向目标网站发起请求
		res = session.get(targetURL, allow_redirects=False)

		if res.status_code == 200:
			# if res.url != targetURL:
			#     session = login_save_cookie(officeId=officeId, userId=userId)
			#     print('登录遭遇rediret')
			#     return session
			# else:
			print('cookie登录成功')
			return session

		# elif res.status_code == 302:  # https://2.python-requests.org//zh_CN/latest/user/quickstart.html
		else:
			print('cookie登录失败，转用户名登录')
			session = login_save_cookie(officeId=officeId, userId=userId)
			return session

	else:  # cookie记录文件不存在，则用用户名登录后保存cookie到新建txt
		session = login_save_cookie(officeId, userId)
		return session


def login_save_cookie(officeId=122, userId=745):
	officeId = 326
	# account = "zhangdongliang"
	# passwd = "simaierzdl123"
	# 登陆参数
	logURL = "https://simaier.linkedcare.cn/LogOn"
	logURL = 'https://bjhhkq.linkedcare.cn/LogOn'

	agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3418.2 Safari/537.36"

	# print(officeId)
	payload = {"officeId": officeId, "account": account, "password": passwd, "validationCode": "",
	           "platform": 1, "kickOther": "false", "clientId": "fa28b13b-3161-4605-ae95-c6d4f35c5064",
	           "isCheckMobileValidation": "", "mobileValidationCode": ""}
	# 登录并获得session
	s = requests.session()
	res = s.post(logURL, params=payload, allow_redirects=False)

	if res.status_code == 200:
		print('用户名登录成功')
		# 申明一个用于存储手动cookies的字典
		manual_cookies = {}
		# 将CookieJar转为字典：
		res_cookies_dic = requests.utils.dict_from_cookiejar(res.cookies)

		# 将新的cookies信息更新到手动cookies字典
		for k in res_cookies_dic.keys():
			manual_cookies[k] = res_cookies_dic[k]

		print(manual_cookies)

		# 重新将新的cookies信息写回文本
		res_manual_cookies_txt = ""

		# 将更新后的cookies写入到文本
		for k in manual_cookies.keys():
			res_manual_cookies_txt += k + "=" + manual_cookies[k] + ";"

		# 将新的cookies写入到文本中更新原来的cookies
		with open('manual_cookies.txt', "w", encoding="utf-8") as fwcookie:
			fwcookie.write(res_manual_cookies_txt)


	else:
		print('用户名登录失败')

	return s


# def logIn(officeId=122, userId = 745):
#     # officeId 劲松122 华贸124
#     # officeId = 122
#     # test()
#     userId = 745
#     account = "zhangdongliang"
#     passwd = "simaierzdl123"
#     # 登陆参数
#     logURL = "https://simaier.linkedcare.cn/LogOn"
#     agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3418.2 Safari/537.36"
#
#     # print(officeId)
#     payload = {"officeId": officeId, "account": account, "password": passwd, "validationCode": "",
#                "platform": 1, "kickOther": "false", "clientId": "7c378f28-6bc8-4c1a-a40e-3ba38a0b48fd",
#                "isCheckMobileValidation": "", "mobileValidationCode": ""}
#     # 登录并获得session
#     s = requests.session()
#     r = s.post(logURL, params=payload)
#
#     if r.status_code == 200:
#         print('登录成功')
#         # with open('log/token.txt', 'w') as f:
#         #     token = getTokenFromSession(s)
#         #     f.write(token)
#
#     else:
#         print('登录失败')
#
#     return s


# 从cookie中获取token
def getTokenFromSession(s):
	cookie = s.cookies.get_dict()
	temp = cookie['AresToken']
	tempdict = eval(temp)  # 将字符串转为字典
	token = tempdict["access_token"]
	return token


# 组装header
def get_headers(session):
	agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3418.2 Safari/537.36"

	# 从cookie中获取token
	token = getTokenFromSession(session)
	# 组装header
	headers = {'authority': 'api.linkedcare.cn:9001',
	           "authorization": "bearer " + token, "access_token": token,
	           # "clientId":"d5724218-5265-4b42-a1b8-fb1191c399bc",
	           "origin": "https://simaier.linkedcare.cn",
	           'Connection': 'keep-alive', 'user-agent': agent,
	           'referer': 'https://simaier.linkedcare.cn/',
	           'content-type': 'application/json;charset=UTF-8'
	           }
	return headers


def queryPatients(session, pageindex=1, pageSize=100, officeId=122, userId=2042):
	'''
    从易看牙同步患者基本信息，并保存到文件
    :param session:
    :param pageindex: 默认1
    :param pageSize: 默认1000
    :param officeId: 劲松122 华贸124 禾禾 326 默认劲松
    :param userId: 默认2042 呵呵5103
    :return: json列表
    '''
	# 默认劲松
	agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3418.2 Safari/537.36"
	s = session
	# s = logIn()
	# print("login: " )

	# 从cookie中获取token
	token = getTokenFromSession(s)
	# 组装header
	headers = {'authority': 'api.linkedcare.cn:9001',
	           "authorization": "bearer " + token, "access_token": token,
	           # "clientId":"7c378f28-6bc8-4c1a-a40e-3ba38a0b48fd",
	           "origin": "https://simaier.linkedcare.cn",
	           'Connection': 'keep-alive', 'user-agent': agent,
	           'referer': 'https://simaier.linkedcare.cn/',
	           'content-type': 'application/json;charset=UTF-8'
	           }
	searchURL = 'https://api.linkedcare.cn:9001/api/v1/patient/search-config'
	# searchURL = 'https://api.linkedcare.cn:9001/api/v1/search-config/get-all'

	# 搜索本人患者
	# searchResultFields = [
	#     {"searchConfigId": 0, "code": "Name", "showOrder": 0, "officeId": 0, "id": 0},
	#     {"searchConfigId": 0, "code": "PrivateId", "showOrder": 1, "officeId": 0, "id": 0},
	#     {"searchConfigId": 0, "code": "Sex", "showOrder": 2, "officeId": 0, "id": 0},
	#     {"searchConfigId": 0, "code": "Birth", "showOrder": 3, "officeId": 0, "id": 0},
	#     {"searchConfigId": 0, "code": "Mobile", "showOrder": 4, "officeId": 0, "id": 0}]
	# condFields = []
	# # condFields= [{"searchConfigId": "", "code": "FirstVisit", "comparator": ">", "value": "2018-10-20"}]
	# searchConfig = {"searchType": "患者查询", "name": "我的患者", "isPreferred": 'false', "isDefault": 'true',
	#                 "userId": userId, "isAscending": 'false', "isShowWeiXin": 'false', "orderByField": "p.Id",
	#                 "searchCondFields": condFields, "searchResultFields": searchResultFields,
	#                 "officeId": 0, "id": 0}
	#
	# searchPayload = {"searchConfig": searchConfig, "pageSize": 200, "pageIndex": pageindex, "searchText": ""}

	# 搜索全部患者
	searchResultFields = [
		{"searchConfigId": 0, "code": "Name", "showOrder": 0, "officeId": 0, "id": 0},
		{"searchConfigId": 0, "code": "PrivateId", "showOrder": 1, "officeId": 0, "id": 0},
		{"searchConfigId": 0, "code": "Sex", "showOrder": 2, "officeId": 0, "id": 0},
		{"searchConfigId": 0, "code": "Birth", "showOrder": 3, "officeId": 0, "id": 0},
		{"searchConfigId": 0, "code": "Mobile", "showOrder": 4, "officeId": 0, "id": 0},
		{"searchConfigId": 0, "code": "DoctorName", "showOrder": 5, "officeId": 0, "id": 0}]

	condFields = []
	searchConfig = {"searchType": "患者查询", "name": "全部患者", "isPreferred": 'true', "isDefault": 'true',
	                "userId": userId, "isAscending": 'false', "isShowWeiXin": 'false', "orderByField": "p.Id",
	                "searchCondFields": condFields, "searchResultFields": searchResultFields,
	                "officeId": 0, "id": 0}

	searchPayload = {"searchConfig": searchConfig, "pageSize": pageSize, "pageIndex": pageindex, "searchText": ""}

	# 得到结果处理并返回
	# searchResult = s.put(searchURL, params=searchPayload, headers=headers)
	searchResult = s.put(searchURL, headers=headers, data=json.dumps(searchPayload))

	# totalcount = eval(r.content)["totalCount"]
	data = json.loads(searchResult.content.decode('utf-8'))
	# print(data)
	print('获取patients 成功')

	dt = datetime.now()
	time2 = dt.strftime("%m%d-%H%M%S")
	# 保存到文件
	try:
		fname = BASE_DIR + '/linkedcare/get_patients' + '_' + time2 + '.txt'
		with open(fname, 'w') as f:
			json.dump(data, f)
	except:
		pass

	return data


# 主要函数，
def get_patients_fill_DB(total=10):
	'''
    批量获取患者基本信息，默认10个
    并新建患者，存入数据库
    :return:
    '''
	dt = datetime.now()
	time2 = dt.strftime("%m%d-%H%M%S")
	# officeId 劲松122 华贸124
	repeated = []
	succeded = []
	office = [124, 122]
	id = 122
	total_page_num = int(total / 10)
	# i = 1;
	s = logIn(officeId=id)

	for i in range(total_page_num):
		# for id in office:
		data = queryPatients(s, pageindex=i + 1)  # 从易看牙获得数据bing保存到文件

		totalPages = data['pageCount']

		# 导入到数据库
		for item in data['items']:
			if item['doctorName'] == '913':  # 筛选张老师的患者
				n = Person.objects.filter(idnum__contains=item['privateId']).filter(name__contains=item['name']).count()
				if n > 0:  # 先根据id判断是否有重复患者，如果有则登记。没有则新建患者
					repeated.append(item['privateId'] + item['name'])

				elif n == 0:
					if item['birth']:
						birth = item['birth'][0:10]
					else:
						birth = None
					p = Person.objects.create(idnum=item['privateId'], name=item['name'], nameCode=item['nameCode'],
					                          mobile=item['mobile'],
					                          otherPrivateId=item['otherPrivateId'], birth=birth, sex=item['sex'],
					                          doctor='zdl',
					                          doctorId=item['doctorId'], officeId=item['officeId'],
					                          clinic=item['officeId'],
					                          email=item['email'],
					                          occupation=item['occupation'], qq=item['qq'], weixin=item['weixin'],
					                          identityCard=item['identityCard'], homeAddress=item['homeAddress'],
					                          patientType=item['patientType'], lastVisit=item['lastVisit'],
					                          lastDoctorId=item['lastDoctorId'], linkedcareId=item['id']
					                          )

					succeded.append(item['privateId'] + '.' + item['name'] + '.' + str(id))

	# 记录导入log
	fname2 = BASE_DIR + '/log/log-syncDB' + time2 + '.txt'
	with open(fname2, 'w') as f:
		# f.write("{}  {}  {}  {}\n".format(title, price, scrible, pic))
		f.write('succeded *******************************\n')
		for i in succeded:
			f.write(i)
			f.write('\n')

		f.write('\n\n\n')
		f.write('repeated *******************************\n')
		for i in repeated:
			f.write(i)
			f.write('\n')


# repeated = []
# succeded = []
#
# office =['124', '122']
# for id in office:
#     s = logIn()
#     data = queryPatients(s, id) # 从易看牙获得数据
#
#     for item in data['items']:
#         n = Person.objects.filter(idnum__contains=item['privateId']).count()
#
#         if n > 0: #  先根据id判断是否有重复患者，如果有则登记。没有则新建患者
#             repeated.append(item['privateId'] + item['name'])
#         elif n == 0:
#             if item['birth']:
#                 birth = item['birth'][0:10]
#             else:
#                 birth = None
#             p = Person.objects.create(idnum=item['privateId'], name=item['name'], nameCode=item['nameCode'], linkedcareId=item['id'], mobile=item['mobile'],
#                                       otherPrivateId=item['otherPrivateId'], birth=birth, sex=item['sex'], doctor='zdl',
#                                       doctorId=item['doctorId'], officeId=item['officeId'], clinic=item['officeId'], email=item['email'],
#                                       occupation=item['occupation'], qq=item['qq'], weixin=item['weixin'], identityCard=item['identityCard'],homeAddress=item['homeAddress'],
#                                       patientType=item['patientType'], lastVisit=item['lastVisit'], lastDoctorId=item['lastDoctorId']
#                                       )
#             succeded.append(item['privateId'] + item['name'])
#
# with open('result.txt', 'w') as f:
#     # f.write("{}  {}  {}  {}\n".format(title, price, scrible, pic))
#     f.write('repeated \n')
#     for i in repeated:
#         f.write(i)
#         f.write('\n')
#         # f.write('\n')
#     f.write('\n\n================================================== \n')
#
#     f.write('succeded: \n')
#     f.write(succeded.count())
#     for i in succeded:
#         f.write(i)
#         f.write('\n')


def search_from_linked_with_string(searchString, session):
	'''
    从易看牙搜索 字符串，将结果json返回
    :param searchString搜索字符串
    :return: 返回 全部搜索数组json
    '''

	# session = logIn()
	headers = get_headers(session)
	searchURL = 'https://api.linkedcare.cn:9001/api/v1/patients'
	# searchURL = 'https://api.linkedcare.cn:9001/api/v1/search-config/get-all'
	payload = {"isBusyRequest": 'false', "isExactMatchSelected": "false", "pageIndex": 1, "pageSize": 10,
	           "searchString": searchString}
	searchResult = session.get(searchURL, params=payload, headers=headers)

	# totalcount = eval(r.content)["totalCount"]
	data = json.loads(searchResult.content.decode('utf-8'))
	print('按照 %s 共搜到 %d 个' % (searchString, data['totalCount']))
	return data


def search_person_from_linked(person, session):
	'''
    根据系统中已经存在的person名字及病历号，去linkedcare搜索
    :param person: Person类
    :param session:
    :return:
    '''
	# todo 添加 根据病历号搜索人
	# 根据名字搜索
	data = search_from_linked_with_string(person.name, session)
	# print(data['totalCount'])

	if data['totalCount'] == 0:
		return None
	# elif data['totalCount'] ==1:
	#     return data['items'][0]
	else:
		for item in data['items']:
			if person.idnum:  # 病例库患者有病历号
				if item['privateId'] == person.idnum:
					print('从结果中匹配：pk--%d, %s 对应id--%d' % (person.pk, person.name, item['id']))
					return item
			else:  # 病例库患者无病历号
				print('患者 %s 搜索结果较多，但是因为病例库无病历号，无法匹配')
				return None


def add_id_for_person(person):
	# 为数据库中有些人添加linkedcareId
	session = logIn()

	data = search_from_linked_with_string(person.name, session)
	# 处理结果
	print(data['totalCount'])
	for item in data['items']:
		if item['name'] == person.name and item['privateId'] == person.id:
			person.linkedcareId = item['id']
			person.save()
			print('成功写入：pk--%d, %s id--%d' % (person.pk, person.name, person.linkedcareId))
			break


# def addID():
#     repeated = []
#     succeded = []
#     offices =['124', '122']
#     n = 0
#     for officeid in offices:
#         data = queryPatients(officeid) # 从易看牙获得数据
#
#         for item in data['items']:
#             ps = Person.objects.filter(idnum__contains=item['privateId']).filter(name__contains=item['name'])
#             if ps.count() ==1:  # 先根据id判断是否有重复患者，如果有则登记。没有则新建患者
#                 p = ps[0]
#                 p.linkedcareId = item['id']
#                 p.save()
#                 n=n+1
#                 succeded.append(item['privateId'] + '.' +item['name']+'.'+ id)
#
#     with open('id.txt', 'w') as f:
#         # f.write("{}  {}  {}  {}\n".format(title, price, scrible, pic))
#
#         f.write('totaol' + n)
#         f.write('succeded \n')
#         for i in succeded:
#             f.write(i)
#             f.write('\n')


def read_jsontxt_add_link_id():
	'''
    读取txt中的json数据，并且提取id保存到患者的linkedcareId
    :return:
    '''
	with open('../linkedcare/get_patients_0225-212429.txt', 'r') as f:
		data = json.load(f)

	print(data['pageCount'])
	i = 0

	for item in data['items']:
		persons = Person.objects.filter(idnum__contains=item['privateId'])
		if persons.count() == 1:
			person = persons[0]
			if not person.linkedcareId:
				person.linkedcareId = item['id']
				person.save()
				print('成功写入：pk--%d, %s id--%d' % (person.pk, person.name, person.linkedcareId))
				i += 1

	print('共写入：%d' % i)
	return None


def update_baseinfo_for_person_with_item(person, item):
	'''
    使用搜索到的data，更新person的数据
    :param person:
    :param item:
    :return:
    '''

	try:
		if item['birth']:
			birth = item['birth'][0:10]
			person.birth = birth
			person.save()
		else:
			birth = None

		person.linkedcareId = item['id']
		person.mobile = item['mobile']
		person.nameCode = item['nameCode']
		person.save()
		person.sex = item['sex']
		person.save()

		# person.update(otherPrivateId=item['otherPrivateId'],
		#     doctorId=item['doctorId'], officeId=item['officeId'],
		#     clinic=item['officeId'],
		#     email=item['email'],
		#     occupation=item['occupation'], qq=item['qq'],
		#     weixin=item['weixin'],
		#     identityCard=item['identityCard'],
		#     homeAddress=item['homeAddress'],
		#     patientType=item['patientType'],
		#     lastVisit=item['lastVisit'],
		#     lastDoctorId=item['lastDoctorId'],
		#     )
		print('成功写入：pk--%d, %s id--%d' % (person.pk, person.name, person.linkedcareId))
		return True

	except:
		print('baseinfo 写入失败 %s' % person.name)
		return False


def get_baseinfo_of_patient(session, person):
	'''
    爬取患者基本信息，并存入数据库
    适用于无linkedcareId的患者
    :param s: session
    :param linkedcareId:
    :return: json模型
    '''
	p = person
	if not p.linkedcareId:  # 没有id
		# 先搜索，爬取
		item = search_person_from_linked(p, session)
		# data = search_from_linked(p.name, s)
		if item:  # 判断是否有内容
			if item['name'] == p.name and item['privateId'] == p.idnum:
				# print('成功写入：pk--%d, %s id--%d' % (p.pk, p.name, p.linkedcareId))
				return update_baseinfo_for_person_with_item(p, item)

			else:
				# print('未写入')
				return False
		else:
			# print('未写入\n')
			return False

	else:  # 有id
		url = 'https://api.linkedcare.cn:9001/api/v1/patient/full/' + str(p.linkedcareId)
		headers = get_headers(session)
		searchResult = session.get(url, headers=headers)
		# totalcount = eval(r.content)["totalCount"]
		item = json.loads(searchResult.content.decode('utf-8'))
		# print(r2)
		return update_baseinfo_for_person_with_item(p, item)


def update_ortho_record_of_patient(person, items):
	#  可以根据medicalRecordId，判断是否已经存入

	utc = pytz.utc
	for item in items:

		if Record.objects.filter(medicalRecordId=item['medicalRecordId']).count() > 0:
			# 先判断重复
			print('重复病历，未导入--日期%s' % (item['recordCreatedTime']))
			continue
		else:
			try:
				record = Record.objects.create()
				record.person = person
				record.treatmentPlan = item['content']
				record.medicalRecordId = item['medicalRecordId']
				record.teethcode = item['toothCode']

				# record.createdAt = item['recordCreatedTime']
				record.createdAtLinkedcare = item['recordCreatedTime']
				record.save()
				print('正畸病例写入成功 患者：%s  病例id %d' % (person.name, item['medicalRecordId']))
				# return  True

				# 修改创建时间 #'2018-07-29T09:48:37'
				dt = datetime.strptime(item['recordCreatedTime'], '%Y-%m-%dT%H:%M:%S')
				ctime = datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, tzinfo=utc)
				record.createdAt = ctime
				record.save()

			except:
				print('正畸病例写入失败 患者：%s  病例id %d' % (person.name, item['medicalRecordId']))
				return False


def get_ortho_record_of_patient(session, person):
	'''
    爬取患者的正畸病例
        1, 判断是否有linked id,根据id下载病例，如果没有则搜索该患者
        2， 可以根据medicalRecordId 判断是否已经存入
    :param session:
    :param person:
    :return:
    '''
	p = person
	if not p.linkedcareId:  # 没有id
		# 先搜索，爬取
		item = search_person_from_linked(p, session)
		# data = search_from_linked(p.name, s)
		if item:  # 判断是否有内容
			if item['name'] == p.name and item['privateId'] == p.idnum:
				# print('成功写入：pk--%d, %s id--%d' % (p.pk, p.name, p.linkedcareId))
				update_baseinfo_for_person_with_item(p, item)
				get_ortho_record_of_patient(session, person)
				return True

			else:
				print('未搜到患者%s，未写入' % (p.name))
				return False
		else:
			print('未搜到患者%s，未写入' % (p.name))
			return False

	else:  # 有id
		url = 'https://api.linkedcare.cn:9001/api/v1/medical-record-summary?id=' + str(p.linkedcareId) + '&type=1'
		headers = get_headers(session)
		searchResult = session.get(url, headers=headers)
		# totalcount = eval(r.content)["totalCount"]
		items = json.loads(searchResult.content.decode('utf-8'))
		# print(r2)

		if len(items) > 0:
			print('下载到record共 %d 个' % (len(items)))
			return update_ortho_record_of_patient(p, items)

		else:
			return False


def get_charge_record_of_patient(session, person):
	'''获取收费记录'''
	p = person
	if not p.linkedcareId:  # 没有id
		# 先搜索，爬取
		item = search_person_from_linked(p, session)
		# data = search_from_linked(p.name, s)
		if item:  # 判断是否有内容
			if item['name'] == p.name and item['privateId'] == p.idnum:
				# print('成功写入：pk--%d, %s id--%d' % (p.pk, p.name, p.linkedcareId))
				update_baseinfo_for_person_with_item(p, item)
				get_charge_record_of_patient(session, person)
				return '导入成功'

			else:
				print('未搜到患者%s pk %d，未写入' % (p.name, p.pk))
				return '未搜到患者%s pk %d，未写入' % (p.name, p.pk)
		else:
			print('未搜到患者%s，未写入' % (p.name))
			return '未搜到患者%s pk %d，未写入' % (p.name, p.pk)

	else:  # 有id

		# 获取 sum 收费汇总
		url_sum = 'https://api.linkedcare.cn:9001/api/v1/charge-order/patient-price-info/' + str(p.linkedcareId)
		headers = get_headers(session)
		# if p.charge_summary.count() == 0:  # 先检查是否存在，没有则创建
		r = session.get(url_sum, headers=headers)
		# totalcount = eval(r.content)["totalCount"]
		if r.status_code == 200:
			res = json.loads(r.content.decode('utf-8'))
			# print(r2)
			print('%s  下载到charge_sum' % (p.name))
			update_charge_sum_of_patient(p, res)
		else:
			print('%s  下载charge_sum失败！' % (p.name))

		# 获取 收费条目
		url = 'https://api.linkedcare.cn:9001/api/v1/charge-order/paging?' \
		      + 'hasCancel=true&hasOverdue=true&hasRefund=true&hasSquare=true&pageIndex=1&pageSize=10&patientId=' \
		      + str(p.linkedcareId)
		r = session.get(url, headers=headers)
		# totalcount = eval(r.content)["totalCount"]

		if r.status_code == 200:
			res = json.loads(r.content.decode('utf-8'))
			# print(r2)
			totalCount = res['totalCount']
			if totalCount > 0:
				print('%s  下载到charge_record共 %d 个' % (p.name, totalCount))
				return update_charge_record_of_patient(p, res['items'], session)

			else:
				return False


def update_charge_sum_of_patient(person, items):
	from charge_record.models import ChargeSummary
	# try:
	sum = ChargeSummary.objects.create(person=person,
	                                   totalActualPrice=items['totalActualPrice'],
	                                   totalPlanPrice=items['totalPlanPrice'],
	                                   totalOverdue=items['totalOverdue'],
	                                   totalAdvacePrice=items['totalAdvacePrice'],
	                                   importText=str(items))
	print(' %s charge_summary 写入成功' % (person.name))


# except:
# 	print('导入时， %s charge_summary 写入失败' % (person.name))


def update_charge_record_of_patient(person, items, session):
	#  可以根据medicalRecordId，判断是否已经存入
	from charge_record.models import ChargeOrder, ChargeDetails

	utc = pytz.utc
	for item in items:
		if ChargeOrder.objects.filter(id2=item['id']).count() > 0:
			# 先判断重复
			print(' %s 重复收费id，未导入--id %s' % (person.name, item['id']))
			continue
		else:
			if 1:
				record = ChargeOrder.objects.create(isImported=True, person=person, import_text=str(item),
				                                    id2=item['id'],
				                                    totalPrice=item['totalPrice'],
				                                    # planPrice=item['planPrice'],
				                                    actualPrice=item['actualPrice'],
				                                    overdue=item['overdue'],
				                                    discountPrice=item['discountPrice'],
				                                    discount=item['discount'],
				                                    actualPrice1=item['actualPrice1'],
				                                    payType=item['payType'],
				                                    recordCreatedTime_text=item['recordCreatedTime'],
				                                    doctorId=item['doctorId'],
				                                    doctorName=item['doctorName'],
				                                    comments=item['comments'],
				                                    patientId=item['patientId'],
				                                    appointmentId=item['appointmentId'],
				                                    sourceChargeOrderId=item['sourceChargeOrderId'],
				                                    status=item['status'],
				                                    isAliPay=item['isAliPay'],
				                                    isWeixinPay=item['isWeixinPay'],
				                                    )

				print(' 收费写入成功 患者：%s  收费id %d' % (person.name, item['id']))
				# return  True

				# 修改创建时间 #'2018-07-29T09:48:37'  recordCreatedTime
				dt = datetime.strptime(item['recordCreatedTime'], '%Y-%m-%dT%H:%M:%S')
				ctime = datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, tzinfo=utc)
				record.recordCreatedTime = ctime
				record.save()

				# 导入child——bill
				update_child_charge_record_of_record(person, record, session)

	# except:
	#     print('收费写入失败 患者：%s  收费id %d' % (person.name, item['id']))
	#     return False


def update_child_charge_record_of_record(person, charge_record, session):
	# todo 导入child——bill
	# 收费条目item下面的收费账单说明（child - bill）
	# 例如交了28000，18000是微信，10000是现金

	url_child = 'https://api.linkedcare.cn:9001/api/v1/charge-order/bill-child/' + str(charge_record.id2)
	headers = get_headers(session)

	r = session.get(url_child, headers=headers)
	# totalcount = eval(r.content)["totalCount"]
	if r.status_code == 200:
		res = json.loads(r.content.decode('utf-8'))
		# print(r2)
		# totalCount = res['totalCount']
		if len(res) > 0:
			print('%s  下载到child_charge_record共 %d 个' % (person.name, len(res)))
			#  可以根据medicalRecordId，判断是否已经存入
			from charge_record.models import ChargeOrder, ChargeDetails, ChildChargeOrder

			# 导入
			items = res
			utc = pytz.utc
			for item in items:
				if ChildChargeOrder.objects.filter(id2=item['id']).count() > 0:
					# 先判断重复
					print(' %s 重复child收费id，未导入--id %s' % (person.name, item['id']))
					continue
				else:
					# try:
					if 1:
						record = ChildChargeOrder.objects.create(sourceChargeOrder=charge_record,
						                                         isImported=True, person=person, import_text=str(item),
						                                         id2=item['id'],
						                                         totalPrice=item['totalPrice'],
						                                         # planPrice=item['planPrice'],
						                                         actualPrice=item['actualPrice'],
						                                         overdue=item['overdue'],
						                                         discountPrice=item['discountPrice'],
						                                         discount=item['discount'],
						                                         actualPrice1=item['actualPrice1'],
						                                         payType=item['payType'],
						                                         recordCreatedTime_text=item['recordCreatedTime'],
						                                         doctorId=item['doctorId'],
						                                         doctorName=item['doctorName'],
						                                         comments=item['comments'],
						                                         patientId=item['patientId'],
						                                         appointmentId=item['appointmentId'],
						                                         sourceChargeOrderId=item['sourceChargeOrderId'],
						                                         status=item['status'],
						                                         isAliPay=item['isAliPay'],
						                                         isWeixinPay=item['isWeixinPay'],
						                                         )

						print(' child收费写入成功 患者：%s  收费id %d' % (person.name, item['id']))
						# return  True

						# 修改创建时间 #'2018-07-29T09:48:37'  recordCreatedTime
						dt = datetime.strptime(item['recordCreatedTime'], '%Y-%m-%dT%H:%M:%S')
						ctime = datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, tzinfo=utc)
						record.recordCreatedTime = ctime
						record.save()

			# except:
			#     print('收费写入失败 患者：%s  收费id %d' % (person.name, item['id']))
			#     return False


'''

搜索iamge也就是预约数组
https://api.linkedcare.cn:9001/api/v1/appointments/search-with-images?cancel=false&endTime=2020-02-26&isPending=false&patientId=353317
	返回的数组内images不是空，则对应的有图
	
图片post地址
	https://api.linkedcare.cn:9201/api/v1/image-upload?appointmentId=1833516&categoryId=1
'''


def uploadImageToLinkedcare(session, person):
	'''获取收费记录'''
	p = person
	if not p.linkedcareId:  # 没有id
		# 先搜索，爬取
		item = search_person_from_linked(p, session)
		# data = search_from_linked(p.name, s)
		if item:  # 判断是否有内容
			if item['name'] == p.name and item['privateId'] == p.idnum:
				# print('成功写入：pk--%d, %s id--%d' % (p.pk, p.name, p.linkedcareId))
				update_baseinfo_for_person_with_item(p, item)
				# get_charge_record_of_patient(session, person)
				# todo
				return '导入成功'

			else:
				# todo
				print('未搜到患者%s pk %d，未写入' % (p.name, p.pk))
				return '未搜到患者%s pk %d，未写入' % (p.name, p.pk)
		else:
			print('未搜到患者%s，未写入' % (p.name))
			return '未搜到患者%s pk %d，未写入' % (p.name, p.pk)

	else:  # 有id

		# 获取预约列表
		url_sum = 'https://api.linkedcare.cn:9001/api/v1/appointments/search-with-images?cancel=false' + \
		          '&endTime=2020-02-26&isPending=false&patientId=' + str(p.linkedcareId)

		headers = get_headers(session)
		# if p.charge_summary.count() == 0:  # 先检查是否存在，没有则创建
		r = session.get(url_sum, headers=headers)
		# totalcount = eval(r.content)["totalCount"]
		if r.status_code == 200:
			res = json.loads(r.content.decode('utf-8'))
			# print(r2)
			print('%s  下载到预约列表' % (p.name))
			update_image_for_apptslist(p, res)
		else:
			print('%s  下载预约失败！' % (p.name))


# post 如果有name，且为日期，则按照name的日期，
#   没有日期，是汉字啥的，则放到第一个。
#   没有name则按照upLoadTime日期。
'''

'''
from boards.models import Person, Post

def update_image_for_apptslist(person, apptItems):
	import re, time

	d2 = u"[d]+"  # 匹配 数字
	patternDigt = re.compile(r'\d+')  # 查找数字
	# pass
	utc = pytz.utc

	for post in person.posts:

		if post.name:  # post 有name
			timelist = patternDigt.findall(post.name)
			if len(timelist):  # 同时name中能提取到数字
				# 开始比较数字日期，挑选合适的
				s_time = time.mktime(time.strptime(timelist[0], '%Y%m%d'))
				for item in apptItems:
					# if not len(item['images']) == 0: #imges 不为空
					dt = datetime.strptime(item['startTime'], '%Y-%m-%dT%H:%M:%S')
					ctime = datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, tzinfo=utc)

			else:  # 取不到数字
				# 放入第一个
				pass

		else:  #post 没有name
			# 按照upLoadTime日期 选择复诊日期并上传
			pass







	#record.recordCreatedTime = ctime


	# id， startTime，endTime
	# 修改创建时间 #'2018-07-29T09:48:37'  recordCreatedTime

	# try:
	# sum = ChargeSummary.objects.create(person=person,
	#                                    totalActualPrice=items['totalActualPrice'],
	#                                    totalPlanPrice=items['totalPlanPrice'],
	#                                    totalOverdue=items['totalOverdue'],
	#                                    totalAdvacePrice=items['totalAdvacePrice'],
	#                                    importText=str(items))
	# print(' %s charge_summary 写入成功' % (person.name))




if __name__ == '__main__':
	pass
# read_jsontxt_add_link_id()
