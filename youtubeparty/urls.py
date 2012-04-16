from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

from central.views.events import * 
from central.views.response_objects import * 
from central.views.media_objects import * 

urlpatterns = patterns('',
	url(r'^$', 'central.views.index'),

	# Display Events
	url(r'^events/$', EventListView.as_view(), name='event_list'),
	url(r'^events/(?P<event_id>\d*)/$', EventDetailView.as_view(), name='event_detail'),
	url(r'^events/(?P<event_id>\d*)/timeline/$', 'central.views.events.timeline'),
	# Modify Events
	url(r'^events/(?P<event_id>\d*)/edit/$', EventUpdateView.as_view(), name='event_update'),
	# Add Events
	url(r'^events/add/$', 'central.views.events.add'),
	
	# Display MediaObjects
	url(r'^events/(?P<event_id>\d*)/media_objects/$', MediaObjectListView.as_view(), name='media_list'),
	url(r'^events/(?P<event_id>\d*)/media_objects/(?P<media_object_id>\d*)/$', 'central.views.media_objects.detail'),
	# Modify MediaObjects
	url(r'^events/(?P<event_id>\d*)/media_objects/(?P<media_object_id>\d*)/edit/$', 'central.views.media_objects.edit'),
	url(r'^events/(?P<event_id>\d*)/media_objects/(?P<media_object_id>\d*)/delete/$', 'central.views.media_objects.delete'),
	# Add MediaObjects
	url(r'^events/(?P<event_id>\d*)/media_objects/add/$', 'central.views.media_objects.add'),
	url(r'^events/(?P<event_id>\d*)/media_objects/add_csv/$', 'central.views.media_objects.add_csv'),
	url(r'^events/(?P<event_id>\d*)/media_objects/add_youtube/$', 'central.views.media_objects.add_youtube'),
	url(r'^events/(?P<event_id>\d*)/media_objects/add_youtube_by_id/$', 'central.views.media_objects.add_youtube_by_id'),
	url(r'^events/(?P<event_id>\d*)/media_objects/add_youtube_in_bulk/$', 'central.views.media_objects.add_youtube_in_bulk'),

	# Display ResponseObjects
	url(r'^events/(?P<event_id>\d*)/response_objects/$', ResponseObjectListView.as_view(), name='response_list_by_event'),
	url(r'^events/(?P<event_id>\d*)/media_objects/(?P<media_object_id>\d*)/response_objects/$', ResponseObjectListView.as_view(), name='response_list_by_media'),
	url(r'^events/(?P<event_id>\d*)/response_objects/(?P<response_object_id>\d*)/$', ResponseObjectDetailView.as_view(), name='response_detail'),
	# Modify ResponseObjects
	url(r'^events/(?P<event_id>\d*)/response_objects/(?P<response_object_id>\d*)/edit/$', ResponseObjectUpdateView.as_view(), name='response_edit'),
	url(r'^events/(?P<event_id>\d*)/response_objects/(?P<response_object_id>\d*)/delete/$', ResponseObjectDeleteView.as_view(), name='response_delete'),
	# Add ResponseObjects
	url(r'^events/(?P<event_id>\d*)/response_objects/add/$', ResponseObjectCreateView.as_view(), name='response_add'),
	url(r'^events/(?P<event_id>\d*)/media_objects/(?P<media_object_id>\d*)/response_objects/add/$', ResponseObjectCreateView.as_view(), name='response_add_by_media_object'),

	url(r'^accounts/login/$', 'django.contrib.auth.views.login', name='login'),

	# Examples:
	# url(r'^$', 'youtubeparty.views.home', name='home'),
	# url(r'^youtubeparty/', include('youtubeparty.foo.urls')),

	# Uncomment the admin/doc line below to enable admin documentation:
	# url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

	# Uncomment the next line to enable the admin:
	url(r'^admin/', include(admin.site.urls)),
)
