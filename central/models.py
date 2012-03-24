from django.db import models

MAX_CHARFIELD_LENGTH = 512

class YoutubeVideo(models.Model):


class Event(models.Model):
	datetime = models.DateTimeField()
	name = models.CharField(max_length=MAX_CHARFIELD_LENGTH)

class MediaObject(models.Model):
	datetime = models.DateTimeField()
	name = models.CharField(max_length=MAX_CHARFIELD_LENGTH)
	# plus tags / keywords
	event = models.ForeignKey(Event)
	parent = models.ForeignKey(MediaObject)
	url = models.URLField()
	author = models.SlugField()

class ResponseObject(models.model):
	datetime = models.DateTimeField()
	name = models.CharField(max_length=MAX_CHARFIELD_LENGTH, null=True,
			blank=True)
	text = models.TextField()
	url = models.URLField(blank=True, null=True)
	author = models.SlugField()
