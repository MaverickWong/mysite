from django.conf.urls import url
from appointment.views import *

urlpatterns = [
	# url(r'^admin/', admin.site.urls),
	url(r'^(?P<personPk>\d+)/$', list_all, name='list_all'),
	url(r'^new/(?P<personPk>\d+)/$', newRecord, name='newRecord'),
	url(r'^$', home, name='apptHome'),
	url(r'^update/', update_today_appts, name='appts_one_month'),
	url(r'^edit/(?P<personPk>\d+)/(?P<recordPk>\d+)$', edit, name='edit'),
	# url(r'^editlabel/(?P<pk>\d+)/$', edit_comment_label, name='edit_label' ),

	# url(r'^del/(?P<pk>\d+)/$', del_task),

]
