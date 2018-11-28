from django.conf.urls import url
from django.contrib import admin
from record.views import *

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^(?P<personPk>\d+)/$', total, name='recordHome'),
    url(r'^new/(?P<personPk>\d+)/$', newRecord, name='newRecord'),

]