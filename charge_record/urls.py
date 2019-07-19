from django.conf.urls import url
from django.contrib import admin
from charge_record.views import *

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^(?P<personPk>\d+)/$', all_orders, name='allCharge'),
    url(r'^new/(?P<personPk>\d+)/$', new_record, name='newChargeRecord'),
    url(r'^print/(?P<recordPk>\d+)/$', print_record, name='printRecord'),

]