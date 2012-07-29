from datetime import timedelta

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, UpdateView

from guardian.shortcuts import assign
from guardian.shortcuts import get_objects_for_user

from central.forms import EventForm, DateRangeForm
from central.models import Event
from central.views import LoginRequiredMixin


class EventMixin(object):
	def dispatch(self, request, *args, **kwargs):
		self.event = get_object_or_404(Event, id=kwargs['event_id'])
		if not request.user.has_perm('central.view_event', self.event):
			messages.error(request, 'You don\'t have access to that event')
			return redirect('event_list')

		return super(EventMixin, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(EventMixin, self).get_context_data(**kwargs)
		context['event'] = self.event

		return context


class EventDetailView(LoginRequiredMixin, EventMixin, DetailView):
	context_object_name = 'event'
	template_name = 'events/detail.html'
	model = Event

	def get_object(self):
		return self.event


class EventListView(LoginRequiredMixin, ListView):
	context_object_name = 'events'
	template_name = 'events/list.html'
	model = Event

	def get_queryset(self):
		return get_objects_for_user(self.request.user, 'central.view_event')


class EventUpdateView(EventMixin, UpdateView):
	template_name = 'events/edit.html'
	model = Event
	form_class = EventForm

	def get_object(self):
		return self.event


@login_required
def add(request):
	form = EventForm(request.POST or None)
	if request.method == 'POST':
		if form.is_valid():
			event = form.save()
			assign('view_event', request.user, event)
			return redirect(event)
	else:
		form = EventForm()

	data = {
		'form': form,
	}

	return render(request, 'events/add.html', data)


def timeline(request, event_id):
	event = get_object_or_404(Event, id=event_id)

	date_range_form = DateRangeForm(request.GET)

	if date_range_form.is_valid():
		start = date_range_form.cleaned_data['start']
		end = date_range_form.cleaned_data['end']
	else:
		start = event.start_datetime
		end = start + timedelta(hours=2)

		date_range_form = DateRangeForm(initial={
			'start': start,
			'end': end,
		})

	data = {
		'event': event,
		'date_range_form': date_range_form,
		'start': start,
		'end': end,
	}

	return render(request, 'events/timeline.html', data)
