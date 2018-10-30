#!/usr/bin/python
# -*- coding: UTF-8 -*-
import mysite
# 这个一定要，不然会报错，但是错误很明显，容易定位。
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
import django
django.setup()
# django版本大于1.7时需要这两句

from datetime import datetime
import requests
import json
import sys
from boards.models import *

agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3418.2 Safari/537.36"


def test():
    print('tesst')


# 开始
def logIn(officeId=122, userId = 745):
    # officeId 劲松122 华贸124
    # officeId = 122
    # test()
    userId = 745
    account = "zhangdongliang"
    passwd = "zhangdongliang666"
    # 登陆参数
    logURL = "https://simaier.linkedcare.cn/LogOn"
    agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3418.2 Safari/537.36"

    # print(officeId)
    payload = {"officeId": officeId, "account": account, "password": passwd, "validationCode": "",
               "platform": 1, "kickOther": "false", "clientId": "7c378f28-6bc8-4c1a-a40e-3ba38a0b48fd",
               "isCheckMobileValidation": "", "mobileValidationCode": ""}
    # 登录并获得session
    s = requests.session()
    r = s.post(logURL, params=payload)

    return s

# 从cookie中获取token
def getTokenFromSession(s):
    cookie = s.cookies.get_dict()
    temp = cookie['AresToken']
    tempdict = eval(temp)  # 将字符串转为字典
    token = tempdict["access_token"]
    return token

# # 组装header
# def getHeaders():
#     token=
#     headers = {'authority': 'api.linkedcare.cn:9001',
#                "authorization": "bearer " + token, "access_token": token,
#                # "clientId":"7c378f28-6bc8-4c1a-a40e-3ba38a0b48fd",
#                "origin": "https://simaier.linkedcare.cn",
#                'Connection': 'keep-alive', 'user-agent': agent,
#                'referer': 'https://simaier.linkedcare.cn/',
#                'content-type': 'application/json;charset=UTF-8'
#                }
#     return headers


def queryPatients(session, officeId=122, userId = 745):
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

    searchResultFields = [
        {"searchConfigId": 0, "code": "Name", "showOrder": 0, "officeId": 0, "id": 0},
        {"searchConfigId": 0, "code": "PrivateId", "showOrder": 1, "officeId": 0, "id": 0},
        {"searchConfigId": 0, "code": "Sex", "showOrder": 2, "officeId": 0, "id": 0},
        {"searchConfigId": 0, "code": "Birth", "showOrder": 3, "officeId": 0, "id": 0},
        {"searchConfigId": 0, "code": "Mobile", "showOrder": 4, "officeId": 0, "id": 0}]
    condFields = []
    # condFields= [{"searchConfigId": "", "code": "FirstVisit", "comparator": ">", "value": "2018-10-20"}]
    searchConfig = {"searchType": "患者查询", "name": "我的患者", "isPreferred": 'false', "isDefault": 'true',
                    "userId": userId, "isAscending": 'false', "isShowWeiXin": 'false', "orderByField": "p.Id",
                    "searchCondFields": condFields, "searchResultFields": searchResultFields,
                    "officeId": 0, "id": 0}

    searchPayload = {"searchConfig": searchConfig, "pageSize": 10, "pageIndex": 1, "searchText": ""}

    # searchResult = s.put(searchURL, params=searchPayload, headers=headers)
    searchResult = s.put(searchURL, headers=headers, data=json.dumps(searchPayload))

    # totalcount = eval(r.content)["totalCount"]
    r2 = json.loads(searchResult.content)
    print(r2)

    return r2



# data = queryPatients()

# with open('a2.txt', 'r') as f:
#     data = json.load(f)
#     # print(data)
# # b = json.loads(a)

# print(data['pageCount'])

def addID():
    repeated = []
    succeded = []
    office =['124', '122']
    n  = 0
    for id in office:
        data = queryPatients(id) # 从易看牙获得数据

        for item in data['items']:
            ps = Person.objects.filter(idnum__contains=item['privateId']).filter(name__contains=item['name'])
            if ps.count() ==1:  # 先根据id判断是否有重复患者，如果有则登记。没有则新建患者
                p = ps[0]
                p.linkedcareId = item['id']
                p.save()
                n=n+1
                succeded.append(item['privateId'] + '.' +item['name']+'.'+ id)

    with open('id.txt', 'w') as f:
        # f.write("{}  {}  {}  {}\n".format(title, price, scrible, pic))

        f.write('totaol' + n)
        f.write('succeded \n')
        for i in succeded:
            f.write(i)
            f.write('\n')


def get_fill_DB():
    repeated = []
    succeded = []

    office =['124', '122']
    for id in office:
        s = logIn()
        data = queryPatients(s, id) # 从易看牙获得数据

        for item in data['items']:
            n = Person.objects.filter(idnum__contains=item['privateId']).count()

            if n > 0: #  先根据id判断是否有重复患者，如果有则登记。没有则新建患者
                repeated.append(item['privateId'] + item['name'])
            elif n == 0:
                if item['birth']:
                    birth = item['birth'][0:10]
                else:
                    birth = None
                p = Person.objects.create(idnum=item['privateId'], name=item['name'], nameCode=item['nameCode'], mobile=item['mobile'],
                                          otherPrivateId=item['otherPrivateId'], birth=birth, sex=item['sex'], doctor='zdl',
                                          doctorId=item['doctorId'], officeId=item['officeId'], clinic=item['officeId'], email=item['email'],
                                          occupation=item['occupation'], qq=item['qq'], weixin=item['weixin'], identityCard=item['identityCard'],homeAddress=item['homeAddress'],
                                          patientType=item['patientType'], lastVisit=item['lastVisit'], lastDoctorId=item['lastDoctorId']
                                          )
                succeded.append(item['privateId'] + item['name'])

    with open('result.txt', 'w') as f:
        # f.write("{}  {}  {}  {}\n".format(title, price, scrible, pic))
        f.write('repeated \n')
        for i in repeated:
            f.write(i)
            f.write('\n')
            # f.write('\n')
        f.write('\n\n================================================== \n')

        f.write('succeded: \n')
        f.write(succeded.count())
        for i in succeded:
            f.write(i)
            f.write('\n')






# s = logIn()
# getXrayRecordOfPatient(s)