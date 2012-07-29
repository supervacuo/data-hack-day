from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DateTimeAwareJSONEncoder
from django.core import serializers
from django.db.models.query import QuerySet
from django.db.models import Model
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import simplejson
from django.utils.decorators import method_decorator


from central.models import *


def index(request):
	return render(request, 'public/index.html')


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


class ModelAwareJSONEncoder(DateTimeAwareJSONEncoder):
	def default(self, o):
		if isinstance(o, QuerySet):
			return serializers.serialize('python', o)
		if isinstance(o, Model):
			return serializers.serialize('python', [o])[0]
		else:
			return super(ModelAwareJSONEncoder, self).default(o)


class JSONResponseMixin(object):
	def render_to_response(self, context):
		if self.request.is_ajax() or 'ajax' in self.request.GET:
			return self.get_json_response(self.convert_context_to_json(context))
		else:
			return super(JSONResponseMixin, self).render_to_response(context)

	def get_json_response(self, content, **httpresponse_kwargs):
		return HttpResponse(content, content_type='application/json', **httpresponse_kwargs)

	def convert_context_to_json(self, context):
		return simplejson.dumps(context, cls=ModelAwareJSONEncoder)

	def get_paginate_by(self, queryset):
		if self.request.is_ajax() or 'ajax' in self.request.GET:
			return None
		return super(JSONResponseMixin, self).get_paginate_by(queryset)


class LoginRequiredMixin(object):
	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)
