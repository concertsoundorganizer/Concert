from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.files.uploadedfile import SimpleUploadedFile

from concertapp.models  import *
from concertapp.forms   import UploadFileForm

from concertapp.audio import audioFormats, audioHelpers
from concertapp.audio.waveform import *
from concertapp.settings import MEDIA_ROOT, LOGIN_REDIRECT_URL

import os, tempfile, audiotools

CHUNKSIZE = 1024 * 32

##
# View all of the audio files you have uploaded
#
# @param request    HTTP Request
##
@login_required
def audio(request):
    audio = Audio.objects.filter(user = request.user)

    return render_to_response("audio.html", {'audio': audio},
            RequestContext(request))

##
# Views a single audio file
#
# @param request    HTTP Request
# @param audio_id   The audio object id
##
def view_audio(request, audio_id):
    audio = Audio.objects.get(pk = audio_id)
    return render_to_response("view_audio.html", {'audio': audio}, RequestContext(request))

##
# Takes an audio file, converts it to mp3, ogg, and wav, saving it to disk
# 
# @param request    HTTP Request
##
@login_required
def upload_audio(request):
    if request.method == 'POST' and "wavfile" in request.FILES:
        # Need to add the user to the audio instance
        user = request.user
        
        # grab the filename of the temporary uploaded file
        inputFilePath = request.FILES['wavfile'].temporary_file_path()

        #   Upload a dummy file (just containing 'a'), just so we can get a 
        #   unique filename.  This will be the actual .wav file soon.
        fileName = os.path.split(str(request.FILES['wavfile']))[-1]
        wavFile = SimpleUploadedFile(fileName+'.wav', 'a')
        
        #   Audio object with dummy wav file in it
        audio = Audio(user = user, wavfile = wavFile, filename = fileName)
        
        form = UploadFileForm(request.POST, instance = audio)
        if form.is_valid():
            #   Save the form, copies the dummy file to the proper location
            audio = form.save()
            
            #   Now we can get the new dummy file location with the
            #   auto-generated name
            outputFilePath = os.path.join(MEDIA_ROOT, str(audio.wavfile))

            try:
                # Create the normalized .wav file at the location specified
                # above.  This will overwrite the dummy file we created.
                # Also we must handle errors here.
                audioHelpers.toNormalizedWav(inputFilePath, outputFilePath)
                
                #Create ogg and mp3 versions of the audio (and handle errors)
                audio.create_ogg_and_mp3()
                
            except (
                audiotools.UnsupportedFile, 
                IOError, 
                audiotools.PCMReaderError,
                Exception
            ), e:
                # Right now we have no better way to handle errors
                errorText = 'Error: '+str(e)
                response = HttpResponse(mimetype='text/plain')
                response.write(errorText)
                audio.delete()
                return response
            
            # Generate the waveform onto disk
            audio.generate_waveform()

            audio.save()
            

            # Get audio duration in seconds
            duration = get_duration(audio)

            # Get user's default group
            default_group = user.groups.get(name = user.username)

            # Determine name of segment and tag
            name = audio.filename

            # Create the initial audio segment
            first_segment = AudioSegment(name = name, beginning = 0, end = duration, audio = audio)
            first_segment.save()

            # Tag segment with default tag
            default_tag = Tag.objects.get(group = default_group, tag = 'Uploads')
            default_tag.segments.add(first_segment)
            default_tag.save()
        
        
    
    if "ajax" in request.POST:
        response = HttpResponse(mimetype='text/plain', responseText = 'success');
        response.write("success")
        return response
    else:
        return HttpResponseRedirect('/audio/')
                    

##
# Display the waveform for an audio object
# 
# @param request     HTTP Request
# @param audio_id    The audio object id
##
def view_waveform(request, audio_id):
    return render_to_response('view_waveform.html', {'audio': a}, RequestContext(request))

