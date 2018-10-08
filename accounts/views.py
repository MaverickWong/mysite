# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, authenticate
from django.http import HttpResponse


# Create your views here.

def signup(request):
    # if request.method == 'POST':
    # 	form = UserCreationForm(request.POST)
    # 	if form.is_valid():
    # 		user = form.save()
    # 		auth_login(request, user)
    # 		return redirect('home')
    # else:
    # 	form = UserCreationForm()
    #
    # return  render(request,'signup.html', {'form':form})
    return HttpResponse("暂未开放注册！")


def login(request):
    if request.method == 'POST':
        if request.POST['username'] and request.POST['passwd']:
            username = request.POST['username']
            passwd = request.POST['passwd']
            user = authenticate(username=username, password=passwd)
            if user is not None and user.is_active:
                auth_login(request, user)
                return redirect('home')
            else:
                return render(request, 'login.html')
    else:
        return render(request, 'login.html')

# return  render(request,'signup.html', {'form':form})
