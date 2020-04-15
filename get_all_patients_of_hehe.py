#!/usr/bin/python
# -*- coding:utf8 -*-
# 这个一定要，不然会报错，但是错误很明显，容易定位。
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
import django,json, re

django.setup()
# django版本大于1.7时需要这两句

# python3 -u /home/zdl/mysite2/readfiles.py
#

from linkedcare.syncDB import logIn, getTokenFromSession, queryPatients
from mysite.settings import BASE_DIR
import random
# from datetime import datetime
import time

# 修正privateDir中的问题
#

agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3418.2 Safari/537.36"


# 从cookie中获取token
token = None
# token = getTokenFromSession(s)
# 组装header
headers = None
# /static/picture/zdl/zdl/zdl/zdl/zdl/李娜_7416/

error = []

from boards.models import *


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




d2 = u"[d]+"  # 匹配 数字
patternDigt = re.compile(r'\d+')

def mainfunc():
	# s = logIn()
	# token = getTokenFromSession(s)
	# headers = get_header_use_token(token)
	# queryPatients(s, pageindex=1, pageSize=10000, userId=5103)

	fname = BASE_DIR + '/linkedcare/get_patients_0226-132852.txt'
	with open(fname, 'r') as f:
		data = json.load(f)

	print(data['totalCount'])

	repeated = []
	succeded = []
	i = 0

	for item in data['items']:
		i= i+1
		idnum = item['privateId']
		linkedcareId = item['id']
		name = item['name']
		nameCode = item['nameCode']

		id2 = patternDigt.findall(idnum)[0]

		pquery = Person.objects.filter(idnum__contains=id2)
		pnum = pquery.count()
		if pnum == 0:
			newP = Person.objects.create(idnum=idnum, name=name, doctor='zdl', linkedcareId=linkedcareId, nameCode=nameCode)
		elif pnum == 1:
			newP = pquery[0]
			pquery.update(linkedcareId=linkedcareId, nameCode=nameCode)

		elif pnum > 1:  # 查询出多个患者，只登记
			query2 = pquery.filter(name__contains=name)
			query2.update(linkedcareId=linkedcareId, nameCode=nameCode)

			# if query2.count() == 1:
			# 	newP = query2[0]
			# 	query2.update(linkedcareId=linkedcareId, nameCode=nameCode)
			# else:
			# 	print("\n发现重复患者： %s,  第 %s个" % (name, str(i)))
			# 	continue

		# print('\n第 %s个， total %s')


if __name__ == '__main__':
	mainfunc()


'''#
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
'''