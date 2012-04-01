import csv

from datetime import datetime
from gdata.youtube.service import YouTubeService

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import SuspiciousOperation
from django.utils import simplejson
from django import forms
from django.http import HttpResponse
from django.contrib import messages
from django.forms.models import modelformset_factory

from central.models import Event, MediaObject, YoutubeVideo, MediaObjectContent, ResponseObject
from central.forms import AddMediaObjectForm, AddYoutubeIDForm, AddYoutubeVideoForm, AddMediaObjectCSVForm


def __youtube_id_to_objects(youtube_id, event):
	yt_service = YouTubeService()

	video = yt_service.GetYouTubeVideoEntry(video_id=youtube_id)

	media_object = MediaObject()
	media_object.author = video.author[0].name.text
	media_object.event = event
	media_object.name = video.title.text
	media_object.url = video.GetHtmlLink().href
	media_object.datetime = datetime.strptime(video.published.text, '%Y-%m-%dT%H:%M:%S.%fZ')

	youtube_video = YoutubeVideo()
	youtube_video.views = video.statistics.view_count
	youtube_video.ratings = video.rating.num_raters
	youtube_video.average_rating = video.rating.average
	youtube_video.favorited = video.statistics.favorite_count
	youtube_video.thumbnail = video.media.thumbnail[0].url

	comment_feed = yt_service.GetYouTubeVideoCommentFeed(video_id=youtube_id)

	comment_list = []

	for comment in comment_feed.entry:
		response_object = ResponseObject()
		response_object.title = comment.title.text
		response_object.text = comment.content.text
		response_object.datetime = datetime.strptime(comment.published.text, '%Y-%m-%dT%H:%M:%S.%fZ')
		response_object.author = comment.author[0].name.text
		response_object.event = event
		response_object.media_object = media_object
		response_object.source_type = 'yt'

		comment_list.append(response_object)

	return media_object, youtube_video, comment_list


def list(request, event_id):
	event = get_object_or_404(Event, id=event_id)

	media_objects = MediaObject.objects.filter(event=event)

	if request.is_ajax() or 'ajax' in request.GET:
		media_objects_list = []

		for media_object in media_objects:
			media_objects_list.append({
				'datetime': media_object.datetime.strftime('%Y-%m-%d %H:%M:%S'),
				'link': media_object.url,
				'type': media_object.type_name,
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
	return render(request, 'media_object/list.html', data)


def detail(request, event_id, media_object_id):
	media_object = get_object_or_404(MediaObject, id=media_object_id)

	if media_object.event.id != int(event_id):
		raise SuspiciousOperation

	try:
		media_object_content = MediaObjectContent.objects.select_subclasses().get(media_object__id=media_object.id)
		media_object_content_type = media_object_content.__class__.__name__
	except MediaObjectContent.DoesNotExist:
		media_object_content = None
		media_object_content_type = None

	data = {
		'event': media_object.event,
		'media_object': media_object,
		'media_object_content': media_object_content,
		'media_object_content_type': media_object_content_type,
	}

	return render(request, 'media_object/detail.html', data)


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

	return render(request, 'media_object/delete.html', data)


@login_required
def add(request, event_id):
	event = get_object_or_404(Event, id=event_id)

	form = AddMediaObjectForm(request.POST or None)

	if form.is_valid():
		media_object = form.save()

		return redirect(media_object)

	data = {
		'event': event,
		'form': form,
	}

	return render(request, 'media_object/add.html', data)


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

	return render(request, 'media_object/add_csv.html', data)


@login_required
def add_youtube_by_id(request, event_id):
	event = get_object_or_404(Event, id=event_id)

	form = AddYoutubeIDForm()

	data = {
		'event': event,
		'form': form,
	}

	return render(request, 'management/add_youtube_by_id.html', data)


@login_required
def add_youtube_in_bulk(request, event_id):
	raise NotImplementedError


def add_youtube(request, event_id):
	event = get_object_or_404(Event, id=event_id)
	video_id = None

	if request.method == 'POST':
		media_object_form = AddMediaObjectForm(request.POST, instance=MediaObject())
		youtube_form = AddYoutubeVideoForm(request.POST, instance=YoutubeVideo())
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

		if media_object_form.is_valid() and youtube_form.is_valid() and youtube_comments_formset.is_valid():
			media_object = media_object_form.save()

			youtube_object = youtube_form.save(commit=False)
			youtube_object.media_object = media_object
			youtube_object.save()
			youtube_comments = youtube_comments_formset.save(commit=False)

			for youtube_comment in youtube_comments:
				youtube_comment.event = event
				youtube_comment.media_object = media_object
				youtube_comment.save()
			messages.success(request, 'Added new YouTube video "%s"' % media_object.name)

			return redirect(media_object)
	else:
		id_form = AddYoutubeIDForm(request.GET or None)

		media_object = None
		youtube_video = None

		if id_form.is_valid():
			video_id = id_form.cleaned_data['youtube_id']

			media_object, youtube_video, comments = __youtube_id_to_objects(video_id, event)

		media_object_form = AddMediaObjectForm(instance=media_object)
		youtube_form = AddYoutubeVideoForm(instance=youtube_video)

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
		'media_object_form': media_object_form,
		'youtube_form': youtube_form,
		'youtube_comments_formset': youtube_comments_formset,
		'video_id': video_id,
	}

	return render(request, 'management/add_youtube.html', data)
