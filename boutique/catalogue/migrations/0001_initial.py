# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Beer'
        db.create_table(u'catalogue_beer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(default='images/missing.jpg', max_length=100)),
            ('price', self.gf('django.db.models.fields.DecimalField')(default='0.0', max_digits=12, decimal_places=2)),
            ('abv', self.gf('django.db.models.fields.DecimalField')(default='0.0', max_digits=12, decimal_places=2)),
        ))
        db.send_create_signal(u'catalogue', ['Beer'])


    def backwards(self, orm):
        # Deleting model 'Beer'
        db.delete_table(u'catalogue_beer')


    models = {
        u'catalogue.beer': {
            'Meta': {'object_name': 'Beer'},
            'abv': ('django.db.models.fields.DecimalField', [], {'default': "'0.0'", 'max_digits': '12', 'decimal_places': '2'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'default': "'images/missing.jpg'", 'max_length': '100'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'price': ('django.db.models.fields.DecimalField', [], {'default': "'0.0'", 'max_digits': '12', 'decimal_places': '2'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        }
    }

    complete_apps = ['catalogue']