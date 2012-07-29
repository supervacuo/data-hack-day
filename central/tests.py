from django.core.urlresolvers import reverse
from django.test import TestCase

from central.models import *


class PublicTest(TestCase):
	def test_public_pages(self):
		"""
		Ensure all public pages can be loaded without errors
		"""
		for page in ['/', 'contributing', 'roadmap']:
			response = self.client.get(page)
			self.assertEqual(response.status_code, 200)
			self.assertTemplateUsed(response, 'public/index.html')

	def test_login_redirect(self):
		"""
		Test that loading user-specific pages redirects to login
		"""
		response = self.client.get(reverse('event_list'))
		# TODO It would be nicer to do clever things with QueryDict here, but it
		# seems contrib.auth actually doesn't urlencode the 'next' parameter. Hmm.
		self.assertRedirects(response, reverse('login') + '?next=%s' % reverse('event_list'))

		# Although this event doesn't (yet) exist, the login redirect should happen
		# before checking whether it does
		media_list_url = reverse('media_list', kwargs={'event_id': 1})
		response = self.client.get(media_list_url)
		self.assertRedirects(response, reverse('login') + '?next=%s' % media_list_url)

		media_detail_url = reverse('media_detail', kwargs={
			'event_id': 1,
			'media_object_id': 1})
		response = self.client.get(media_detail_url)
		self.assertRedirects(response, reverse('login') + '?next=%s' % media_detail_url)

		response_list_url = reverse('response_list_by_event', kwargs={'event_id': 1})
		response = self.client.get(response_list_url)
		self.assertRedirects(response, reverse('login') + '?next=%s' % response_list_url)

		response_list_url = reverse('response_list_by_media', kwargs={
			'event_id': 1,
			'media_object_id': 1})
		response = self.client.get(response_list_url)
		self.assertRedirects(response, reverse('login') + '?next=%s' % response_list_url)

		response_detail_url = reverse('response_detail', kwargs={
			'event_id': 1,
			'response_object_id': 1})
		response = self.client.get(response_detail_url)
		self.assertRedirects(response, reverse('login') + '?next=%s' % response_detail_url)

class EventTest(TestCase):
	fixtures = ('test',)

	def test_add_event(self):
		self.client.login(username='wei', password='test')

		event_add_url = reverse('event_add')

		response = self.client.get(event_add_url)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'events/add.html')

		# Send blank form data using POST
		response = self.client.post(event_add_url, {
			'name': ''
		})
		# Should re-show the form...
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'events/add.html')
		# ... with some errors
		self.assertFormError(response, 'form', 'name', 'This field is required.')
		self.assertFormError(response, 'form', 'start_datetime', 'This field is required.')
		self.assertFormError(response, 'form', 'end_datetime', 'This field is required.')

		# Send invalid form data using POST
		response = self.client.post(event_add_url, {
			'name': 'Test event',
			'start_datetime_0': 'invalid',
			'start_datetime_1': 'invalid',
			'end_datetime_0': 'invalid',
			'end_datetime_1': 'invalid',
		})
		# Should re-show the form...
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'events/add.html')
		# ... with some errors
		self.assertFormError(response, 'form', 'start_datetime', 'Enter a valid date/time.')
		self.assertFormError(response, 'form', 'end_datetime', 'Enter a valid date/time.')

		# Send valid form data using POST
		response = self.client.post(event_add_url, {
			'name': 'Test event',
			'start_datetime_0': '2011-11-15',
			'start_datetime_1': '00:00',
			'end_datetime_0': '2011-11-16',
			'end_datetime_1': '00:00',
		})
		event = Event.objects.order_by('-id')[0]
		self.assertEqual(event.name, 'Test event')
		self.assertRedirects(response, reverse('event_detail', kwargs={
			'event_id': event.id
		}))
