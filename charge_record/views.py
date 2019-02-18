from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from boards.models import *
# from record.models import *
from charge_record.models import  *
# Create your views here.


def new_record(request, personPk):
    """
    新建收费记录
    :param request:
    :param personPk:
    :return:
    """
    if request.method == 'GET':
        return render(request, 'charge_record/new.html', {'pk':personPk})
    else:
        planPrice =  request.POST.get('planPrice')
        inPrice = request.POST.get('inPrice')
        comment = request.POST.get('comment')
        # note = request.POST.get('note')

        p = Person.objects.get(pk=personPk)
        try:
            newOrder = ChargeOrder.objects.create(doctor=request.user,
                                             planPrice=float(planPrice),
                                             inPrice=float(inPrice),
                                             comment=comment
                                            # note=note,
                                            )
            newOrder.person=p
            newOrder.save()

            # todo 保存后应该只返回状态，让前端出通知，不用后面的再查询浪费
            p = Person.objects.get(pk=personPk)
            records = p.charge_orders.order_by('createdAt').reverse()
            context = {'records': records, 'pk': personPk, 'succeed': 1}
            return render(request, 'charge_record/total.html', context)
            # url = reverse('person_detail', kwargs={'pk':personPk}) + '?tab=4'
            # context = {'succeed':0, 'pk':personPk}
            # return HttpResponse('保存成功')
            # return render(request, 'charge_record/result.html', context)
        except:
            p = Person.objects.get(pk=personPk)
            records = p.charge_orders.order_by('createdAt').reverse()
            context = {'records': records, 'pk': personPk, 'succeed': 0}
            return render(request, 'charge_record/total.html', context)

            # context = {'succeed':0, 'pk':personPk}
            # return render(request, 'charge_record/result.html', context)
            # return HttpResponse('保存失败,请重新输入！')


def all_orders(request, personPk):
    """
    获取该患者 所有 收费记录
    :param request:
    :param personPk:
    :return:
    """
    p = Person.objects.get(pk=personPk)

    records = p.charge_orders.order_by('createdAt').reverse()
    context = {'records': records, 'pk': personPk}
    return render(request, 'charge_record/total.html', context)


