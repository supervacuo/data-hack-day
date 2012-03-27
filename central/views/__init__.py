from django.shortcuts import render
from django.utils import simplejson
from django.http import HttpResponse

from central.models import *


def index(request):
	return render(request, 'index.html')


def api(request, event_id):
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
