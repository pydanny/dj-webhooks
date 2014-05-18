# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'WebhookTarget'
        db.create_table('djwebhooks_webhooktarget', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.User'], related_name='webhooks')),
            ('event', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('identifier', self.gf('django.db.models.fields.CharField')(blank=True, max_length=255)),
            ('target_url', self.gf('django.db.models.fields.URLField')(max_length=255)),
            ('header_content_type', self.gf('django.db.models.fields.CharField')(default='application/json', max_length=255)),
        ))
        db.send_create_signal('djwebhooks', ['WebhookTarget'])

        # Adding model 'Delivery'
        db.create_table('djwebhooks_delivery', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('webhook_target', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['djwebhooks.WebhookTarget'])),
            ('payload', self.gf('jsonfield.fields.JSONField')(default={})),
            ('success', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('attempt', self.gf('django.db.models.fields.IntegerField')()),
            ('hash_value', self.gf('django.db.models.fields.CharField')(blank=True, max_length=255)),
            ('notification', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('response_message', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('response_status', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('response_content_type', self.gf('django.db.models.fields.CharField')(blank=True, max_length=255)),
        ))
        db.send_create_signal('djwebhooks', ['Delivery'])


    def backwards(self, orm):
        # Deleting model 'WebhookTarget'
        db.delete_table('djwebhooks_webhooktarget')

        # Deleting model 'Delivery'
        db.delete_table('djwebhooks_delivery')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True', 'symmetrical': 'False'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'contenttypes.contenttype': {
            'Meta': {'db_table': "'django_content_type'", 'unique_together': "(('app_label', 'model'),)", 'ordering': "('name',)", 'object_name': 'ContentType'},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'djwebhooks.delivery': {
            'Meta': {'ordering': "['-created']", 'object_name': 'Delivery'},
            'attempt': ('django.db.models.fields.IntegerField', [], {}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'hash_value': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'notification': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'payload': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'response_content_type': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255'}),
            'response_message': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'response_status': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'success': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'webhook_target': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['djwebhooks.WebhookTarget']"})
        },
        'djwebhooks.webhooktarget': {
            'Meta': {'ordering': "['-modified']", 'object_name': 'WebhookTarget'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'event': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'header_content_type': ('django.db.models.fields.CharField', [], {'default': "'application/json'", 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.User']", 'related_name': "'webhooks'"}),
            'target_url': ('django.db.models.fields.URLField', [], {'max_length': '255'})
        },
        'users.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True', 'related_name': "'user_set'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True', 'related_name': "'user_set'"}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        }
    }

    complete_apps = ['djwebhooks']