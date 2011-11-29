# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding M2M table for field Managers on 'Club'
        db.create_table('Dojo_club_Managers', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('club', models.ForeignKey(orm['Dojo.club'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('Dojo_club_Managers', ['club_id', 'user_id'])


    def backwards(self, orm):
        
        # Removing M2M table for field Managers on 'Club'
        db.delete_table('Dojo_club_Managers')


    models = {
        'Dojo.club': {
            'Managers': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False'}),
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
        'Dojo.rankrecord': {
            'DateOccured': ('django.db.models.fields.DateField', [], {}),
            'Meta': {'ordering': "['DateOccured', 'Rank']", 'object_name': 'RankRecord'},
            'Person': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['Dojo.Person']", 'null': 'True'}),
            'Rank': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
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
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['Dojo']
