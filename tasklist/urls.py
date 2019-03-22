from django.conf.urls import url, include
from django.contrib import admin
from tasklist.views import *

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    # url(r'^(?P<personPk>\d+)/$', total, name='recordHome'),
    # url(r'^new/(?P<personPk>\d+)/$', newRecord, name='newRecord'),
    url(r'^$', home, name='taskhome'),
    url(r'^add/', add),
    url(r'^edit/(?P<pk>\d+)/$', edit),
    url(r'^del/(?P<pk>\d+)/$', del_task),
    url(r'^search$', search_task, name='search'),
    url(r'^group$', search_group, name='search_group'),

]