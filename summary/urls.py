from django.conf.urls import url, include
from django.contrib import admin
from .views import *

urlpatterns = [
	# url(r'^admin/', admin.site.urls),
	# url(r'^(?P<personPk>\d+)/$', total, name='recordHome'),
	# url(r'^new/(?P<personPk>\d+)/$', newRecord, name='newRecord'),
	url(r'^$', home, name='home'),
	url(r'^month/', num_of_month),
	# url(r'^edit/(?P<pk>\d+)/$', edit),
	# url(r'^del/(?P<pk>\d+)/$', del_task),
	# url(r'^search$', search_task, name='search'),
	# url(r'^group$', search_group, name='search_group'),

]
