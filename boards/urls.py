from django.conf.urls import url
from django.contrib import admin
from boards.views import *

urlpatterns = [
	# url(r'^admin/', admin.site.urls),

	url(r'^today_person$', today_person_detail, name='today_person'),

]
