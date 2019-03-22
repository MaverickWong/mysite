from django.conf.urls import url, include
# from django.contrib import admin
from baseinfo.views import *

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    # url(r'^(?P<personPk>\d+)/$', total, name='recordHome'),
    # url(r'^new/(?P<personPk>\d+)/$', newRecord, name='newRecord'),
    url(r'^(?P<pk>\d+)/$', home, name='baseinfohome'),
    # url(r'^add/', add),
    url(r'^edit/(?P<pk>\d+)/$', edit),
    url(r'^editlabel/(?P<pk>\d+)/$', edit_comment_label, name='edit_label' ),

    # url(r'^del/(?P<pk>\d+)/$', del_task),

]