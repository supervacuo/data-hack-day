import csv

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import SuspiciousOperation
from django.utils import simplejson
from django import forms
from django.http import HttpResponse, Http404
from django.contrib import messages
from django.forms.models import modelformset_factory

from central.models import Event, MediaObject, YouTubeVideo, ResponseObject
from central.forms import AddMediaObjectForm, AddYouTubeIDForm, AddYouTubeVideoForm, AddMediaObjectCSVForm


class MediaObjectMixin(object):
	def dispatch(self, request, *args, **kwargs):
		try:
			self.media_object = get_object_or_404(MediaObject, id=kwargs['media_object_id'])
		except KeyError:
			# User has requested a view that *might* accept media_object_id, but one
			# has not been provided -- this means we don't need to check permissions
			# (as they'll be handled by other components of this view)
			self.media_object = None

		return super(MediaObjectMixin, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(MediaObjectMixin, self).get_context_data(**kwargs)
		context['media_object'] = self.media_object

		return context


def list(request, event_id):
	event = get_object_or_404(Event, id=event_id)

	media_objects = MediaObject.objects.filter(event=event).select_subclasses()

	if request.is_ajax() or 'ajax' in request.GET:
		media_objects_list = []

		for media_object in media_objects:
			media_objects_list.append({
				'datetime': media_object.datetime.strftime('%Y-%m-%d %H:%M:%S'),
				'link': media_object.url,
				'type': media_object._meta.verbose_name,
				'responses': [{
						'datetime': r.datetime.isoformat(),
						'author': r.author,
					} for r in media_object.responses.all()],
				'title': media_object.name})

		json_obj = {
			"events": media_objects_list
		}

		return HttpResponse(simplejson.dumps(json_obj), content_type='application/json; charset=utf-8')

	data = {
		'event': event,
		'media_objects': media_objects
	}
	return render(request, 'media_objects/list.html', data)


def detail(request, event_id, media_object_id):
	try:
		media_object = MediaObject.objects.get_subclass(id=media_object_id)
	except MediaObject.DoesNotExist():
		raise Http404

	if media_object.event.id != int(event_id):
		raise SuspiciousOperation

	data = {
		'event': media_object.event,
		'media_object': media_object,
	}

	return render(request, 'media_objects/detail.html', data)


@login_required
def edit(request, event_id, media_object_id):
	raise NotImplementedError


@login_required
def delete(request, event_id, media_object_id):
	media_object = get_object_or_404(MediaObject, id=media_object_id)
	event = media_object.event

	if request.method == 'POST' or request.is_ajax or 'ajax' in request.GET:
		media_object.delete()
		messages.success(request, 'Deleted media object "%s"' % media_object.name)
		return redirect(list, event_id=event.id)

	data = {
		'event': event,
		'media_object': media_object,
	}

	return render(request, 'media_objects/delete.html', data)


@login_required
def add(request, event_id):
	event = get_object_or_404(Event, id=event_id)

	form = AddMediaObjectForm(request.POST or None)

	if form.is_valid():
		media_object = form.save(commit=False)
		media_object.event = event
		media_object.save()

		return redirect(media_object)

	data = {
		'event': event,
		'form': form,
	}

	return render(request, 'media_objects/add.html', data)


@login_required
def add_csv(request, event_id):
	event = get_object_or_404(Event, id=event_id)

	if request.method == 'POST':
		form = AddMediaObjectCSVForm(request. POST, request.FILES)

		if form.is_valid():
			dataReader = csv.reader(request.FILES['csv_file'], delimiter=';')

			media_objects = []

			for row in dataReader:
				media_object = MediaObject()
				media_object.datetime = row[0]
				media_object.name = row[1]
				media_object.url = row[2]
				media_object.author = row[3]
				media_object.event = event
				media_object.save()

				media_objects.append(media_object)

			messages.success(request, 'Imported %d new media objects' % len(media_objects))
			return redirect(list, event_id=event.id)
	else:
		form = AddMediaObjectCSVForm()

	data = {
		'event': event,
		'form': form,
	}

	return render(request, 'media_objects/add_csv.html', data)


@login_required
def add_youtube_by_id(request, event_id):
	event = get_object_or_404(Event, id=event_id)

	form = AddYouTubeIDForm()

	data = {
		'event': event,
		'form': form,
	}

	return render(request, 'media_objects/add_youtube_by_id.html', data)


@login_required
def add_youtube_in_bulk(request, event_id):
	raise NotImplementedError


def add_youtube(request, event_id):
	event = get_object_or_404(Event, id=event_id)
	video_id = None

	if request.method == 'POST':
		youtube_form = AddYouTubeVideoForm(request.POST, instance=YouTubeVideo())
		ResponseObjectFormSet = modelformset_factory(
			ResponseObject,
			exclude=('id', 'event', 'media_object', 'reply_to'),
			# Shouldn't be necessary in this coder's humble opinion
			extra=len([k for k in request.POST.keys() if 'response_object' in k]),
			formfield_callback=lambda f: f.formfield(widget=forms.HiddenInput))

		youtube_comments_formset = ResponseObjectFormSet(
			request.POST,
			queryset=ResponseObject.objects.none(),
			prefix='response_object')

		if youtube_form.is_valid() and youtube_comments_formset.is_valid():
			youtube_object = youtube_form.save(commit=False)
			youtube_object.event = event
			youtube_object.save()
			youtube_comments = youtube_comments_formset.save(commit=False)

			for youtube_comment in youtube_comments:
				youtube_comment.event = event
				youtube_comment.media_object = youtube_object
				youtube_comment.save()
			messages.success(request, 'Added new YouTube video "%s"' % youtube_object.name)

			return redirect(youtube_object)
	else:
		id_form = AddYouTubeIDForm(request.GET or None)

		youtube_video = None

		if id_form.is_valid():
			video_id = id_form.cleaned_data['youtube_id']

			youtube_video = YouTubeVideo.objects.create_from_id(video_id)
			youtube_video.event = event
			comments = youtube_video.fetch_comments()

		youtube_form = AddYouTubeVideoForm(instance=youtube_video)

		ResponseObjectFormSet = modelformset_factory(
			ResponseObject,
			exclude=('id', 'event', 'media_object', 'reply_to'),
			# Shouldn't be necessary in this coder's humble opinion
			extra=len(comments),
			formfield_callback=lambda f: f.formfield(widget=forms.HiddenInput))

		youtube_comments_formset = ResponseObjectFormSet(
			initial=[c.__dict__ for c in comments],
			queryset=ResponseObject.objects.none(),
			prefix='response_object')

	data = {
		'event': event,
		'youtube_form': youtube_form,
		'youtube_comments_formset': youtube_comments_formset,
		'video_id': video_id,
	}

	return render(request, 'media_objects/add_youtube.html', data)
