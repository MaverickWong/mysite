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
# from boards.views import *
from accounts import views as accounts_views
from django.contrib.auth import views as auth_views
from record import urls as recordurls
from django.views.generic.base import TemplateView

from rest_framework.authtoken.views import obtain_auth_token


# 测试 restful-api
from charge_record.views import ChargeOrderViewSet, ChargeSummaryViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'chargeorder', ChargeOrderViewSet)
router.register(r'chargesum', ChargeSummaryViewSet)



urlpatterns = [
	url(r'^api/', include(router.urls)),  # 测试restful
	url('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', obtain_auth_token), # api认证返回token
    url('test3', TemplateView.as_view(template_name='index.html')),

    url(r'^admin/', admin.site.urls),
    # url(r'^$', home, name='home'),
    # url(r'^$', bad, name='home'),  # 维护升级用
    url(r'^$', show_home, name='home'),   # 第1主页入口
    url(r'^list_by_page', list_by_page, name='list_by_page'),  # 第二主页入口

    url(r'^syncDB/', syncDB, name='syncdb'),  # 从易看牙同步数据
    url(r'^sync_xray/(?P<pk>\d+)/$', sync_xray_of_linkedcare_for_person, name='sync_xray'),  # 从易看牙同步数据
    url(r'imoprtFolders', importFolders, name='importFolder'),  # 从文件夹导入图像
    url(r'^ip$', get_host_ip, name='hostip'),
    # url(r'^test/', test, name='test'),
    # url(r'^testdata/', testdata),
    # 统计post
    url(r'^allposts$', allposts),

    # 应用
    url(r'^test/', include(('testapp.urls', 'testapp'), namespace='test')),
    url(r'^search/', include(('search.urls', 'search'), namespace='search')),
    url(r'^boards/', include(('boards.urls', 'boards'), namespace='boards')),
    # baseinfo
    url(r'^baseinfo/', include(('baseinfo.urls', 'baseinfo'), namespace='baseinfo')),
    # record
    url(r'^record/', include(('record.urls', 'record'), namespace='record')),
    url(r'^netdisk/', include('netdisk.urls')),
    url(r'^task/', include(('tasklist.urls', 'tasklist'), namespace='tasklist')),
    url(r'^sum/', include(('summary.urls', 'summary'), namespace='summary')),
    url(r'^appt/', include(('appointment.urls', 'appointment'), namespace='appointment')),
    # 收费
    url(r'^charge/', include(('charge_record.urls', 'charge_record'), namespace='charge_record')),
	url(r'^storage/', include(('storage.urls', 'storage'), namespace='storage')),

    # account
    url(r'^signup/$', accounts_views.signup, name='signup'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^login/$', accounts_views.login, name='login'),

	url(r'^user/login$', login2, name='login2'),
	url(r'^user/info', getinfo),

    # url(r'^login/$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),

]
