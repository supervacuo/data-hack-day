from central.models import *

from django.shortcuts import render_to_response, get_object_or_404
from django.utils import simplejson
from django.http import HttpResponse

from datetime import datetime

def timeline(request):
	event = Event.objects.all()[0]


	data = {
			'event': event,
			}

	return render_to_response('timeline.html', data)

def events(request, event_id):
	event = get_object_or_404(Event, id=event_id)

	# return JSON serialization of events with start events
	mobj_list = []

	for mobj in event.mediaobject_set.all():
		data = {
			'start': mobj.datetime.isoformat(),
			'title': mobj.name
			}
		mobj_list.append(data)
	
	json_obj = {
			"events": mobj_list
			}

	return HttpResponse(simplejson.dumps(json_obj), content_type='application/json; charset=utf-8')
