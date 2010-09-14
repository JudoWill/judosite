# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Club'
        db.create_table('Dojo_club', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('Slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
        ))
        db.send_create_signal('Dojo', ['Club'])

        # Adding model 'Person'
        db.create_table('Dojo_person', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('Email', self.gf('django.db.models.fields.EmailField')(default=None, max_length=75, null=True, blank=True)),
            ('is_instructor', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('Picture', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal('Dojo', ['Person'])

        # Adding M2M table for field Rank on 'Person'
        db.create_table('Dojo_person_Rank', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('person', models.ForeignKey(orm['Dojo.person'], null=False)),
            ('rankrecord', models.ForeignKey(orm['Dojo.rankrecord'], null=False))
        ))
        db.create_unique('Dojo_person_Rank', ['person_id', 'rankrecord_id'])

        # Adding model 'Requirement'
        db.create_table('Dojo_requirement', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('Slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('URL', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('Valid_for', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('Dojo', ['Requirement'])

        # Adding model 'Practice'
        db.create_table('Dojo_practice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('Dojo', ['Practice'])

        # Adding M2M table for field Club on 'Practice'
        db.create_table('Dojo_practice_Club', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('practice', models.ForeignKey(orm['Dojo.practice'], null=False)),
            ('club', models.ForeignKey(orm['Dojo.club'], null=False))
        ))
        db.create_unique('Dojo_practice_Club', ['practice_id', 'club_id'])

        # Adding model 'RequirementRecord'
        db.create_table('Dojo_requirementrecord', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Dojo.Person'])),
            ('DateOccured', self.gf('django.db.models.fields.DateField')()),
            ('Requirement', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Dojo.Requirement'])),
        ))
        db.send_create_signal('Dojo', ['RequirementRecord'])

        # Adding model 'PracticeRecord'
        db.create_table('Dojo_practicerecord', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Dojo.Person'])),
            ('DateOccured', self.gf('django.db.models.fields.DateField')()),
            ('Practice', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Dojo.Practice'])),
        ))
        db.send_create_signal('Dojo', ['PracticeRecord'])

        # Adding model 'MemberRecord'
        db.create_table('Dojo_memberrecord', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Dojo.Person'])),
            ('DateOccured', self.gf('django.db.models.fields.DateField')()),
            ('Club', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Dojo.Club'])),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('Dojo', ['MemberRecord'])

        # Adding model 'RankRecord'
        db.create_table('Dojo_rankrecord', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Dojo.Person'])),
            ('DateOccured', self.gf('django.db.models.fields.DateField')()),
            ('Rank', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('Dojo', ['RankRecord'])


    def backwards(self, orm):
        
        # Deleting model 'Club'
        db.delete_table('Dojo_club')

        # Deleting model 'Person'
        db.delete_table('Dojo_person')

        # Removing M2M table for field Rank on 'Person'
        db.delete_table('Dojo_person_Rank')

        # Deleting model 'Requirement'
        db.delete_table('Dojo_requirement')

        # Deleting model 'Practice'
        db.delete_table('Dojo_practice')

        # Removing M2M table for field Club on 'Practice'
        db.delete_table('Dojo_practice_Club')

        # Deleting model 'RequirementRecord'
        db.delete_table('Dojo_requirementrecord')

        # Deleting model 'PracticeRecord'
        db.delete_table('Dojo_practicerecord')

        # Deleting model 'MemberRecord'
        db.delete_table('Dojo_memberrecord')

        # Deleting model 'RankRecord'
        db.delete_table('Dojo_rankrecord')


    models = {
        'Dojo.club': {
            'Members': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['Dojo.Person']", 'through': "orm['Dojo.MemberRecord']", 'symmetrical': 'False'}),
            'Meta': {'object_name': 'Club'},
            'Name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'Dojo.memberrecord': {
            'Club': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Dojo.Club']"}),
            'DateOccured': ('django.db.models.fields.DateField', [], {}),
            'Meta': {'object_name': 'MemberRecord'},
            'Person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Dojo.Person']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'Dojo.person': {
            'Email': ('django.db.models.fields.EmailField', [], {'default': 'None', 'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'Meta': {'object_name': 'Person'},
            'Name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'PracticeAttended': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['Dojo.Practice']", 'through': "orm['Dojo.PracticeRecord']", 'symmetrical': 'False'}),
            'Rank': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['Dojo.RankRecord']", 'symmetrical': 'False'}),
            'Requirements': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['Dojo.Requirement']", 'through': "orm['Dojo.RequirementRecord']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_instructor': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'Dojo.practice': {
            'Club': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['Dojo.Club']", 'symmetrical': 'False'}),
            'Date': ('django.db.models.fields.DateField', [], {}),
            'Meta': {'object_name': 'Practice'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'Dojo.practicerecord': {
            'DateOccured': ('django.db.models.fields.DateField', [], {}),
            'Meta': {'object_name': 'PracticeRecord'},
            'Person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Dojo.Person']"}),
            'Practice': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Dojo.Practice']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'Dojo.rankrecord': {
            'DateOccured': ('django.db.models.fields.DateField', [], {}),
            'Meta': {'object_name': 'RankRecord'},
            'Person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Dojo.Person']"}),
            'Rank': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'Dojo.requirement': {
            'Meta': {'object_name': 'Requirement'},
            'Name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'URL': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'Valid_for': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'Dojo.requirementrecord': {
            'DateOccured': ('django.db.models.fields.DateField', [], {}),
            'Meta': {'object_name': 'RequirementRecord'},
            'Person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Dojo.Person']"}),
            'Requirement': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Dojo.Requirement']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['Dojo']
