# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'TechniqueTag.Name'
        db.add_column('Technique_techniquetag', 'Name', self.gf('django.db.models.fields.CharField')(default=' ', max_length=255), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'TechniqueTag.Name'
        db.delete_column('Technique_techniquetag', 'Name')


    models = {
        'Dojo.club': {
            'Members': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['Dojo.Person']", 'through': "orm['Dojo.MemberRecord']", 'symmetrical': 'False'}),
            'Meta': {'ordering': "['Name']", 'object_name': 'Club'},
            'Name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'Dojo.memberrecord': {
            'Club': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Dojo.Club']"}),
            'DateOccured': ('django.db.models.fields.DateField', [], {}),
            'Meta': {'ordering': "['Club', 'DateOccured']", 'object_name': 'MemberRecord'},
            'Person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Dojo.Person']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'Dojo.person': {
            'Email': ('django.db.models.fields.EmailField', [], {'default': 'None', 'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'Gender': ('django.db.models.fields.CharField', [], {'default': "'Male'", 'max_length': '10'}),
            'Meta': {'ordering': "['Name']", 'object_name': 'Person'},
            'Name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Picture': ('django.db.models.fields.files.ImageField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'PracticeAttended': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['Dojo.Practice']", 'through': "orm['Dojo.PracticeRecord']", 'symmetrical': 'False'}),
            'Requirements': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['Dojo.Requirement']", 'through': "orm['Dojo.RequirementRecord']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_instructor': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'Dojo.practice': {
            'Club': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['Dojo.Club']", 'null': 'True'}),
            'Date': ('django.db.models.fields.DateField', [], {}),
            'Meta': {'ordering': "['Club', 'Date']", 'object_name': 'Practice'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'Dojo.practicerecord': {
            'DateOccured': ('django.db.models.fields.DateField', [], {}),
            'Meta': {'ordering': "['Practice', 'DateOccured']", 'object_name': 'PracticeRecord'},
            'Person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Dojo.Person']"}),
            'Practice': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Dojo.Practice']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'Dojo.requirement': {
            'Club': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['Dojo.Club']", 'null': 'True'}),
            'Meta': {'ordering': "['Name']", 'object_name': 'Requirement'},
            'Name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'URL': ('django.db.models.fields.URLField', [], {'default': 'None', 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'Valid_for': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'Dojo.requirementrecord': {
            'DateOccured': ('django.db.models.fields.DateField', [], {}),
            'Meta': {'ordering': "['Requirement', 'DateOccured']", 'object_name': 'RequirementRecord'},
            'Person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Dojo.Person']"}),
            'Requirement': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Dojo.Requirement']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'Technique.technique': {
            'Meta': {'object_name': 'Technique'},
            'Name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Practices': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['Dojo.Practice']", 'symmetrical': 'False'}),
            'Slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'Technique.techniquetag': {
            'Meta': {'object_name': 'TechniqueTag'},
            'Name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'Technique': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['Technique.Technique']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['Technique']
