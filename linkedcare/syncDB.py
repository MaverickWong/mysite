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


def test():
    print('tesst')


# 开始
def logIn(officeId=122, userId = 745):
    # officeId 劲松122 华贸124
    # officeId = 122
    # test()
    userId = 745
    account = "zhangdongliangzl"
    passwd = "simaierzl123"
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

    if r.status_code == 200:
        print('登录成功')
    else:
        print('登录失败')

    return s

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
               # "clientId":"7c378f28-6bc8-4c1a-a40e-3ba38a0b48fd",
               "origin": "https://simaier.linkedcare.cn",
               'Connection': 'keep-alive', 'user-agent': agent,
               'referer': 'https://simaier.linkedcare.cn/',
               'content-type': 'application/json;charset=UTF-8'
               }
    return headers


def queryPatients(session, pageindex=1, pageSize=10, officeId=122, userId = 2042):
    '''
    从易看牙同步患者基本信息，并保存到文件
    :param session:
    :param pageindex: 默认1
    :param pageSize: 默认1000
    :param officeId: 劲松122 华贸124 默认劲松
    :param userId: 默认2042
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
    print(data)

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
    id=122
    total_page_num = int(total/10)
    # i = 1;
    s = logIn(officeId=id)

    for i in range(total_page_num):
    # for id in office:
        data = queryPatients(s, pageindex=i+1)  # 从易看牙获得数据bing保存到文件

        totalPages = data['pageCount']

        # 导入到数据库
        for item in data['items']:
            if item['doctorName'] == '913':# 筛选张老师的患者
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
                                              doctorId=item['doctorId'], officeId=item['officeId'], clinic=item['officeId'],
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
    searchResult = session.get(searchURL,  params=payload, headers=headers)

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
    print(data['totalCount'])

    if data['totalCount'] ==0:
        return None
    else:
        for item in data['items']:
            if item['privateId'] == person.idnum:
                print('找到：pk--%d, %s 对应id--%d' % (person.pk, person.name, item['id']))
                return item


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
    if item['birth']:
        birth = item['birth'][0:10]
        person.birth=birth
        person.save()
    else:
        birth = None

    try:
        person.linkedcareId=item['id']
        person.mobile=item['mobile']
        person.nameCode=item['nameCode']
        person.save()
        person.sex=item['sex']
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

    except :
        print('baseinfo 写入失败')
        return False


def get_baseinfo_of_patient(session, person):
    '''
    爬取患者基本信息，并存入数据库
    适用于无linkedcareId的患者
    :param s: session
    :param linkedcareId:
    :return: json模型
    '''
    p=person
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
        if Record.objects.filter(medicalRecordId=item['medicalRecordId']).count() >0:
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
                print('正畸病例写入成功 患者：%s  病例id %d' %(person.name, item['medicalRecordId']))
                # return  True

                # 修改创建时间 #'2018-07-29T09:48:37'
                dt = datetime.strptime(item['recordCreatedTime'], '%Y-%m-%dT%H:%M:%S')
                ctime = datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, tzinfo=utc)
                record.createdAt = ctime
                record.save()

            except:
                print('正畸病例写入失败 患者：%s  病例id %d' %(person.name, item['medicalRecordId']))
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
    p=person
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
                # print('未写入')
                return False
        else:
            # print('未写入\n')
            return False

    else:  # 有id
        url = 'https://api.linkedcare.cn:9001/api/v1/medical-record-summary?id=' + str(p.linkedcareId) +'&type=1'
        headers = get_headers(session)
        searchResult = session.get(url, headers=headers)
        # totalcount = eval(r.content)["totalCount"]
        items = json.loads(searchResult.content.decode('utf-8'))
        # print(r2)

        if len(items) > 0:
            print('下载到record共 %d 个\n' % (len(items)))
            return update_ortho_record_of_patient(p, items)

        else:
            return False


if __name__ == '__main__':
    pass
    # read_jsontxt_add_link_id()