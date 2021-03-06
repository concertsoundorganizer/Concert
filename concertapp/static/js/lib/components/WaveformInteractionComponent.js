/**
 *  @file       WaveformInteractionComponent.js
 *
 *  @author     Colin Sullivan <colinsul [at] gmail.com>
 *              amy wieliczka <amywieliczka [at] gmail.com>
 **/

/**
 *  The component that allows for highlighting functionality on a WaveformPanel.
 *  @class
 *  @extends    Component
 *  @throws     Highlight   -   When a section of the waveform is highlighted.
 **/
var WaveformInteractionComponent = Component.extend(
	/**
	 *	@scope	WaveformInteractionComponent.prototype
	 **/
{
    initialize: function() {
        Component.prototype.initialize.call(this);
        
        var params = this.options;
        
        var el = this.el;
        
        
        /* Determine if highlight is currently disabled (incase someone messes 
        with template) */
        if(el.hasClass('disabled')) {
            this.disabled = true;
        }
        else {
            this.disabled = false;
        }
        
        /* If we are currently dragging a highlight */
        this.dragging = false;
        
        /**
         *  If we are currently adjusting a highlight that already existed.
         **/
        this.adjusting = false;
        
        /* Where the last drag started (x-coordinate) */
        this.lastDragStartX = null;
        
        /* Where the last drag point was (x-coordinate) */
        this.lastDragEndX = null;
        
        /* Cache the duration of the current audio file (we will need it each time
        we highlight) */
        this.audioFileDuration = null;
    }, 
    
    _initializeElements: function() {
        Component.prototype._initializeElements.call(this);
        
        
        /* Get highlight element inside this container */
        var highlight = this.el.children('.highlight');
        if(typeof(highlight) == 'undefined') {
            throw new Error('this.el.children(\'.highlight\') is undefined');
        }
        else if(highlight.length == 0) {
            throw new Error('highlight not found');
        }
        this.highlight = highlight;
        
        /* Get leftHandle element inside this container */
        var leftHandle = this.highlight.children('.leftHandle');
        if(typeof(leftHandle) == 'undefined') {
            throw new Error('this.highlight.children(\'.leftHandle\') is undefined');
        }
        else if(leftHandle.length == 0) {
            throw new Error('leftHandle not found');
        }
        this.leftHandle = leftHandle;

        /* Get rightHandle element inside this container */
        var rightHandle = this.highlight.children('.rightHandle');
        if(typeof(rightHandle) == 'undefined') {
            throw new Error('this.highlight.children(\'.rightHandle\') is undefined');
        }
        else if(rightHandle.length == 0) {
            throw new Error('rightHandle not found');
        }
        this.rightHandle = rightHandle;
            
        this.currentHighlight = {startTime:null,
            endTime:null};
    },
    
    _initializeEvents: function(){
        Component.prototype._initializeEvents.call(this);
        
        /* The element that we are receiving the drag events from (should be defined
        in child classes) */
        var el = this.el;
        
        el.bind('mousedown', function(me) {
            return function(e) {
                e.stopPropagation();
                
                me._handle_mousedown(get_event_x(e));
            };
        }(this));
        
        el.bind('mousemove', function(me) {
            return function(e) {
                e.stopPropagation();
                
                if(me.dragging) {
                    me._handle_mousemove(get_event_x(e));
                }
            };
        }(this));
        
        el.bind('mouseup', function(me) {
            return function(e) {
                e.stopPropagation();
                
                me._handle_mouseup(get_event_x(e));
            };
        }(this));
    }, 
    
    /**
     *  When a mousedown event is triggered on this.el
     *
     *  @param  {Number}    x    -  The x-coordinate where the drag began.
     **/
    _handle_mousedown: function(x) {
        if(this.disabled == false && this.dragging == false && this.handle(x)) {
            this.dragging = true;
            /* we are adjusting the highlight */
            this.adjusting = true;
            
            this.panel.page.clear_waveform_highlight();
        } else {
            /* Save new starting point */
            this.lastDragStartX = x;
            /* We are now dragging */
            this.dragging = true;
        }
    }, 
    
    /**
     *  When a mousemove event is triggered on this.el after a mousedown and before
     *  a mouseup.
     *
     *  @param  {Number}    x   -   The x-coordinate where the drag is currently.
     **/
    _handle_mousemove: function(x) {
        this.lastDragEndX = x;
        
        /* If the mouse has moved out of the 'click' buffer zone.  This ensures
        that the user is actually trying to make a highlight, and didn't just 
        move the mouse a little bit while clicking. */
        if (this.lastDragEndX > this.lastDragStartX + 2 || 
            this.lastDragEndX < this.lastDragStartX - 2) {
                /* Reset any old highlight */
                this.reset();
                /* Draw highlight */
                this.draw_highlight_px(this.lastDragStartX, this.lastDragEndX);
        }

    }, 
    
    /**
     *  When a mouseup event is triggered on this.el
     *
     *  @param  {Number}    x    -  The x-coordinate where the drag has stopped.
     **/
    _handle_mouseup: function(x) {
        
        /* Now determine what the time of the highlight was relative to the audio
        file */
        var dragStartX = this.lastDragStartX;
        var dragEndX = x;
        /* If this was just a click (with a 2px error buffer) */
        if(dragStartX < dragEndX + 2 && dragStartX > dragEndX - 2) {
            /* If click is outside current highlight, and the highlight is enabled */
            if((dragEndX < this.highlight.position().left ||
                dragEndX > this.highlight.position().left + this.highlight.width()) 
                && this.disabled == false) {
                    this.panel.page.disable_audio_loop();
            }
                
            //update audio's currentTime to location clicked
            var seconds = dragStartX/this.panel.get_resolution();
            this.panel.page.set_audio_time(seconds);
            
            /* If click is inside current highlight */
            if((dragEndX > this.highlight.position().left && 
                dragEndX < this.highlight.position().left + this.highlight.width()) 
                && this.disabled == false) {
                    this.panel.page.enable_audio_loop();
            } 
        }
        /* This was a drag */
        else {
            this.leftHandle.removeClass('disabled');
            this.rightHandle.removeClass('disabled');

            var pxPerSecond = this.panel.get_resolution();
            var startTime = Math.min(dragStartX, dragEndX)/pxPerSecond;
            var endTime = Math.max(dragStartX, dragEndX)/pxPerSecond;

            this.currentHighlight.startTime = startTime;
            this.currentHighlight.endTime = endTime;

            /* if we were just adjusting */
            if(this.adjusting) {
                /* Tell page that we've changed segment */
                this.panel.page.modify_current_segment_times(startTime, endTime);
            }
            /* we must have been creating a new segment */
            else {
                /* Tell page about highlight */
                this.panel.page.create_new_segment(startTime, endTime);                
            }
        }

        this.lastDragEndX = x;
        this.dragging = false;
        this.adjusting = false;
    }, 
    
    /**
     *  Called when a highlight is to be drawn on the waveform by pixels.  Takes
     *  two arguments, each of which are x-coordinates relative to the highlight
     *  container.  The order doesn't matter.
     *
     *  @param  {Number}    x    -  One side of the highlight
     *  @param  {Number}    y    -  The other side.
     **/
    draw_highlight_px: function(x, y) {
        
        /* Make highlight visible */
        this.enable();
        
        
        /* If the values are left to right */
        if(x < y) {
            this.highlight.css({
                left: x+'px', 
                width: (y-x)+'px' 
            });
        }
        /* If the drag is from right to left */
        else if(x > y) {
            this.highlight.css({
                left: y+'px', 
                width: (x-y)+'px'
            });
        }
        
    }, 
    
    /**
     *  Called when a highlight is to be drawn on the waveform, but we only have
     *  time information.  Takes two arguments, one for each side of the highlight.
     *
     *  @param  {Number}    t1  -   One side of the highlight
     *  @param  {Number}    t2    - The other side.
     **/
    draw_highlight_sec: function(t1, t2) {
        if (this.currentHighlight.startTime == t1 && this.currentHighlight.endTime == t2) {
            return;
        } else {
            var duration = this.audioFileDuration;
            var pxPerSecond = this.panel.get_resolution();
            var x = (t1/duration)*(duration*pxPerSecond);
            var y = (t2/duration)*(duration*pxPerSecond);
            this.draw_highlight_px(x, y);
        
            this.leftHandle.removeClass('disabled');
            this.rightHandle.removeClass('disabled');
            
            this.currentHighlight.startTime = t1;
            this.currentHighlight.endTime = t2;
        }
    }, 
    
    /**
     *  When an audio file has been selected.  Called from panel.
     *
     *  @param  {AudioFile}    selectedAudioFile    -   The audio file object.
     **/
    audio_file_selected: function(selectedAudioFile) {
        
        var audioFileDuration = selectedAudioFile.get('duration');
        this.audioFileDuration = audioFileDuration;
        
        /* Set width of highlight container element properly */
        this.el.css('width', audioFileDuration*this.panel.get_resolution()+'px');
    }, 
    
    /**
     *  When an audio segment has been selected.  Called from panel.
     *
     *  @param  {AudioSegment}    selectedAudioSegment    - The segment obj.
     **/
    audio_segment_selected: function(selectedAudioSegment) {
        var audioFileDuration = selectedAudioSegment.get('audioFile').get('duration');
        this.audioFileDuration = audioFileDuration;
        
        /* Set width of highlight container element */
        this.el.css('width', audioFileDuration*this.panel.get_resolution()+'px');
        
        /* Draw highlight for this segment */
        this.draw_highlight_sec(
            selectedAudioSegment.get('beginning'),
            selectedAudioSegment.get('end')
        );
        
        /* show highlight */
        this.enable();
    }, 
    
    /**
     *  When this highlight is being used.  Make sure it is visible on UI.
     **/
    enable: function() {
        this.disabled = false;
        this.highlight.removeClass('disabled');
        this.leftHandle.removeClass('disabled');
        this.rightHandle.removeClass('disabled');
    }, 
    
    /**
     *  When this highlight is not being used.  It will not be shown on the screen.
     **/
    disable: function() {
        /* If we are currently dragging, don't disable please */
        if(!this.dragging) {
            this.disabled = true;
            this.highlight.addClass('disabled');
            this.leftHandle.addClass('disabled');
            this.rightHandle.addClass('disabled');            
        }
    }, 
    
    /**
     *  When the highlight is to be reset.  This will reset the width to 0.
     **/
    reset: function() {
        this.disable();

        this.highlight.css({
            width: '0px'
        });
                
        this.panel.page.clear_waveform_highlight();
    },
    
    /**
     *  Checks if mousedown event occurred at the position of the highlight handles
     **/
    handle: function(x) {        
        //if we have the right handle        
        if (x <= ((this.currentHighlight.endTime * this.panel.get_resolution()) + 10) && 
            x >= ((this.currentHighlight.endTime * this.panel.get_resolution()) - 10)) {
                this.lastDragStartX = this.currentHighlight.startTime * this.panel.get_resolution();
                this.lastDragEndX = this.currentHighlight.endTime * this.panel.get_resolution();
                return true;
            }
        //if we have the left handle
        if (x <= ((this.currentHighlight.startTime * this.panel.get_resolution()) + 10) && 
            x >= ((this.currentHighlight.startTime * this.panel.get_resolution()) - 10)) {
                this.lastDragStartX = this.currentHighlight.endTime * this.panel.get_resolution();
                this.lastDragEndX = this.currentHighlight.startTime * this.panel.get_resolution();
                return true;
            }
        
        return false;
    },

});
