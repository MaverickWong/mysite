#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
import datetime
import time
import json
import sys

# officeId 劲松122 华贸124

# 登陆参数
logURL = "https://simaier.linkedcare.cn/LogOn"
agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3418.2 Safari/537.36"
apptURL = 'https://api.linkedcare.cn:9001/api/v1/appointments/search/paging'
# apptURL = 'https://api.linkedcare.cn:9001/api/v1/patient/search-config'
logOffUrl = "https://simaier.linkedcare.cn/logoff"
logOffPayload = {"platform": '1', "clientId": "7c378f28-6bc8-4c1a-a40e-3ba38a0b48fd"}
# payload = {"account":"zhangdongliang","password":"simaier123","validationCode":"","officeId":officeId,"platform":1,"kickOther":"false","clientId":"7c378f28-6bc8-4c1a-a40e-3ba38a0b48fd","isCheckMobileValidation":"","mobileValidationCode":""}
# requestID = "6F08187A-7490-416B-9B71-C5F3C3F323D4"
# token = "8RnfnuLoJLn9di8_kZkRVLRaLhyGi25OXCG6T8auyfAXKmSDkx4poGrTRyPwghenvqCfs7WfaiN3twZ0BP3WXK49jPh-oat79A3BDuAG-g36ZB5ZYW4RiBuKnhFu93J_H4_0Qpu8r0hDJ_ow9x_1FPQZDY24KVGTWki3wtqKN8TLEUeSkwZBWfifmvlfpcrywR1FFdKE71lCalVkz4l2yJwgtp-BrGNFmGuCw2OPGfKVx_KPIVZmMsKDWLJ8vLbtaAzestilfbsJxUjqBBvmW1tLvQuHgGs-F2LXK5AZp8n9g04HK9DJEhERJ9a0TYeO"
token = "lq64T0pchLWJyFGs2qZbpOuPhQvo2IC8XlbUc3jchF3FRPZvGQPm52F8vfxNxZCARhsLOlQbPGS_rHLIME870LECOVsf5g-1m5FAY7OCoicb47yciaOjxJD3CsX1YHRzARBwvY_84skjkn43-2oEPZ57ea7hc31oylNiMSn60HUmc9zh24BSBDAtzhacJXizIFzLjC0TGSbUWPWXjE_o16jeLY_mn8HDL9wIXDhNOImLCaXwXbPPyi7ryf-J4u0i3aR3mdt5iigI68o1o6ckOOUA5vk_Yw8wrCo5dpjxzV_dE4o6AtN9dqeuoDO-bzB3"
result = []

officeId = 122
# print(officeId)
payload = {"officeId": officeId, "account": "zhangdongliang", "password": "zhangdongliang666", "validationCode": "",
           "platform": 1, "kickOther": "false", "clientId": "7c378f28-6bc8-4c1a-a40e-3ba38a0b48fd",
           "isCheckMobileValidation": "", "mobileValidationCode": ""}
s = requests.session()
r = s.post(logURL, params=payload)
# print("login: " + r.content)
# print(s)

# 从cookie中获取token
cookie = s.cookies.get_dict()
temp = cookie['AresToken']
tempdict = eval(temp)  # 将字符串转为字典
token = tempdict["access_token"]

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
# condFields = [{"searchConfigId": 506, "code": "DoctorId", "comparator": "=", "value": "913", "officeId": 122, "id": 289}]
condFields = []

searchConfig = {"searchType": "患者查询", "name": "我的患者", "isPreferred": 'false', "isDefault": 'true',
                "userId": 745, "isAscending": 'false', "isShowWeiXin": 'false', "orderByField": "p.Id",
                "searchCondFields": condFields, "searchResultFields": searchResultFields,
                "officeId": 0, "id": 0}

searchPayload = {"searchConfig": searchConfig, "pageSize": 3000, "pageIndex": 1, "searchText": ""}

# searchResult = s.put(searchURL, params=searchPayload, headers=headers)
searchResult = s.put(searchURL, headers=headers, data=json.dumps(searchPayload))

# totalcount = eval(r.content)["totalCount"]
r2 = json.loads(searchResult.content)
print(r2)

with open('patients.txt', 'w') as f:
    json.dump(r2, f)
    # f.write("{}  {}  {}  {}\n".format(title, price, scrible, pic))
    # f.write('\n')
    f.close()
