/**
 *  @file       CollectionsPage.js
 *  Initialize all stuff needed on the collections page.
 *  @author     Colin Sullivan <colinsul [at] gmail.com>
 **/
 
function CollectionsPage(params) {
    if(params) {
        this.init(params);
    }
}
CollectionsPage.prototype = new LoggedInPage();

CollectionsPage.prototype.init = function(params) {
    LoggedInPage.prototype.init.call(this, params);

    /**
     *  Create "create/join collection panel"
     **/
    var createJoinCollectionPanel = new CreateJoinCollectionPanel({
        container: $('#create_join_panel'), 
        inputElement: $('#create_join_input'), 
        resultsElement: $('#create_join_results'),
        resultTemplate: $('#create_join_result'),
        createNewTemplate: $('#create_join_create_new')
    });
    this.createJoinCollectionPanel = createJoinCollectionPanel;
    
    /**
     *  "ManageCollectionsPanel"
     **/
    var manageCollectionsPanel = new ManageCollectionsPanel({
        container: $('#manage_collections_panel'), 
        collectionTemplate: $('#collection_template')
    });
    this.manageCollectionsPanel = manageCollectionsPanel;
    
    /** Connect panels **/
    createJoinCollectionPanel.manageCollectionsPanel = manageCollectionsPanel;
    manageCollectionsPanel.globalOptionsPanel = this.globalOptionsPanel;
    
    /* Retrieve collections to manage */
    manageCollectionsPanel.retrieveAndUpdateCollections();
    
}