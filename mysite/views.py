from django.http import HttpResponse

from django.shortcuts import render
from django.template import Template, Context
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required
from boards.models import Person
def hello(request):
    return HttpResponse("Hello world, "+ request.get_host())

def home(request):
	t = get_template('index.html')
	c = {'board': 'i am ok ', 'a':'aaaaa'}
	return HttpResponse( t.render(c))
    #return render(request, 'home.html',{'board':'what ', 'a':'aaa'})



# 患者详细信息展示
@login_required()
def person_detail(request, pk):
    p = Person.objects.get(pk=pk)
    name = p.name

    picurl = ''
    if p.icon:
        picurl = p.icon
        print(picurl)

    posts = p.posts

    contex = {'patient': p,  'posts': posts}

    # return render(request, 'detail.html', contex)
    return render(request, 'detail2.html', contex)

