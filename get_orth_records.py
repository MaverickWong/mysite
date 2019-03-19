#!/usr/bin/python
# -*- coding:utf8 -*-
# 这个一定要，不然会报错，但是错误很明显，容易定位。
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
import django
django.setup()
# django版本大于1.7时需要这两句

# python3 -u /home/zdl/mysite2/readfiles.py
#

from boards.models import Person
from record.models import Record
from linkedcare.syncDB import logIn, getTokenFromSession, get_ortho_record_of_patient, search_person_from_linked
from mysite.settings import  BASE_DIR
import random
# from datetime import datetime
import time

# 修正privateDir中的问题
#

agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3418.2 Safari/537.36"
# linkedcareId = 432349
# UrlGetApptList = "https://api.linkedcare.cn:9001/api/v1/appointment-record/patient/"
# https: // api.linkedcare.cn: 9001 / api / v1 / appointment - record / patient / 432349

# UrlGetImage = "https://api.linkedcare.cn:9001/api/v1/imaging?appointmentId="
# https://api.linkedcare.cn:9001/api/v1/imaging?appointmentId=1222210
# s = logIn()

# 从cookie中获取token
token = None
# token = getTokenFromSession(s)
# 组装header
headers =None
#/static/picture/zdl/zdl/zdl/zdl/zdl/李娜_7416/


error=[]




def get_header_use_token(token):
    header = {'authority': 'api.linkedcare.cn:9001',
               "authorization": "bearer " + token, "access_token": token,
               # "clientId":"7c378f28-6bc8-4c1a-a40e-3ba38a0b48fd",
               "origin": "https://simaier.linkedcare.cn",
               'Connection': 'keep-alive', 'user-agent': agent,
               'referer': 'https://simaier.linkedcare.cn/',
               'content-type': 'application/json;charset=UTF-8'
               }
    return header


def mainfunc():
	s = logIn()
	token = getTokenFromSession(s)
	headers = get_header_use_token(token)

	persons = Person.objects.all()
	total = persons.count()
	i = 0

	for p in persons:
		i = i + 1
		time.sleep(random.uniform(0, 2))

		get_ortho_record_of_patient(s, p)

		# if p.linkedcareId:  #  有id
		# 	# time.sleep(random.randint(1, 5))
		# 	get_ortho_record_of_patient(s, p)
		#
		# else:  # 无id
		# 	item = search_person_from_linked(p, s)
		# 	if item:
		# 		p.linkedcareId =  item['privateId']
		# 		p.save()
		# 		get_ortho_record_of_patient(s, p)

		print('\n第 %s个， total %s' % (str(i), str(total)))


mainfunc()
#
# if __name__ == '__main__':
# 	pass


# print('\n完成，正在生成log文件。。。。')

# dt = datetime.now()
# time2 = dt.strftime("%m%d-%H%M%S")
#
# fname3 = 'log/log_privDir' + time2 + '.txt'
# with open(fname3, 'w+') as f:
#     f.write('\n错误********************************************\n')
#     # f.write('name' + ' ' + 'id' + ' ' + 'path' + '\n')
#     f.write('总计：' + str(len(error)) + '\n')
#     for d in error:
#         f.write(d + '\n')