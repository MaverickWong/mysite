"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from mysite.views import hello
from boards.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', home, name='home'),
    # url(r'^boards/(?P<pk>\d+)/$', board_topics, name='board_topics'),
    # url(r'^creat_new/$', creat_new_person, name='new_person'),
    url(r'^(\d+)/$', person_detail, name='person_detail'),
    url(r'^filer/', include('filer.urls')),
    url(r'new/$', new_person, name='new_person'),
    # url(r'upfile/$', upfile),
    # url(r'^p/', person_detail),
]
