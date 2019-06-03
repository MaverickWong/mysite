from django.conf.urls import url
# from django.contrib import admin
from .views import *

urlpatterns = [

	# 查询首页
	url(r'^search_patients/', search_index, name='search_index'),

	# 导航栏搜索建议
	url(r'^search_suggest/', search_suggest, name='search_suggest'),
	# 导航栏搜索
	# url(r'^$', navbar_search, name='nav_search'),

	# 单标签搜索
	url(r'^tags/(?P<tag>\w+[^/]+)', tag_search, name='tag_search'),
	# 多标签 联合搜索
	url(r'^super_search/', super_search, name='super_search'),

	# url(r'^ss/', s_search),

]
