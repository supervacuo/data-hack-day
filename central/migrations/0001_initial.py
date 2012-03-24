# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MediaObjectContent'
        db.create_table('central_mediaobjectcontent', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('media_object', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['central.MediaObject'], unique=True)),
        ))
        db.send_create_signal('central', ['MediaObjectContent'])

        # Adding model 'YoutubeVideo'
        db.create_table('central_youtubevideo', (
            ('mediaobjectcontent_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['central.MediaObjectContent'], unique=True, primary_key=True)),
            ('views', self.gf('django.db.models.fields.IntegerField')()),
            ('ratings', self.gf('django.db.models.fields.IntegerField')()),
            ('average_rating', self.gf('django.db.models.fields.FloatField')()),
            ('favorited', self.gf('django.db.models.fields.IntegerField')()),
            ('thumbnail', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal('central', ['YoutubeVideo'])

        # Adding model 'Event'
        db.create_table('central_event', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('start_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=512)),
        ))
        db.send_create_signal('central', ['Event'])

        # Adding model 'MediaObject'
        db.create_table('central_mediaobject', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['central.Event'])),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['central.MediaObject'], null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=512)),
        ))
        db.send_create_signal('central', ['MediaObject'])

        # Adding model 'ResponseObject'
        db.create_table('central_responseobject', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=512, null=True, blank=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=512)),
        ))
        db.send_create_signal('central', ['ResponseObject'])

    def backwards(self, orm):
        # Deleting model 'MediaObjectContent'
        db.delete_table('central_mediaobjectcontent')

        # Deleting model 'YoutubeVideo'
        db.delete_table('central_youtubevideo')

        # Deleting model 'Event'
        db.delete_table('central_event')

        # Deleting model 'MediaObject'
        db.delete_table('central_mediaobject')

        # Deleting model 'ResponseObject'
        db.delete_table('central_responseobject')

    models = {
        'central.event': {
            'Meta': {'object_name': 'Event'},
            'end_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'start_datetime': ('django.db.models.fields.DateTimeField', [], {})
        },
        'central.mediaobject': {
            'Meta': {'object_name': 'MediaObject'},
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
            'Meta': {'object_name': 'ResponseObject'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
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