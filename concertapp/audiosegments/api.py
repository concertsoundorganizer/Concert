from concertapp.lib.api import *
from concertapp.models import *
from concertapp.users.api import *
from concertapp.audio.api import AudioResource
from django.conf.urls.defaults import *
from django.contrib.auth.models import User
from tastypie import fields
from tastypie.authentication import Authentication, BasicAuthentication
from tastypie.authorization import DjangoAuthorization, Authorization
from tastypie.http import *

###
#   Make sure that the user who is trying to modify the board is the administrator.
###
class AudioSegmentAuthorization(ConcertAuthorization):
    def is_authorized(self, request, object=None):
        if super(AudioSegmentAuthorization, self).is_authorized(request, object):
            #   Get is always allowed, since we're just requesting information about
            #   the collection.
            if request.method == 'GET':
                return True
            
            #   If there is an object to authorize
            if object:
                #   Make sure that the person modifying is in the collection that the audiosegment belongs to.
                return (request.user in object.audio.collection.users.all())
            else:
                #   TODO: This currently is always the case (tastypie issues)
                return True
        else:
            return False


class AudioSegmentResource(MyResource):
    creator = fields.ForeignKey(UserResource, 'creator', full=True) 
    audio = fields.ForeignKey(AudioResource, 'audio', full=True)

    class Meta:
        authentication = DjangoAuthentication()
        authorization = AudioSegmentAuthorization()
        
        queryset = AudioSegment.objects.all()
