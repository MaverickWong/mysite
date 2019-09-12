from django.conf.urls import url, include
from django.contrib import admin
from charge_record.views import *
from rest_framework import routers

#
# router = routers.DefaultRouter()
# router.register(r'users', ChargeOrderView)

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^(?P<personPk>\d+)/$', all_orders, name='allCharge'),
    url(r'^new/(?P<personPk>\d+)/$', new_record, name='newChargeRecord'),
    url(r'^print/(?P<recordPk>\d+)/$', print_record, name='printRecord'),
    url(r'^import/(?P<pk>\d+)/$', import_record, name='importRecord'),

    url(r'^api/$', ChargeOrderView.as_view(), name='api'),
    url(r'^api/test/$', testViewSet.as_view({'get': 'list', 'post': 'create'}), name='api2'),
    url(r'^login', login),

]