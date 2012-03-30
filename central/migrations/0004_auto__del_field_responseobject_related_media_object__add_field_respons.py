# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'ResponseObject.related_media_object'
        db.delete_column('central_responseobject', 'related_media_object_id')

        # Adding field 'ResponseObject.media_object'
        db.add_column('central_responseobject', 'media_object',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['central.MediaObject'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'ResponseObject.source_type'
        db.add_column('central_responseobject', 'source_type',
                      self.gf('django.db.models.fields.CharField')(default='YT', max_length=512),
                      keep_default=False)

    def backwards(self, orm):
        # Adding field 'ResponseObject.related_media_object'
        db.add_column('central_responseobject', 'related_media_object',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['central.MediaObject'], null=True, blank=True),
                      keep_default=False)

        # Deleting field 'ResponseObject.media_object'
        db.delete_column('central_responseobject', 'media_object_id')

        # Deleting field 'ResponseObject.source_type'
        db.delete_column('central_responseobject', 'source_type')

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
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['central.MediaObject']", 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'central.mediaobjectcontent': {
            'Meta': {'object_name': 'MediaObjectContent'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'media_object': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['central.MediaObject']", 'unique': 'True'})
        },
        'central.responseobject': {
            'Meta': {'ordering': "['event', '-datetime']", 'object_name': 'ResponseObject'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['central.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'media_object': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['central.MediaObject']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'reply_to': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['central.ResponseObject']", 'null': 'True', 'blank': 'True'}),
            'source_type': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'central.youtubevideo': {
            'Meta': {'object_name': 'YoutubeVideo', '_ormbases': ['central.MediaObjectContent']},
            'average_rating': ('django.db.models.fields.FloatField', [], {}),
            'favorited': ('django.db.models.fields.IntegerField', [], {}),
            'mediaobjectcontent_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['central.MediaObjectContent']", 'unique': 'True', 'primary_key': 'True'}),
            'ratings': ('django.db.models.fields.IntegerField', [], {}),
            'thumbnail': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'views': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['central']