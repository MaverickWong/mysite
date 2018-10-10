# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render
from boards.models import *
from record.models import *

# Create your views here.

def newRecord(request, personPk):
    if request.method == 'GET':
        return render(request, 'record/new.html', {'pk':personPk})
    else:
        complain =  request.POST.get('complain')
        exam = request.POST.get('exam')
        treat = request.POST.get('treat')
        note = request.POST.get('note')

        p = Person.objects.get(pk=personPk)
        try:
            new = Record.objects.create(doctor=request.user,
                                        complain= complain,
                                        treatmentPlan=treat,
                                        note=note,
                                        )
            new.person.add(p)
            return HttpResponse('保存成功')
        except:
            return HttpResponse('保存失败')


def total(request, personPk):
    p = Person.objects.get(pk=personPk)
    # if p.records.count()>0:
    #     return render(request, 'record/total.html', {'records': p.records})
    # else:
    #     return render(request, 'record/total.html')
    records = p.records.order_by('createdAt')

    return render(request, 'record/total.html', {'records': records, 'pk': personPk})


