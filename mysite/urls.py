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


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', home, name='home'),
    # url(r'^boards/(?P<pk>\d+)/$', board_topics, name='board_topics'),
    # url(r'^creat_new/$', creat_new_person, name='new_person'),
    # url(r'^(?P<pk>\d+)/$', person_detail, name='person_detail'),
    # url(r'^filer/', include('filer.urls')),
    url(r'^new/$', new_person, name='new_person'),
    url(r'^wrong/', wrong, name='wrong'),
    url(r'^search/', search, name='search'),
    url(r'^tags/(?P<tag>\w+)', tag_search),
    # url(r'^test/', test, name='test'),
    url(r'^del/person/(?P<pk>\d+)', delperson),
    url(r'^del/person(?P<ppk>\d+)/post(?P<postpk>\d+)', delpost),

    url(r'^detail/(?P<pk>\d+)/$', person_detail, name='person_detail'),

    #post
    url(r'^posts/(?P<pk>\d+)/$', posts, name='posts'),
    url(r'^posts/(?P<pk>\d+)/addpost$', addpost, name='addpost'),

    # account
    url(r'^signup/$', accounts_views.signup, name='signup'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^login/$', accounts_views.login, name='login'),
    # url(r'^login/$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),

    # record
    url(r'^record/', include(('record.urls', 'record'), namespace='record')),

    url(r'^netdisk/', include('netdisk.urls')),
    # url(r'upfile/$', upfile),
    # url(r'^p/', person_detail),
]
