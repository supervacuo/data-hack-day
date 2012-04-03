# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'ResponseObject', fields ['text', 'source_type', 'event', 'datetime']
        db.create_unique('central_responseobject', ['text', 'source_type', 'event_id', 'datetime'])

    def backwards(self, orm):
        # Removing unique constraint on 'ResponseObject', fields ['text', 'source_type', 'event', 'datetime']
        db.delete_unique('central_responseobject', ['text', 'source_type', 'event_id', 'datetime'])

    models = {
        'central.event': {
            'Meta': {'object_name': 'Event'},
            'end_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'start_datetime': ('django.db.models.fields.DateTimeField', [], {})
        },
        'central.mediaobject': {
            'Meta': {'ordering': "['event', '-datetime']", 'object_name': 'MediaObject'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['central.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['central.MediaObject']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'central.responseobject': {
            'Meta': {'ordering': "['event', '-datetime']", 'unique_together': "(('event', 'datetime', 'text', 'source_type'),)", 'object_name': 'ResponseObject'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'responses'", 'to': "orm['central.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'media_object': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'responses'", 'null': 'True', 'to': "orm['central.MediaObject']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'}),
            'reply_to': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'replies'", 'null': 'True', 'to': "orm['central.ResponseObject']"}),
            'source_type': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'central.youtubevideo': {
            'Meta': {'ordering': "['event', '-datetime']", 'object_name': 'YouTubeVideo', '_ormbases': ['central.MediaObject']},
            'average_rating': ('django.db.models.fields.FloatField', [], {}),
            'favorited': ('django.db.models.fields.IntegerField', [], {}),
            'mediaobject_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['central.MediaObject']", 'unique': 'True', 'primary_key': 'True'}),
            'ratings': ('django.db.models.fields.IntegerField', [], {}),
            'thumbnail': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'video_id': ('django.db.models.fields.CharField', [], {'max_length': '11'}),
            'views': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['central']