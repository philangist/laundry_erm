# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'WashFoldOrder'
        db.create_table(u'launder_washfoldorder', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('phone_number', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 8, 19, 0, 0))),
            ('weight', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('num_comforters', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
            ('total_cost', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
            ('payment_method', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('payment_finalized', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('payment_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 8, 19, 0, 0))),
            ('comments', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('staff_comments', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
        ))
        db.send_create_signal(u'launder', ['WashFoldOrder'])

        # Adding model 'DryCleaning'
        db.create_table(u'launder_drycleaning', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('phone_number', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 8, 19, 0, 0))),
            ('garment_type', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('garment_amount', self.gf('django.db.models.fields.IntegerField')()),
            ('total_cost', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
            ('payment_method', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('payment_finalized', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('payment_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 8, 19, 0, 0))),
        ))
        db.send_create_signal(u'launder', ['DryCleaning'])

        # Adding model 'LaundryShirtsOrder'
        db.create_table(u'launder_laundryshirtsorder', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('phone_number', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 8, 19, 0, 0))),
            ('shirts_amount', self.gf('django.db.models.fields.IntegerField')()),
            ('shirts_price', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
            ('starched', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('total_cost', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
            ('payment_method', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('payment_finalized', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('payment_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 8, 19, 0, 0))),
        ))
        db.send_create_signal(u'launder', ['LaundryShirtsOrder'])

        # Adding model 'DailyOperations'
        db.create_table(u'launder_dailyoperations', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 8, 19, 0, 0))),
        ))
        db.send_create_signal(u'launder', ['DailyOperations'])


    def backwards(self, orm):
        # Deleting model 'WashFoldOrder'
        db.delete_table(u'launder_washfoldorder')

        # Deleting model 'DryCleaning'
        db.delete_table(u'launder_drycleaning')

        # Deleting model 'LaundryShirtsOrder'
        db.delete_table(u'launder_laundryshirtsorder')

        # Deleting model 'DailyOperations'
        db.delete_table(u'launder_dailyoperations')


    models = {
        u'launder.dailyoperations': {
            'Meta': {'object_name': 'DailyOperations'},
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 8, 19, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'launder.drycleaning': {
            'Meta': {'object_name': 'DryCleaning'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 8, 19, 0, 0)'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'garment_amount': ('django.db.models.fields.IntegerField', [], {}),
            'garment_type': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'payment_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 8, 19, 0, 0)'}),
            'payment_finalized': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'payment_method': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'total_cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'})
        },
        u'launder.laundryshirtsorder': {
            'Meta': {'object_name': 'LaundryShirtsOrder'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 8, 19, 0, 0)'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'payment_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 8, 19, 0, 0)'}),
            'payment_finalized': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'payment_method': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'shirts_amount': ('django.db.models.fields.IntegerField', [], {}),
            'shirts_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'starched': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'total_cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'})
        },
        u'launder.washfoldorder': {
            'Meta': {'object_name': 'WashFoldOrder'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'comments': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 8, 19, 0, 0)'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'num_comforters': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'payment_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 8, 19, 0, 0)'}),
            'payment_finalized': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'payment_method': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'staff_comments': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'total_cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'weight': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['launder']