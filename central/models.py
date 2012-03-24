from django.db import models
import tagging

MAX_CHARFIELD_LENGTH = 512

class MediaObjectContent(models.Model):
	media_object = models.OneToOneField('MediaObject')

	def __get_score(self):
		return 0

	score = property(__get_score)

class YoutubeVideo(MediaObjectContent):
	views = models.IntegerField()
	ratings = models.IntegerField()
	average_rating = models.FloatField()
	favorited = models.IntegerField()
	thumbnail = models.URLField()

class Event(models.Model):
	start_datetime = models.DateTimeField()
	end_datetime = models.DateTimeField()
	name = models.CharField(max_length=MAX_CHARFIELD_LENGTH)


class MediaObject(models.Model):
	datetime = models.DateTimeField()
	name = models.CharField(max_length=MAX_CHARFIELD_LENGTH)
	# plus tags / keywords
	event = models.ForeignKey(Event)
	parent = models.ForeignKey('self', null=True, blank=True)
	url = models.URLField()
	author = models.CharField(max_length=MAX_CHARFIELD_LENGTH)


class ResponseObject(models.Model):
	datetime = models.DateTimeField()
	name = models.CharField(max_length=MAX_CHARFIELD_LENGTH, null=True,
			blank=True)
	text = models.TextField()
	url = models.URLField(blank=True, null=True)
	author = models.CharField(max_length=MAX_CHARFIELD_LENGTH)

tagging.register(MediaObject)
