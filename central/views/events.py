from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from central.forms import AddEventForm
from central.models import Event


class EventMixin(object):
	def dispatch(self, *args, **kwargs):
		self.event = get_object_or_404(Event, id=kwargs['event_id'])

		return super(EventMixin, self).dispatch(*args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(EventMixin, self).get_context_data(**kwargs)
		context['event'] = self.event

		return context


def detail(request, event_id):
	event = get_object_or_404(Event, id=event_id)

	data = {
		'event': event
	}

	return render(request, 'event/detail.html', data)


def list(request):
	events = Event.objects.all()

	data = {
		'events': events,
	}

	return render(request, 'event/list.html', data)


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

	return render(request, 'event/add.html', data)


def timeline(request, event_id):
	event = get_object_or_404(Event, id=event_id)

	data = {
		'event': event,
	}

	return render(request, 'event/timeline.html', data)
