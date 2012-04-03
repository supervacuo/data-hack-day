from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView

from central.models import Event, ResponseObject
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


def edit(request, event_id, response_object_id, media_object_id=None):
	raise NotImplementedError


def delete(request, event_id, response_object_id, media_object_id=None):
	raise NotImplementedError


def add(request, event_id, media_object_id=None):
	event = get_object_or_404(Event, id=event_id)

	raise NotImplementedError
