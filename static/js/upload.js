/*
 * jQuery File Upload Plugin JS Example 8.9.1
 * https://github.com/blueimp/jQuery-File-Upload
 *
 * Copyright 2010, Sebastian Tschan
 * https://blueimp.net
 *
 * Licensed under the MIT license:
 * http://www.opensource.org/licenses/MIT
 *
 * Adjusted by Johan Beekhuizen for the SwitchON Data Upload Tool
 *  
 */

/* global $, window */

function setMessage(messagetype, messagefa, messagetext){
	
	try {	
		//var messagetypeDiv = document.getElementById("messagetype");	// javascript method
		//messagetypeDiv.className = "alert alert-info";				// javascript method
		$('#messagetype').removeClass().addClass(messagetype);
		$('#messagefa').removeClass().addClass(messagefa);
		$('#messagetext').text(messagetext);
	}
		catch(err) {
			console.log(err.message);
	}
}


function checkFilename(filename){
	if (/[^a-z0-9_]/gi.test(filename)) {  // anything but a-zA-Z0-9 - add other permitted characters to suit
		return false;
	}
	else{
		return true;
	}
}


$(function () {
    'use strict';	
	
	// Initialize the jQuery File Upload widget:
    $('#fileupload').fileupload({
        // Uncomment the following to send cross-domain cookies:
        //xhrFields: {withCredentials: true},
        url: 'upload'			
    });
	
    // Enable iframe cross-domain access via redirect option:
    $('#fileupload').fileupload(
        'option',
        'redirect',
        window.location.href.replace(
            /\/[^\/]*$/,
            '/cors/result.html?%s'
        )
    );		
	
	// OWN BUTTON: ZIP FILES
	$('.zip').click(function() {
	
		var filesList = $('.files');	
		console.log("Files to zip:");		
		console.log(filesList);
		
		var toggledFiles = filesList.find('.toggle:checked');			
		var selectedFiles = {};
		var nrFiles = 0		
		
		$(toggledFiles).each(function(i, val) {
			//console.log(val.value);
			selectedFiles[i]=val.value;
			nrFiles++;
			});			
			
		// check if there is at least one file selected
		if (nrFiles > 0) {			
		
			bootbox.prompt({
			  title: "Zip filename (without extension)",
			  value: $('#datasetID').val(),
			  callback: function(result) {
				if (result === null) {
				  console.log("Cancelled");
				} else {
					// check if a valid filename					
					if(checkFilename(result)){
						$.ajax({
							type: "POST",
							url: "/zip",					
							data: JSON.stringify({'files': selectedFiles, 'zipfilename': result}),
							contentType: "application/json; charset=utf-8",
							dataType: "json",
							//success: function(data){alert(data);},
							success: function(data){location.reload();console.log("refresh");},
							failure: function(errMsg) {
								alert(errMsg);
							}
						});
						
						//	
					}
					else{
						setMessage("alert alert-danger", "fa fa-4x fa-fw fa-pull-left fa-exclamation-triangle", "Invalid zip filename! Please try again.")
					}
				}
			  }
			});	
			
		}
		else{
				setMessage("alert alert-warning", "fa fa-4x fa-fw fa-pull-left fa-exclamation-triangle", "Please select at least one file to zip using the checkboxes")
			}
	});		
		

	// Not sure what this does?
	$('#fileupload').addClass('fileupload-processing');
	
	$.ajax({
		// Uncomment the following to send cross-domain cookies:
		//xhrFields: {withCredentials: true},
		// data: $('#datasetID').val(), 	// pass information on the dataset (= folder) (OLD CODE)
		data: {								// pass information on the dataset (= folder)	
			dataset: $('#datasetID').val(),
			servertype: $('#servertypeID').val()
		},		
		url: $('#fileupload').fileupload('option', 'url'),	// OLD ORIGINAL CODE           	
		dataType: 'json',
		context: $('#fileupload')[0],	
	}).always(function () {
		$(this).removeClass('fileupload-processing');	// Not sure what this does?
	}).done(function (result) {
		$(this).fileupload('option', 'done')
			.call(this, $.Event('done'), {result: result});
	});
});
