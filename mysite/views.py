from django.http import HttpResponse

from django.shortcuts import render,redirect
from django.template import Template, Context
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required
from boards.models import *


def hello(request):
    return render(request, 'upload-vue2.html')

# def home(request):
# 	t = get_template('index.html')
# 	c = {'board': 'i am ok ', 'a':'aaaaa'}
# 	return HttpResponse( t.render(c))
#     #return render(request, 'home.html',{'board':'what ', 'a':'aaa'})



# 患者详细信息展示

@login_required()
def home(request):
    docname = request.user.username
    if request.user.is_authenticated:
        if docname == 'zdl': #  用户名为zdl时，可以查看所有患者
            persons =  Person.objects.order_by('idnum').reverse()[:16]
            total = Person.objects.all().count()

        else:  #  只能看该医生的患者
            persons = Person.objects.filter(doctor=docname).reverse()[:16]
            total = Person.objects.filter(doctor=docname).count()

        tags = Tag.objects.all()
        return render(request, 'index.html', {'persons': persons, 'total':total, 'tags':tags})
    else:
        return redirect('login')

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

