from django.conf.urls import url
# from django.contrib import admin
from boards.views import *

urlpatterns = [
	url(r'^$', home),
	# 今日患者
	url(r'^today_person$', today_person_detail, name='today_person'),
	# 详细信息
	url(r'^detail/(?P<pk>\d+)/$', person_detail, name='person_detail'),
	url(r'^detail_no_sidebar/(?P<pk>\d+)/$', person_detail_without_sidebar, name='person_detail_without_sidebar'),

	# post 获取所有post列表
	url(r'^posts/(?P<pk>\d+)/$', posts, name='show_posts'),
	url(r'^posts/(?P<pk>\d+)/addpost$', addpost, name='addpost'),

	#  获取所有x线的post列表
	url(r'^posts_xray/(?P<pk>\d+)/$', posts_xray, name='show_posts_xray'),
	url(r'^posts_xray/(?P<pk>\d+)/addpost$', addpost_xray, name='addpost_xray'),

	# 新建患者
	url(r'^new/$', new_person, name='new_person'),

	url(r'^wrong/', wrong, name='wrong'),  # 重复患者
	# url(r'^test/', test, name='test'),
	# url(r'^testdata/', testdata),

	# url(r'^ss/', s_search),

	url(r'^del/person/(?P<pk>\d+)', delperson),
	url(r'^del/person(?P<ppk>\d+)/post(?P<postpk>\d+)', delpost),

	# 下载所有照片
	url(r'^down/(?P<pk>\d+)/$', down_zip, name='down_posts'),
	url(r'^downm/(?P<pk>\d+)/$', down_mid_zip, name='down_mid'),
	url(r'^downpost/(?P<postpk>\d+)/', down_post_mid_zip, name='down_post_mid'),
	url(r'^downpostfull/(?P<postpk>\d+)/', down_post_zip, name='down_post_full'),

	# 为person添加tag
	url(r'^addtag/(?P<pk>\d+)/', add_tag_for_person, name='add_tag'),

]
