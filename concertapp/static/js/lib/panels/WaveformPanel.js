/**
 *  @file       WaveformPanel.js
 *  
 *  @author     Colin Sullivan <colinsul [at] gmail.com>
 **/
 
/**
 *  Abstract class for housing functionality relating to both waveform panels
 *  @class
 *  @extends    Panel
 **/
var WaveformPanel = Panel.extend({
    initialize: function() {
        Panel.prototype.initialize.call(this);

        var params = this.options;
                        
        /* The model manager's selected files */
        var selectedAudioFiles = params.selectedAudioFiles;
        if(typeof(selectedAudioFiles) == 'undefined') {
            throw new Error('params.selectedAudioFiles is undefined');
        }
        this.selectedAudioFiles = selectedAudioFiles;
        
        /* The model manager's selected audio segments */
        var selectedAudioSegments = params.selectedAudioSegments;
        if(typeof(selectedAudioSegments) == 'undefined') {
            throw new Error('params.selectedAudioSegments is undefined');
        }
        this.selectedAudioSegments = selectedAudioSegments;
        
        /* The image element */
        var waveformImageElement = this.el.find('.waveform_image');
        if(typeof(waveformImageElement) == 'undefined') {
            throw new Error('this.el.find(\'.waveform_image\') is undefined');
        }
        else if(waveformImageElement.length == 0) {
            throw new Error('waveformImageElement not found');
        }
        this.waveformImageElement = waveformImageElement;
        
        /* The container for the playhead widget */
        var playheadContainerElement = this.el.find('.playhead');
        if(typeof(playheadContainerElement) == 'undefined') {
            throw new Error('$(\'#detail_waveform_panel_playhead\') is undefined');
        }
        else if(playheadContainerElement.length == 0) {
            throw new Error('playheadContainerElement not found');
        }
        this.playheadContainerElement = playheadContainerElement;

        _.bindAll(this, "render");
        selectedAudioSegments.bind('refresh', this.render);
        selectedAudioSegments.bind('add', this.render);
        selectedAudioSegments.bind('remove', this.render);
        selectedAudioFiles.bind('refresh', this.render);
        selectedAudioFiles.bind('add', this.render);
        selectedAudioFiles.bind('remove', this.render);
    },

    render: function() {
        Panel.prototype.render.call(this);
        
        var selectedAudioFiles = this.selectedAudioFiles;
        var selectedAudioSegments = this.selectedAudioSegments;
        
        /* If there was an audio segment selected */
        if(selectedAudioSegments.length == 1 && selectedAudioFiles.length == 0) {
            throw new Error('Not yet implemented selecting audio segment');
        }
        else if(selectedAudioFiles.length == 1 && selectedAudioSegments.length == 0) {
            this.audio_file_selected(selectedAudioFiles.first());
        }
        else if(selectedAudioFiles.length && selectedAudioSegments.length){
            throw Error('Not yet implemented multiple selection')            
        }
        else {
            throw Error('Not yet implemented when nothing is selected')
        }
        
        return this;
    },    
});
