import tagging
import otter
from datetime import datetime
from gdata.youtube.service import YouTubeService

from django.db import models
from model_utils.managers import InheritanceManager

from youtubeparty import settings

MAX_CHARFIELD_LENGTH = 512


class Event(models.Model):
	start_datetime = models.DateTimeField(verbose_name=u'Start date/time')
	end_datetime = models.DateTimeField(verbose_name=u'End date/time')
	name = models.CharField(max_length=MAX_CHARFIELD_LENGTH)

	def __unicode__(self):
		return u'%s (%s - %s)' % (self.name, self.start_datetime.strftime('%D %T'),
				self.start_datetime.strftime('%D %T'))

	@models.permalink
	def get_absolute_url(self):
		return ('event_detail', (), {'event_id': self.id})

	class Meta:
		permissions = (
			('view_event', 'Can view events'),
		)


class MediaObject(models.Model):
	datetime = models.DateTimeField(verbose_name=u'Date/time')
	name = models.CharField(max_length=MAX_CHARFIELD_LENGTH)
	# plus tags / keywords
	event = models.ForeignKey(Event, related_name='media_objects')
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


class YouTubeVideoManager(models.Manager):
	def create_from_id(self, video_id):
		yt_service = YouTubeService()

		video = yt_service.GetYouTubeVideoEntry(video_id=video_id)

		youtube_video = YouTubeVideo()
		youtube_video.author = video.author[0].name.text
		youtube_video.name = video.title.text
		youtube_video.url = video.GetHtmlLink().href
		youtube_video.datetime = datetime.strptime(video.published.text, '%Y-%m-%dT%H:%M:%S.%fZ')
		youtube_video.views = video.statistics.view_count
		youtube_video.ratings = video.rating.num_raters
		youtube_video.average_rating = video.rating.average
		youtube_video.favorited = video.statistics.favorite_count
		youtube_video.thumbnail = video.media.thumbnail[0].url
		youtube_video.video_id = video_id

		return youtube_video


class YouTubeVideo(MediaObject):
	views = models.IntegerField()
	ratings = models.IntegerField()
	average_rating = models.FloatField()
	favorited = models.IntegerField()
	thumbnail = models.URLField()
	video_id = models.CharField(max_length=11)

	objects = YouTubeVideoManager()

	def fetch_comments(self):
		yt_service = YouTubeService()

		comment_feed = yt_service.GetYouTubeVideoCommentFeed(video_id=self.video_id)

		comment_list = []

		for comment in comment_feed.entry:
			response_object = ResponseObject()
			response_object.name = comment.title.text
			response_object.text = comment.content.text
			response_object.datetime = datetime.strptime(comment.published.text, '%Y-%m-%dT%H:%M:%S.%fZ')
			response_object.author = comment.author[0].name.text
			response_object.event = self.event
			response_object.media_object = self
			response_object.source_type = 'yt'

			comment_list.append(response_object)
		return comment_list

	def fetch_tweets(self):
		tweets = ResponseObject.objects.tweets_from_url('http://www.youtube.com/watch?v=%s' % self.video_id)

		tweet_list = []

		for tweet in tweets:
			tweet.media_object = self
			tweet.event = self.event
			tweet_list.append(tweet)

		return tweet_list

	class Meta:
		verbose_name = 'youtube video'


class ResponseObjectManager(models.Manager):
	def tweets_from_url(self, url):
		r = otter.Resource('trackbacks', api_key=settings.OTTER_API_KEY, url=url)

		r()

		response_objects = []

		for tweet in r.response.list:
			response_object = ResponseObject()
			response_object.datetime = datetime.fromtimestamp(tweet.date)
			response_object.text = tweet.content
			try:
				response_object.url = tweet.permalink_url
			except AttributeError:
				pass
			response_object.author = tweet.author.nick
			response_object.source_type = 'tw'

			response_objects.append(response_object)

		return response_objects


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
		# Hopefully enough here to prevent major duplicates. Obviously the resulting
		# exception should be caught by views.
		unique_together = (('event', 'datetime', 'text', 'source_type'),)

tagging.register(MediaObject)
