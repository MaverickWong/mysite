from django.conf.urls import url
from .views import *

urlpatterns = [
	url(r'^$', index, name='testHome'),
	# url(r'^new/(?P<personPk>\d+)/$', newRecord, name='newRecord'),
	# url(r'^import/(?P<personPk>\d+)/$', importRecord, name='import'),
	#
	# url(r'^del/(?P<personPk>\d+)/(?P<recordPk>\d+)$', delRecord, name='delRecord'),
	# url(r'^edit/(?P<personPk>\d+)/(?P<recordPk>\d+)$', editRecord, name='editRecord'),

]
