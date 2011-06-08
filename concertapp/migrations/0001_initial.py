# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'ConcertUser'
        db.create_table('concertapp_concertuser', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True)),
        ))
        db.send_create_signal('concertapp', ['ConcertUser'])

        # Adding M2M table for field unreadEvents on 'ConcertUser'
        db.create_table('concertapp_concertuser_unreadEvents', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('concertuser', models.ForeignKey(orm['concertapp.concertuser'], null=False)),
            ('event', models.ForeignKey(orm['concertapp.event'], null=False))
        ))
        db.create_unique('concertapp_concertuser_unreadEvents', ['concertuser_id', 'event_id'])

        # Adding model 'Event'
        db.create_table('concertapp_event', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('collection', self.gf('django.db.models.fields.related.ForeignKey')(related_name='events', to=orm['concertapp.Collection'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('audioSegment', self.gf('django.db.models.fields.related.ForeignKey')(related_name='events', null=True, to=orm['concertapp.AudioSegment'])),
            ('audioFile', self.gf('django.db.models.fields.related.ForeignKey')(related_name='events', null=True, to=orm['concertapp.AudioFile'])),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(related_name='events', null=True, to=orm['concertapp.Tag'])),
            ('eventType', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('concertapp', ['Event'])

        # Adding model 'AudioSegmentCreatedEvent'
        db.create_table('concertapp_audiosegmentcreatedevent', (
            ('event_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['concertapp.Event'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('concertapp', ['AudioSegmentCreatedEvent'])

        # Adding model 'AudioSegmentTaggedEvent'
        db.create_table('concertapp_audiosegmenttaggedevent', (
            ('event_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['concertapp.Event'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('concertapp', ['AudioSegmentTaggedEvent'])

        # Adding model 'AudioFileUploadedEvent'
        db.create_table('concertapp_audiofileuploadedevent', (
            ('event_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['concertapp.Event'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('concertapp', ['AudioFileUploadedEvent'])

        # Adding model 'JoinCollectionEvent'
        db.create_table('concertapp_joincollectionevent', (
            ('event_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['concertapp.Event'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('concertapp', ['JoinCollectionEvent'])

        # Adding model 'LeaveCollectionEvent'
        db.create_table('concertapp_leavecollectionevent', (
            ('event_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['concertapp.Event'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('concertapp', ['LeaveCollectionEvent'])

        # Adding model 'CreateCollectionEvent'
        db.create_table('concertapp_createcollectionevent', (
            ('event_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['concertapp.Event'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('concertapp', ['CreateCollectionEvent'])

        # Adding model 'RequestJoinCollectionEvent'
        db.create_table('concertapp_requestjoincollectionevent', (
            ('event_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['concertapp.Event'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('concertapp', ['RequestJoinCollectionEvent'])

        # Adding model 'RequestDeniedEvent'
        db.create_table('concertapp_requestdeniedevent', (
            ('event_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['concertapp.Event'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('concertapp', ['RequestDeniedEvent'])

        # Adding model 'RequestRevokedEvent'
        db.create_table('concertapp_requestrevokedevent', (
            ('event_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['concertapp.Event'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('concertapp', ['RequestRevokedEvent'])

        # Adding model 'AudioSegment'
        db.create_table('concertapp_audiosegment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('beginning', self.gf('django.db.models.fields.FloatField')()),
            ('end', self.gf('django.db.models.fields.FloatField')()),
            ('audioFile', self.gf('django.db.models.fields.related.ForeignKey')(related_name='segments', to=orm['concertapp.AudioFile'])),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('collection', self.gf('django.db.models.fields.related.ForeignKey')(related_name='segments', to=orm['concertapp.Collection'])),
        ))
        db.send_create_signal('concertapp', ['AudioSegment'])

        # Adding model 'Collection'
        db.create_table('concertapp_collection', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('admin', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('concertapp', ['Collection'])

        # Adding M2M table for field users on 'Collection'
        db.create_table('concertapp_collection_users', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('collection', models.ForeignKey(orm['concertapp.collection'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('concertapp_collection_users', ['collection_id', 'user_id'])

        # Adding model 'Request'
        db.create_table('concertapp_request', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('collection', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['concertapp.Collection'])),
            ('status', self.gf('django.db.models.fields.CharField')(default='p', max_length=1)),
        ))
        db.send_create_signal('concertapp', ['Request'])

        # Adding model 'Tag'
        db.create_table('concertapp_tag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('collection', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tags', to=orm['concertapp.Collection'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('concertapp', ['Tag'])

        # Adding M2M table for field segments on 'Tag'
        db.create_table('concertapp_tag_segments', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('tag', models.ForeignKey(orm['concertapp.tag'], null=False)),
            ('audiosegment', models.ForeignKey(orm['concertapp.audiosegment'], null=False))
        ))
        db.create_unique('concertapp_tag_segments', ['tag_id', 'audiosegment_id'])

        # Adding model 'Comment'
        db.create_table('concertapp_comment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('comment', self.gf('django.db.models.fields.TextField')()),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('concertapp', ['Comment'])

        # Adding model 'TagComment'
        db.create_table('concertapp_tagcomment', (
            ('comment_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['concertapp.Comment'], unique=True, primary_key=True)),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['concertapp.Tag'])),
        ))
        db.send_create_signal('concertapp', ['TagComment'])

        # Adding model 'SegmentComment'
        db.create_table('concertapp_segmentcomment', (
            ('comment_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['concertapp.Comment'], unique=True, primary_key=True)),
            ('segment', self.gf('django.db.models.fields.related.ForeignKey')(related_name='comments', to=orm['concertapp.AudioSegment'])),
        ))
        db.send_create_signal('concertapp', ['SegmentComment'])

        # Adding model 'AudioFile'
        db.create_table('concertapp_audiofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('uploader', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('collection', self.gf('django.db.models.fields.related.ForeignKey')(related_name='files', to=orm['concertapp.Collection'])),
            ('wav', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('ogg', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('mp3', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('duration', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=8, decimal_places=2)),
        ))
        db.send_create_signal('concertapp', ['AudioFile'])


    def backwards(self, orm):
        
        # Deleting model 'ConcertUser'
        db.delete_table('concertapp_concertuser')

        # Removing M2M table for field unreadEvents on 'ConcertUser'
        db.delete_table('concertapp_concertuser_unreadEvents')

        # Deleting model 'Event'
        db.delete_table('concertapp_event')

        # Deleting model 'AudioSegmentCreatedEvent'
        db.delete_table('concertapp_audiosegmentcreatedevent')

        # Deleting model 'AudioSegmentTaggedEvent'
        db.delete_table('concertapp_audiosegmenttaggedevent')

        # Deleting model 'AudioFileUploadedEvent'
        db.delete_table('concertapp_audiofileuploadedevent')

        # Deleting model 'JoinCollectionEvent'
        db.delete_table('concertapp_joincollectionevent')

        # Deleting model 'LeaveCollectionEvent'
        db.delete_table('concertapp_leavecollectionevent')

        # Deleting model 'CreateCollectionEvent'
        db.delete_table('concertapp_createcollectionevent')

        # Deleting model 'RequestJoinCollectionEvent'
        db.delete_table('concertapp_requestjoincollectionevent')

        # Deleting model 'RequestDeniedEvent'
        db.delete_table('concertapp_requestdeniedevent')

        # Deleting model 'RequestRevokedEvent'
        db.delete_table('concertapp_requestrevokedevent')

        # Deleting model 'AudioSegment'
        db.delete_table('concertapp_audiosegment')

        # Deleting model 'Collection'
        db.delete_table('concertapp_collection')

        # Removing M2M table for field users on 'Collection'
        db.delete_table('concertapp_collection_users')

        # Deleting model 'Request'
        db.delete_table('concertapp_request')

        # Deleting model 'Tag'
        db.delete_table('concertapp_tag')

        # Removing M2M table for field segments on 'Tag'
        db.delete_table('concertapp_tag_segments')

        # Deleting model 'Comment'
        db.delete_table('concertapp_comment')

        # Deleting model 'TagComment'
        db.delete_table('concertapp_tagcomment')

        # Deleting model 'SegmentComment'
        db.delete_table('concertapp_segmentcomment')

        # Deleting model 'AudioFile'
        db.delete_table('concertapp_audiofile')


    models = {
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
        'concertapp.audiofile': {
            'Meta': {'object_name': 'AudioFile'},
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'files'", 'to': "orm['concertapp.Collection']"}),
            'duration': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mp3': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'ogg': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'uploader': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'wav': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        },
        'concertapp.audiofileuploadedevent': {
            'Meta': {'object_name': 'AudioFileUploadedEvent', '_ormbases': ['concertapp.Event']},
            'event_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['concertapp.Event']", 'unique': 'True', 'primary_key': 'True'})
        },
        'concertapp.audiosegment': {
            'Meta': {'object_name': 'AudioSegment'},
            'audioFile': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'segments'", 'to': "orm['concertapp.AudioFile']"}),
            'beginning': ('django.db.models.fields.FloatField', [], {}),
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'segments'", 'to': "orm['concertapp.Collection']"}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'end': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'concertapp.audiosegmentcreatedevent': {
            'Meta': {'object_name': 'AudioSegmentCreatedEvent', '_ormbases': ['concertapp.Event']},
            'event_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['concertapp.Event']", 'unique': 'True', 'primary_key': 'True'})
        },
        'concertapp.audiosegmenttaggedevent': {
            'Meta': {'object_name': 'AudioSegmentTaggedEvent', '_ormbases': ['concertapp.Event']},
            'event_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['concertapp.Event']", 'unique': 'True', 'primary_key': 'True'})
        },
        'concertapp.collection': {
            'Meta': {'object_name': 'Collection'},
            'admin': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'collections'", 'symmetrical': 'False', 'to': "orm['auth.User']"})
        },
        'concertapp.comment': {
            'Meta': {'object_name': 'Comment'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'comment': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'concertapp.concertuser': {
            'Meta': {'object_name': 'ConcertUser'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'unreadEvents': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['concertapp.Event']", 'symmetrical': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'concertapp.createcollectionevent': {
            'Meta': {'object_name': 'CreateCollectionEvent', '_ormbases': ['concertapp.Event']},
            'event_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['concertapp.Event']", 'unique': 'True', 'primary_key': 'True'})
        },
        'concertapp.event': {
            'Meta': {'object_name': 'Event'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'audioFile': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'events'", 'null': 'True', 'to': "orm['concertapp.AudioFile']"}),
            'audioSegment': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'events'", 'null': 'True', 'to': "orm['concertapp.AudioSegment']"}),
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'events'", 'to': "orm['concertapp.Collection']"}),
            'eventType': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'events'", 'null': 'True', 'to': "orm['concertapp.Tag']"}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'concertapp.joincollectionevent': {
            'Meta': {'object_name': 'JoinCollectionEvent', '_ormbases': ['concertapp.Event']},
            'event_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['concertapp.Event']", 'unique': 'True', 'primary_key': 'True'})
        },
        'concertapp.leavecollectionevent': {
            'Meta': {'object_name': 'LeaveCollectionEvent', '_ormbases': ['concertapp.Event']},
            'event_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['concertapp.Event']", 'unique': 'True', 'primary_key': 'True'})
        },
        'concertapp.request': {
            'Meta': {'object_name': 'Request'},
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['concertapp.Collection']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'p'", 'max_length': '1'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'concertapp.requestdeniedevent': {
            'Meta': {'object_name': 'RequestDeniedEvent', '_ormbases': ['concertapp.Event']},
            'event_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['concertapp.Event']", 'unique': 'True', 'primary_key': 'True'})
        },
        'concertapp.requestjoincollectionevent': {
            'Meta': {'object_name': 'RequestJoinCollectionEvent', '_ormbases': ['concertapp.Event']},
            'event_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['concertapp.Event']", 'unique': 'True', 'primary_key': 'True'})
        },
        'concertapp.requestrevokedevent': {
            'Meta': {'object_name': 'RequestRevokedEvent', '_ormbases': ['concertapp.Event']},
            'event_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['concertapp.Event']", 'unique': 'True', 'primary_key': 'True'})
        },
        'concertapp.segmentcomment': {
            'Meta': {'object_name': 'SegmentComment', '_ormbases': ['concertapp.Comment']},
            'comment_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['concertapp.Comment']", 'unique': 'True', 'primary_key': 'True'}),
            'segment': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'comments'", 'to': "orm['concertapp.AudioSegment']"})
        },
        'concertapp.tag': {
            'Meta': {'object_name': 'Tag'},
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tags'", 'to': "orm['concertapp.Collection']"}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'segments': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'tags'", 'symmetrical': 'False', 'to': "orm['concertapp.AudioSegment']"})
        },
        'concertapp.tagcomment': {
            'Meta': {'object_name': 'TagComment', '_ormbases': ['concertapp.Comment']},
            'comment_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['concertapp.Comment']", 'unique': 'True', 'primary_key': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['concertapp.Tag']"})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['concertapp']
