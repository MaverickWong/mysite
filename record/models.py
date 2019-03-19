# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from boards.models import *
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Record(models.Model):
    doctorId = models.IntegerField(null=True)
    # "doctorName":"张栋梁",
    doctor = models.ForeignKey(User, related_name='records', null=True, on_delete=models.SET_NULL)
    person = models.ForeignKey(Person, related_name='records', null=True, on_delete=models.SET_NULL)

    # 易看牙病例号
    medicalRecordId = models.IntegerField(null=True)

    complain = models.TextField(max_length=128, null=True)
    exam = models.TextField(max_length=512, null=True)
    treatmentPlan = models.TextField(max_length=512, null=True)
    teethcode = models.TextField(max_length=128, null=True)

    # 医嘱
    note =  models.TextField(max_length=128, null=True)

    comment = models.TextField(max_length=128, null=True)

    updatedAt = models.DateTimeField(auto_now=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    createdAtLinkedcare = models.TextField(max_length=32, null=True)


    # {"planPrice":0.0,
# "imageId":26186,
# "drugorderId":0,
# "patientDocumentId":0,
# "outProcessorderId":0,
# "chargeOrderTagId":0,
# "generalExamId":0,
# "perioExam":0,
# "followupId":133903,
# "id":452444,
# "patientId":256342,
# "patientName":null,
# "appointId":833190,
# "medicalRecordType":0,
# "appointDateTime":"2017-04-28T14:30:00",
# "chiefComplaint":"",
# "history":"",
# "pastHistory":"",
# "firstVisit":true,
# "advice":"",
# "archive":"",
# "doctorId":"913",

# "nurseId":"0",
# "nurseName":"",
# "comment":"",

# "recordDateTime":"2017-04-28T14:28:43",
# "officeId":124,
# "chargeOrderId":null,
# "diagnoseRecordList":[],
# "cureRecordList":[{"id":541420,"mid":452444,"cure":"37. 47 粘颊管。 下颌18镍钛<br/>下次拍X片鉴别11， 21牙根， 之后拔牙","fdiToothCodes":"","doctorName":null}],
# "oralCheckRecordList":[],
# "radiologyCheckRecordList":[],
# "treatmentPlanList":[],
# "treatmentAdviceList":[],
# "isHistory":false}
