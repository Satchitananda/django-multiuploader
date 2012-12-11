setup_filecollector = function($,uploadedWidgetHtmlName,sendbutton_id,doSubmitLock){
    
    $(document).ready(function(){
	    function collectfiles(){
		    var files_inputs = '';
		    $('.filelink').each(function(i, el) { 
			    files_inputs += '<input type="hidden" value="'+$(el).attr('id')+'" name="'+uploadedWidgetHtmlName+'"/>';
		    });
		    $("#hidden_container").append(files_inputs);
	    };

    $("#"+sendbutton_id).click(function(e){
		    if (doSubmitLock){
			        var isUploading = $(".fileupload-progressbar").is(":visible");
			
			        if (isUploading){	
				        e.preventDefault();
			        }
			        else {
				        collectfiles();
			        }
			   }
		    else
			    collectfiles();
	    });
    });
}

