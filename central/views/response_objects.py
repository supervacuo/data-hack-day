from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse

from central.models import ResponseObject
from central.views.events import EventMixin
from central.views.media_objects import MediaObjectMixin


class ResponseObjectMixin(object):
	def dispatch(self, request, *args, **kwargs):
		self.response_object = get_object_or_404(ResponseObject, id=kwargs['response_object_id'])

		return super(ResponseObjectMixin, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(ResponseObjectMixin, self).get_context_data(**kwargs)
		context['response_object'] = self.response_object

		return context


class ResponseObjectListView(MediaObjectMixin, EventMixin, ListView):
	context_object_name = 'response_objects'
	template_name = 'response_objects/list.html'

	def get_queryset(self):
		try:
			return self.media_object.responses.all()
		except AttributeError:
			return self.event.responses.all()


class ResponseObjectDetailView(ResponseObjectMixin, MediaObjectMixin, EventMixin, DetailView):
	context_object_name = 'response_object'
	template_name = 'response_objects/detail.html'

	def get_object(self):
		return self.response_object


class ResponseObjectCreateView(MediaObjectMixin, EventMixin, CreateView):
	model = ResponseObject
	template_name = 'response_objects/add.html'

	def get_form_kwargs(self):
		kwargs = super(ResponseObjectCreateView, self).get_form_kwargs()
		kwargs.update({'instance': ResponseObject(event=self.event, media_object=self.media_object)})
		return kwargs

	def dispatch(self, request, *args, **kwargs):
		# FIXME this should not be a "global" permission
		if not request.user.has_perm('central.create_responseobject'):
			raise PermissionDenied

		return super(ResponseObjectCreateView, self).dispatch(request, *args, **kwargs)


class ResponseObjectUpdateView(ResponseObjectMixin, MediaObjectMixin, EventMixin, UpdateView):
	model = ResponseObject
	template_name = 'response_objects/edit.html'

	def get_object(self):
		if not self.request.user.has_perm('central.change_responseobject', self.response_object):
			raise PermissionDenied
		return self.response_object


class ResponseObjectDeleteView(ResponseObjectMixin, MediaObjectMixin, EventMixin, DeleteView):
	model = ResponseObject
	template_name = 'response_objects/delete.html'

	def get_object(self):
		return self.response_object

	def get_success_url(self):
		if self.media_object:
			return reverse('response_list_by_media', kwargs={
				'event_id': self.event.id,
				'media_object_id': self.media_object.id,
			})
		else:
			return reverse('response_list_by_event', kwargs={
				'event_id': self.event.id,
			})
