# 这个一定要，不然会报错，但是错误很明显，容易定位。
import mysite
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
# django版本大于1.7时需要这两句
import django
django.setup()

import json
import sys
from boards.models import *

# 开始
with open('a2.txt', 'r') as f:
    data = json.load(f)
    # print(data)
# b = json.loads(a)

print(data['pageCount'])

repeated = []
succeded = []

for item in data['items']:
    n = Person.objects.filter(idnum__contains=item['privateId']).count()
    if n > 0: #  先根据id判断是否有重复患者，如果有则登记。没有则新建患者
        repeated.append(item['privateId'] + item['name'])
    elif n == 0:

        if item['birth']:
            birth = item['birth'][0:10]
        p = Person.objects.create(idnum=item['privateId'], linkedcareId=item['id'], name=item['name'], nameCode=item['nameCode'], mobile=item['mobile'],
                                  otherPrivateId=item['otherPrivateId'], birth=birth, sex=item['sex'], doctor='zdl',
                                  doctorId=item['doctorId'], officeId=item['officeId'], clinic=item['officeId'], email=item['email'],
                                  occupation=item['occupation'], qq=item['qq'], weixin=item['weixin'], identityCard=item['identityCard'],homeAddress=item['homeAddress'],
                                  patientType=item['patientType'], lastVisit=item['lastVisit'], lastDoctorId=item['lastDoctorId']
                                  )
        # p.linkedcareId = item['id']
        succeded.append(item['privateId'] + item['name'])

with open('result.txt', 'w') as f:
    # f.write("{}  {}  {}  {}\n".format(title, price, scrible, pic))
    f.write('repeated \n')
    for i in repeated:
        f.write(i)
        f.write('\n')
        # f.write('\n')

# data['items'][0]
#           [doctorId]   id  patientid  patient{}
#                                --id  name namecode privatedId sex

# {"pageIndex": 1, "pageSize": 10, "pageCount": 6649, "totalCount": 66486, "items": [


# "id": 432693, "officeId": 0, "privateId": "8867", "otherPrivateId": null,
# "name": "\u738b\u5929\u8212A", "nameCode": null, "sex": 2, "birth": "1991-12-07T00:00:00",
# "mobile": "\u672c\u4eba:15210957869"
# "email": null, "occupation": null, "qq": null, "weixin": null,
#  "identityCard": null, "homeAddress": null,
# "patientType": "\u666e\u901a"
# "doctorId": null, "nickName": null, "lastVisit": null, "lastDoctorId": null,
# "tag": null,

# "dutyDoctorId": null,
# "sourceType": null, "refereeName": null, "refereeId": null, "sourceTypeOne": null, "sourceTypeTwo": null, "sourceTypeThree": null,
# "medicalAlert": null, "firstVisit": null, "overdue": 0.0,

# "pictureId": 0,, "isArchived": false,
# , "phoneNumber": null, "phoneNumber1": null, "phoneNumber2": null, "phoneNumber3": null, "phoneNumber4": null, "phoneNumber5": null,

#  "province": null, "city": null, "district": null, "content": null,
# "totalCount": 0,

# "marketCenterAccount": null, "aliMarketCenterAccount": null, "membershipId": null,
# "point": 0, "notes": null, "consultantId": null, "nationality": null, "medicine": "",
# "membershipTypeName": null, "cardNumber": null, "familyAddress": null, "isMembershipExpired": false,
# "onlineConsultantId": 0, "recordCreatedUser": 0, "department": null}
# "dutyDoctorName": "", "onlineConsultantName": "",
# "developerId": null, "developerName": "",  "attendantId": null, "attendantName": "",

# {"membershipTypeId": null, "membershipType": null, "doctorName": null, "lastDoctorName": null, "officeName": null,
# "recordCreatedUserName": null, "isShared": false, "shareName": null, "recordCreatedTime": "0001-01-01T00:00:00",
#  "totalAmount": null, "isSharedMembershipExpired": false,
