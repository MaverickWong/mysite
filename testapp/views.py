# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


# def index(request):
# 	return HttpResponse('ok')


def index(request):
	return render(request, 'appointment/index.html')


# def testdata(request):
# with open('data.json', 'r') as f:
# 	data = json.load(f)
# 	return HttpResponse(data, content_type='application/json')

def hello(request):
	return render(request, 'upload-vue2.html')
