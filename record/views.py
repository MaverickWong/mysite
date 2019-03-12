# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from boards.models import *
from record.models import *

# Create your views here.

def newRecord(request, personPk):
    if request.method == 'GET':
        return render(request, 'record/new.html', {'pk':personPk})
    else:
        complain = request.POST.get('complain')
        exam = request.POST.get('exam')
        treat = request.POST.get('treat')
        note = request.POST.get('note')

        p = Person.objects.get(pk=personPk)
        try:
            new_record = Record.objects.create(doctor=request.user,
                                        exam=exam,
                                        complain=complain,
                                        treatmentPlan=treat,
                                        note=note,
                                        )
            new_record.person.add(p)
            # url = reverse('person_detail', kwargs={'pk':personPk}) + '?tab=3'
            # return HttpResponse('保存成功')
            # return redirect(url)

            # todo 保存后应该只返回状态，让前端出通知，不用后面的再查询浪费
            p = Person.objects.get(pk=personPk)
            records = p.records.order_by('createdAt').reverse()
            return render(request, 'record/total.html', {'records': records, 'pk': personPk, 'succeed':1})
        except:
            # return HttpResponse('保存失败')
            p = Person.objects.get(pk=personPk)
            records = p.records.order_by('createdAt').reverse()
            return render(request, 'record/total.html', {'records': records, 'pk': personPk, 'succeed': 0})

def total(request, personPk):
    p = Person.objects.get(pk=personPk)
    # if p.records.count()>0:
    #     return render(request, 'record/total.html', {'records': p.records})
    # else:
    #     return render(request, 'record/total.html')
    records = p.records.order_by('createdAt').reverse()

    return render(request, 'record/total.html', {'records': records, 'pk': personPk})


def delRecord(request,  personPk, recordPk):
    record = Record.objects.get(pk=recordPk)
    record.delete()

    p = Person.objects.get(pk=personPk)
    records = p.records.order_by('createdAt').reverse()

    return render(request, 'record/total.html', {'records': records, 'pk': personPk})