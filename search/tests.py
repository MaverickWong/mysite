# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.urls import reverse


# Create your tests here.


class SearchTest(TestCase):
	def test_search_home_status_code(self):
		url = reverse('search_index')
		re = self.client.get(url)
		self.assertEqual(re.status_code, 200)

	def test_search_suggest_status_code(self):
		url = reverse('search_suggest')
		re = self.client.get(url)
		self.assertEqual(re.status_code, 200)

	def test_tag_search_status_code(self):
		url = reverse('tag_search')
		re = self.client.get(url)
		self.assertEqual(re.status_code, 200)

	def test_super_search_status_code(self):
		url = reverse('super_search')
		re = self.client.get(url)
		self.assertEqual(re.status_code, 200)
	# def test_home_url_resolves(self):
	#     url = '/boards/'
	#     re = self.client.get(url)
	#     # print(re.path)
	#     self.assertEqual(re.status_code, 200)
