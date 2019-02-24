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
from mysite.views import *
from boards.views import *
from accounts import views as accounts_views
from django.contrib.auth import views as auth_views
from record import urls as recordurls

# filemanager
# from filemanager import path_end
# from mysite.views import filemanager


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^$', home, name='home'),
    url(r'^$', show_home, name='home'),
    url(r'^home2', home), #另一个主页入口，测试用

    url(r'^ip$', get_host_ip, name='hostip'),

    # url(r'^boards/(?P<pk>\d+)/$', board_topics, name='board_topics'),
    # url(r'^creat_new/$', creat_new_person, name='new_person'),
    # url(r'^(?P<pk>\d+)/$', person_detail, name='person_detail'),
    # url(r'^filer/', include('filer.urls')),
    url(r'^new/$', new_person, name='new_person'),
    url(r'^wrong/', wrong, name='wrong'),

    # 搜索
    url(r'^search/', search, name='search'),
    url(r'^search_suggest/', search_suggest, name='searchs'),

    url(r'^tags/(?P<tag>\w+[^/]+)', tag_search),
    url(r'^super_search/', super_search),
    url(r'^ss/', s_search),

    # url(r'^test/', test, name='test'),
    url(r'^del/person/(?P<pk>\d+)', delperson),
    url(r'^del/person(?P<ppk>\d+)/post(?P<postpk>\d+)', delpost),

    url(r'^detail/(?P<pk>\d+)/$', person_detail, name='person_detail'),
    url(r'^down/(?P<pk>\d+)/$', down_zip),

    url(r'^baseinfo/(?P<pk>\d+)/$', baseinfo),
    url(r'^addtag/(?P<pk>\d+)/', add_tag_for_person),

    # post 获取所有post列表
    url(r'^posts/(?P<pk>\d+)/$', posts, name='posts'),
    url(r'^posts/(?P<pk>\d+)/addpost$', addpost, name='addpost'),
    url(r'^allposts$', allposts),

    #  获取所有x线的post列表
    url(r'^posts_xray/(?P<pk>\d+)/$', posts_xray, name='posts_xray'),
    url(r'^posts_xray/(?P<pk>\d+)/addpost$', addpost_xray, name='addpost_xray'),

    # account
    url(r'^signup/$', accounts_views.signup, name='signup'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^login/$', accounts_views.login, name='login'),
    # url(r'^login/$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),

    # record
    url(r'^record/', include(('record.urls', 'record'), namespace='record')),

    url(r'^netdisk/', include('netdisk.urls')),
    url(r'^task/', include(('tasklist.urls', 'tasklist'), namespace='tasklist')),

    # 收费
    url(r'^charge/', include(('charge_record.urls', 'charge_record'), namespace='charge_record')),

    url(r'^syncDB/', syncDB, name='syncdb'),  # 从易看牙同步数据
    url(r'^sync_xray/(?P<pk>\d+)/$', sync_xray_of_linkedcare_for_person, name='sync_xray'),  # 从易看牙同步数据

    url(r'imoprtFolders', importFolders, name='importFolder'),  # 从文件夹导入图像

    # url(r'up/$', hello),
    # url(r'^p/', person_detail),
    # url(r'^abc/' + path_end, filemanager, name='filemanager'),

]
