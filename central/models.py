import tagging
import otter
from datetime import datetime

from django.db import models
from model_utils.managers import InheritanceManager

from youtubeparty import settings

MAX_CHARFIELD_LENGTH = 512


class ResponseObjectManager(models.Manager):
	def tweets_for_youtube(self, youtube_id):
		try:
			youtube_video = YoutubeVideo.objects.get(media_object__url__contains=youtube_id)
		except YoutubeVideo.DoesNotExist:
			# Should create the YoutubeVideo from ID here
			pass

		r = otter.Resource('trackbacks',
			api_key=settings.OTTER_API_KEY,
			url='http://www.youtube.com/watch?v=%s' % youtube_id)

		r()

		response_objects = []

		for tweet in r.response.list:
			response_object = ResponseObject()
			response_object.datetime = datetime.fromtimestamp(tweet.date)
			response_object.text = tweet.content
			response_object.url = tweet.permalink_url
			response_object.author = tweet.author.nick
			response_object.source_type = 'tw'
			response_object.media_object = youtube_video.media_object
			response_object.event = youtube_video.media_object.event

			response_objects.append(response_object)

		return response_objects



	def __get_score(self):
		raise NotImplementedError

	score = property(__get_score)


class Event(models.Model):
	start_datetime = models.DateTimeField(verbose_name=u'Start date/time')
	end_datetime = models.DateTimeField(verbose_name=u'End date/time')
	name = models.CharField(max_length=MAX_CHARFIELD_LENGTH)

	def __unicode__(self):
		return u'%s (%s - %s)' % (self.name, self.start_datetime.strftime('%D %T'),
				self.start_datetime.strftime('%D %T'))

	@models.permalink
	def get_absolute_url(self):
		return ('central.views.events.detail', (), {'event_id': self.id})

	class Meta:
		permissions = (
			('view_event', 'Can view events'),
		)


class MediaObject(models.Model):
	datetime = models.DateTimeField(verbose_name=u'Date/time')
	name = models.CharField(max_length=MAX_CHARFIELD_LENGTH)
	# plus tags / keywords
	event = models.ForeignKey(Event)
	parent = models.ForeignKey('self', null=True, blank=True, related_name='children')
	url = models.URLField()
	author = models.CharField(max_length=MAX_CHARFIELD_LENGTH)

	objects = InheritanceManager()

	def __unicode__(self):
		return self.name

	@models.permalink
	def get_absolute_url(self):
		return ('central.views.media_objects.detail', (), {
			'event_id': self.event.id,
			'media_object_id': self.id,
		})

	class Meta:
		ordering = ['event', '-datetime']


class YouTubeVideo(MediaObject):
	views = models.IntegerField()
	ratings = models.IntegerField()
	average_rating = models.FloatField()
	favorited = models.IntegerField()
	thumbnail = models.URLField()
	video_id = models.CharField(max_length=11)

	class Meta:
		verbose_name = 'youtube video'


class ResponseObject(models.Model):
	SOURCES = (
		('yt', 'YouTube'),
		('tw', 'Twitter')
	)

	datetime = models.DateTimeField()
	name = models.CharField(max_length=MAX_CHARFIELD_LENGTH, blank=True)
	text = models.TextField(blank=True)
	url = models.URLField(blank=True, null=True)
	author = models.CharField(max_length=MAX_CHARFIELD_LENGTH, blank=True)
	event = models.ForeignKey(Event, related_name='responses')
	media_object = models.ForeignKey(MediaObject, null=True, blank=True, related_name='responses')
	reply_to = models.ForeignKey('self', null=True, blank=True, related_name='replies')
	source_type = models.CharField(max_length=MAX_CHARFIELD_LENGTH, choices=SOURCES)
	objects = ResponseObjectManager()

	def __unicode__(self):
		return u'%s: %s by %s' % (self.source_type, self.datetime, self.author or 'unknown')

	@models.permalink
	def get_absolute_url(self):
		return ('response_detail', (), {
			'event_id': self.event.id,
			'response_object_id': self.id,
		})

	class Meta:
		ordering = ['event', '-datetime']

tagging.register(MediaObject)
