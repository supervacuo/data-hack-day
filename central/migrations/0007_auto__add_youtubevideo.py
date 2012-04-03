# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'YouTubeVideo'
        db.create_table('central_youtubevideo', (
            ('mediaobject_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['central.MediaObject'], unique=True, primary_key=True)),
            ('views', self.gf('django.db.models.fields.IntegerField')()),
            ('ratings', self.gf('django.db.models.fields.IntegerField')()),
            ('average_rating', self.gf('django.db.models.fields.FloatField')()),
            ('favorited', self.gf('django.db.models.fields.IntegerField')()),
            ('thumbnail', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal('central', ['YouTubeVideo'])

    def backwards(self, orm):
        # Deleting model 'YouTubeVideo'
        db.delete_table('central_youtubevideo')

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
            'Meta': {'ordering': "['event', '-datetime']", 'object_name': 'ResponseObject'},
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
            'views': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['central']