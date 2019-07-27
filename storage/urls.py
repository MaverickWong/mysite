from django.conf.urls import url, include
from django.contrib import admin
from .views import *

urlpatterns = [
	# url(r'^admin/', admin.site.urls),
	# url(r'^(?P<personPk>\d+)/$', total, name='recordHome'),
	# url(r'^new/(?P<personPk>\d+)/$', newRecord, name='newRecord'),
	url(r'^$', home, name='home'),
	url(r'^add/', add, name='additem'),
	url(r'^edit/(?P<pk>\d+)/$', edit, name='edit'),
	url(r'^inout/(?P<drugpk>\d+)/$', inout, name='inout'),
	url(r'^inout_detail/(?P<drugpk>\d+)/$', inout_detail, name='inout_detail'),

	url(r'^del/(?P<pk>\d+)/$', del_task, name='del'),
	url(r'^search$', search_task, name='search'),
	url(r'^group$', search_group, name='search_group'),

]
