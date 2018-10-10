from django.conf.urls import url, include
from django.contrib import admin
from netdisk.views import *
urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    # url(r'^(?P<repath>\w+)', showPath, name='showPath'),
    # url(r'^new/(?P<personPk>\d+)/$', newRecord, name='newRecord'),
    # url(r'^$', home),
    url(r'^', showPath, name='showPath'),

]