/**
 *  @file       SegmentWidget.js
 *  @author     Colin Sullivan <colinsul [at] gmail.com>
 **/


/**
 *  This is the widget associated with an audio segment on the organize page.
 *	@class
 *  @extends    AudioListWidget
 **/
var SegmentWidget = AudioListWidget.extend(
	/**
	 *	@scope	SegmentWidget.prototype
	 **/
{
    initialize: function() {
        AudioListWidget.prototype.initialize.call(this);
        
        var params = this.options;        
        
        _.bindAll(this, "render");
        this.render();
    }, 
    /**
     *  When this widget's delete button is clicked.
     **/    
    _handle_delete_click: function() {
        AudioListWidget.prototype._handle_delete_click.call(this);
        
        this.panel.page.delete_audio_segment(this.model);
    }, 
});