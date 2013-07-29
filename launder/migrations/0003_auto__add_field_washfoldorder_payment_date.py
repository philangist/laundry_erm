# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'WashFoldOrder.payment_date'
        db.add_column(u'launder_washfoldorder', 'payment_date',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.date.today),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'WashFoldOrder.payment_date'
        db.delete_column(u'launder_washfoldorder', 'payment_date')


    models = {
        u'launder.drycleaning': {
            'Meta': {'object_name': 'DryCleaning'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'garment_amount': ('django.db.models.fields.IntegerField', [], {}),
            'garment_type': ('django.db.models.fields.TextField', [], {'max_length': '12'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'payment_finalized': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'payment_method': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'total_cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'})
        },
        u'launder.laundryshirtsorder': {
            'Meta': {'object_name': 'LaundryShirtsOrder'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'payment_finalized': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'payment_method': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'shirts_amount': ('django.db.models.fields.IntegerField', [], {}),
            'shirts_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'starched': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'total_cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'})
        },
        u'launder.washfoldorder': {
            'Meta': {'object_name': 'WashFoldOrder'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'comments': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'payment_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.date.today'}),
            'payment_finalized': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'payment_method': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'total_cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'})
        }
    }

    complete_apps = ['launder']