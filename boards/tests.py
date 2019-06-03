# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase, RequestFactory
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from .models import Person, Post
from .views import person_detail
from datetime import datetime

# Create your tests here.


class HomeTest(TestCase):
	def test_home_view_status_code(self):
		url = reverse('home')
		re = self.client.get(url)
		self.assertEqual(re.status_code, 200)

	def test_home_url_resolves(self):
		url = '/boards/'
		re = self.client.get(url)
		# print(re.path)
		self.assertEqual(re.status_code, 200)


class BoardPersonTests(TestCase):
	def setUp(self):
		self.factory = RequestFactory()
		p = Person.objects.create(name='wangwang', idnum='111')
		Post.objects.create(name='Django', type=1, comment='test', person=p)
		self.user = User.objects.create_user(username='zdl', email='chuan@163.com', password='123')

	#     self._set_player_session()
	#
	# def _set_player_session(self, player=None):
	#     """
	#     hack the session code to change it to the right one
	#     """
	#     from django.contrib.sessions.models import Session
	#     from django.contrib.sessions.backends.db import SessionStore
	#
	#     session = Session.objects.get(pk=self.client.cookies['sessionid'].value)
	#     today = datetime.today().strftime('%Y%m%d')
	#     newsession = {"date_of_list": today}
	#     session.session_data = SessionStore().encode(newsession)
	#     session.save()

	def test_board_Person_detail_success_status_code(self):
		url = reverse('boards:person_detail', kwargs={'pk': 1})
		request = self.factory.get(url)
		request.user = self.user
		response = person_detail(request, pk=1)
		self.assertEquals(response.status_code, 200)

	def test_board_topics_view_not_found_status_code(self):
		url = reverse('boards:person_detail', kwargs={'pk': 99})
		response = self.client.get(url)
		# print(response.path)
		self.assertEquals(response.status_code, 404)

	def test_board_topics_url_resolves_board_topics_view(self):
		view = resolve('/boards/detail/1/')
		self.assertEquals(view.func, person_detail)
