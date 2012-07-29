from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse

from central.forms import DateRangeForm
from central.models import ResponseObject
from central.views import JSONResponseMixin, LoginRequiredMixin
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


class ResponseObjectListView(LoginRequiredMixin, JSONResponseMixin, MediaObjectMixin, EventMixin, ListView):
	context_object_name = 'response_objects'
	template_name = 'response_objects/list.html'
	paginate_by = 20

	def get_queryset(self):
		try:
			response_objects = self.media_object.responses.all()
		except AttributeError:
			response_objects = self.event.responses.all()

		date_range_form = DateRangeForm(self.request.GET)

		if date_range_form.is_valid():
			response_objects = response_objects.filter(
				datetime__gte=date_range_form.cleaned_data['start']
			).filter(
				datetime__lte=date_range_form.cleaned_data['end']
			)

		if int(self.request.GET.get('replies', 1)) == 0:
			response_objects = response_objects.filter(reply_to=None).filter(media_object=None)

		return response_objects


class ResponseObjectDetailView(LoginRequiredMixin, ResponseObjectMixin, MediaObjectMixin, EventMixin, DetailView):
	context_object_name = 'response_object'
	template_name = 'response_objects/detail.html'

	def get_object(self):
		return self.response_object


class ResponseObjectCreateView(LoginRequiredMixin, MediaObjectMixin, EventMixin, CreateView):
	model = ResponseObject
	template_name = 'response_objects/add.html'

	def get_initial(self):
		initial = super(ResponseObjectCreateView,self).get_initial()
		initial['event'] = self.event
		initial['media_object'] = self.media_object
		return initial

	def dispatch(self, request, *args, **kwargs):
		# FIXME this should not be a "global" permission
		if not request.user.has_perm('central.create_responseobject'):
			raise PermissionDenied

		return super(ResponseObjectCreateView, self).dispatch(request, *args, **kwargs)


class ResponseObjectUpdateView(LoginRequiredMixin, ResponseObjectMixin, MediaObjectMixin, EventMixin, UpdateView):
	model = ResponseObject
	template_name = 'response_objects/edit.html'

	def get_object(self):
		if not self.request.user.has_perm('central.change_responseobject', self.response_object):
			raise PermissionDenied
		return self.response_object


class ResponseObjectDeleteView(LoginRequiredMixin, ResponseObjectMixin, MediaObjectMixin, EventMixin, DeleteView):
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
