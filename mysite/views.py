from django.http import HttpResponse

from django.shortcuts import render
from django.template import Template, Context
from django.template.loader import get_template

def hello(request):
    return HttpResponse("Hello world, "+ request.get_host())

def home(request):
	t = get_template('index.html')
	c = {'board': 'i am ok ', 'a':'aaaaa'}
	return HttpResponse( t.render(c))
    #return render(request, 'home.html',{'board':'what ', 'a':'aaa'})
