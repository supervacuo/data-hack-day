from datetime import timedelta

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView, DetailView, UpdateView
from django.contrib.auth.views import redirect_to_login

from central.forms import AddEventForm, DateRangeForm
from central.models import Event
from central.views import LoginRequiredMixin


class EventMixin(object):
	def dispatch(self, request, *args, **kwargs):
		self.event = get_object_or_404(Event, id=kwargs['event_id'])
		if not request.user.has_perm('central.view_event', self.event):
			return redirect_to_login(request.build_absolute_uri())

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


class EventUpdateView(EventMixin, UpdateView):
	template_name = 'events/edit.html'
	model = Event

	def get_object(self):
		return self.event

@login_required
def add(request):
	form = AddEventForm(request.POST or None)
	if request.method == 'POST':
		if form.is_valid():
			event = form.save()

			return redirect(event)
	else:
		form = AddEventForm()

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
