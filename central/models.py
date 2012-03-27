import tagging

from django.db import models
from model_utils.managers import InheritanceManager


MAX_CHARFIELD_LENGTH = 512


class MediaObjectContent(models.Model):
	media_object = models.OneToOneField('MediaObject')

	objects = InheritanceManager()

	def __get_score(self):
		raise NotImplementedError

	score = property(__get_score)


class YoutubeVideo(MediaObjectContent):
	views = models.IntegerField()
	ratings = models.IntegerField()
	average_rating = models.FloatField()
	favorited = models.IntegerField()
	thumbnail = models.URLField()


class Event(models.Model):
	start_datetime = models.DateTimeField(verbose_name=u'Start date/time')
	end_datetime = models.DateTimeField(verbose_name=u'End date/time')
	name = models.CharField(max_length=MAX_CHARFIELD_LENGTH)

	def __unicode__(self):
		return u'%s (%s - %s)' % (self.name, self.start_datetime.strftime('%D %T'),
				self.start_datetime.strftime('%D %T'))

	def get_absolute_url(self):
		return u'/events/%d/' % self.id


class MediaObject(models.Model):
	datetime = models.DateTimeField(verbose_name=u'Date/time')
	name = models.CharField(max_length=MAX_CHARFIELD_LENGTH)
	# plus tags / keywords
	event = models.ForeignKey(Event)
	parent = models.ForeignKey('self', null=True, blank=True)
	url = models.URLField()
	author = models.CharField(max_length=MAX_CHARFIELD_LENGTH)

	def __unicode__(self):
		return self.name

	def get_absolute_url(self):
		return u'/events/%d/media_objects/%d/' % (self.event.id, self.id)

	class Meta:
		ordering = ['event', '-datetime']


class ResponseObject(models.Model):
	datetime = models.DateTimeField()
	name = models.CharField(max_length=MAX_CHARFIELD_LENGTH, null=True,
			blank=True)
	text = models.TextField()
	url = models.URLField(blank=True, null=True)
	author = models.CharField(max_length=MAX_CHARFIELD_LENGTH)
	event = models.ForeignKey(Event)

	class Meta:
		ordering = ['event', '-datetime']

tagging.register(MediaObject)
