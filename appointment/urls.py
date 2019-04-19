from django.conf.urls import url
from appointment.views import *

urlpatterns = [
	# url(r'^admin/', admin.site.urls),
	# url(r'^(?P<personPk>\d+)/$', total, name='recordHome'),
	# url(r'^new/(?P<personPk>\d+)/$', newRecord, name='newRecord'),
	url(r'^$', home, name='apptHome'),
	url(r'^update/', update_today_appts, name='update_today'),
	# url(r'^edit/(?P<pk>\d+)/$', edit),
	# url(r'^editlabel/(?P<pk>\d+)/$', edit_comment_label, name='edit_label' ),

	# url(r'^del/(?P<pk>\d+)/$', del_task),

]