###
#   responds in plain text with the audio waveform url for the requested
#   audio object.
#
#   @param          request         HTTP request
#   @param          audio_id        The Audio object id
#   @param          type_waveform   specifies which image is wanted
###
def waveform_src(request, audio_id, type_waveform = 'viewer'):
    audio = Audio.objects.get(pk = audio_id)
    
    # return waveform path in plaintext
    response = HttpResponse(mimetype='text/plain')
    if type_waveform == 'viewer':
        response.write(audio.waveformViewer.url)
    elif type_waveform == 'editor':    
        response.write(audio.waveformEditor.url)
    else:
        raise Exception("paramater type_waveform can be either 'viewer' or 'editor', '" + type_waveform + "' its invalid")
        return
        
    return response
    
###
#   Responds in plain text with the path to the file associated with
#   the requested Audio object, at the requested type
#
#   @param          request         HTTP request
#   @param          audio_id        The Audio object id
#   @param          audio_type      'wav', 'mp3', or 'ogg'.
###/    
def audio_src(request, audio_id, audio_type):
    audio = Audio.objects.get(pk = audio_id)
    
    #return audio src in plaintext
    response = HttpResponse(mimetype='text/plain')
    
    # Return only audio type requested
    if(audio_type == 'wav'):
        response.write(audio.wavfile.url)
    elif(audio_type == 'mp3'):
        response.write(audio.mp3file.url)
    elif(audio_type == 'ogg'):
        response.write(audio.oggfile.url)
        
    return response


###
# Returns the duration of the audio file associated with the passed-in audio object.
#
# @param      audio     The audio object.
###
def get_duration(audio):
  # Create wav object
  wavObj = audioFormats.Wav(os.path.join(MEDIA_ROOT, str(audio.wavfile)))
  # Get duration
  return wavObj.getLength()

##
# Delete the audio object and all objects referencing it, including files on
# disk
#
# @param request    HTTP Request
# @param audio_id   The id of the audio object to delete
##
def delete_audio(request, audio_id):
    audio = Audio.objects.get(pk = audio_id)

    # Bounce user if not the owner
    if int(request.user.id) != int(audio.user.id):
        return Http404

    audio.delete()

    return HttpResponseRedirect('/audio/')

##
#   Add the specified segment to the specified group.  This means
#   creating a new segment object for this group, as well as 
#   new tag objects for any of the specified segment's tags
#   unless there is a tag in the new group that is named the same.
#
#   @param      request         HTTP request
#   @param      segment_id      The id of the specified segment
#   @param      group_id        the id of the specified group
###
def add_segment_to_group(request, segment_id, group_id) :

    # Get the specified segment
    old_segment = AudioSegment.objects.get(pk = segment_id)
    
    # First we need to create the new audio segment with the properties of the old one
    new_segment = AudioSegment(name = old_segment.name, beginning = old_segment.beginning, end = old_segment.end, audio = old_segment.audio)
    new_segment.save()
    
    #   Next, we need to add all of the tags from the old segment/group, to the new segment/group, but 
    #   not if a tag with the same name already exists for the new group.
    
    # Get all of the specified segment's tags (except for Uploads)
    old_segment_tags = old_segment.tag_set.all().exclude(tag = 'Uploads')
    
    # Get specified group
    group = Group.objects.get(pk = group_id)
    
    # Get all tags associated with this group (except for uploads tag)
    group_tags = Tag.objects.filter(group = group).exclude(tag = 'Uploads')
    
    # For each of the old segment's tags
    for old_tag in old_segment_tags :
        
        # If the new group has a tag that is named the same
        try :
            other_version_of_tag = group_tags.get(tag = old_tag.tag)
            
            # Add the new segment to this group's version of the tag
            other_version_of_tag.segments.add(new_segment)
            other_version_of_tag.save()
            
        # If the new group does not have a tag matching this name
        except Tag.DoesNotExist:
            # Create the tag within the group
            new_tag = Tag(tag = old_tag.tag, group = group, isProject = 0, isFixture = 0)
            new_tag.save()
            # Add the segment to the newly created tag
            new_tag.segments.add(new_segment)
            new_tag.save()
            
    
    # We will return plaintext response
    response = HttpResponse(mimetype='text/plain')
    # If an error variable was defined in this scope
    if 'error' in locals() :
        response.write(error)
    else :
        response.write('success')
    return response
