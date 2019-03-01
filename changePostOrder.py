#!/usr/bin/python
# -*- coding:utf8 -*-


# 这个一定要
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
import django
django.setup()
# django版本大于1.7时需要这两句

"""
# 对所有自动导入的Post进行排序
# 
# 
# python3 -u /home/zdl/mysite2/readfiles.py
"""

from boards.models import *
import re,shutil


d = u"[\u4e00-\u9fa5]+"  # 中文 匹配
d2 = u"[d]+"  # 匹配 数字
patternDigt = re.compile(r'\d+')   # 查找数字
patternA = re.compile(d)  # 中文

# nameList = patternA.findall(post)  # 名字
# idlist = patternDigt.findall(post)  # 数字

#
# def bubbleSort(nums):
#     for i in range(len(nums) - 1): # 遍历 len(nums)-1 次
#         for j in range(len(nums) - i - 1): # 已排好序的部分不用再次遍历
#             if nums[j] > nums[j+1]:
#                 nums[j], nums[j+1] = nums[j+1], nums[j] # Python 交换两个数不用中间变量
#     return nums

has_first = False
has_end = False
# first_pk =0
# end_pk = 0

# if 1:
for p in Person.objects.all():
	# p = Person.objects.get(pk=3744) #  zhangwei
	posts = p.posts.filter(type__lte=90)
	post_names = []

	# 提取名字
	for post in posts:
		if post.name:
			if post.name.isdigit():
				post_names.append(post.name)
			elif ('初始' in post.name):
				has_first = True
				# first_pk = post.pk
				post.type = 0
				post.save()
			elif ('结束' in post.name):
				has_end = True
				# end_pk = post.pk
				post.type = posts.count()
				post.save()
			else:
				numlist = patternDigt.findall(post.name)
				if  numlist:
					post_names.append(numlist[0])
					post.name = numlist[0]
					post.save()

	# 排序
	# post_names = bubbleSort(post_names)

	post_names.sort()
	# 更改post 的 type

	for post in posts:
		if has_first:
			if post.name in post_names:
				post.type = post_names.index(post.name) + 1
				post.save()
		else:
			if post.name in post_names:
				post.type = post_names.index(post.name)
				post.save()
				# print('  ')

	print(p.name)




