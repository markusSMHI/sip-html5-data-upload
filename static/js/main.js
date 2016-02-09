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

function validateForm() {	
	
    var datasetname = document.getElementById("datasetnameID").value;	
	var re = /^[a-zA-Z].*/;	
    if (re.test(datasetname))
	{		
        return true;
    } else{	
	
		setMessage("alert alert-warning", "fa fa-4x fa-fw fa-pull-left fa-exclamation-triangle", "Dataset name is not valid. The name should start with a letter and may not contain spaces or special characters. Please try again.");
        return false;
    }
}


$(function () {
    'use strict';
	
	$( "#regularserver" ).click(function() {
		var message = "Regular file server, suitable for all file types";
		setMessage("alert alert-success", "fa fa-4x fa-fw fa-pull-left fa-info-circle", message);		
	});	
	
	$( "#geoserver" ).click(function() {
		var message = "Geoserver can store various geodata formats, such as shapefiles and GeoTIFFs. Data can be accessed using WMS and WFS, enabling online visualization and partial file downloads.";
		setMessage("alert alert-success", "fa fa-4x fa-fw fa-pull-left fa-info-circle", message);
	});	
	
	$( "#thredds" ).click(function() {
		var message = "The THREDDS Data Server (TDS) is a web server that provides data access for scientific grid datasets (such as NetCDF), using a variety of remote data access protocols.";
		setMessage("alert alert-success", "fa fa-4x fa-fw fa-pull-left fa-info-circle", message);	
	});		
	
	$( "#datasetnameID" ).click(function() {	
		var message = "The dataset name should be as specific as possible and contain the variable and source of data (in that order). The name must start with a letter and may not contain spaces or special characters.";
		setMessage("alert alert-success", "fa fa-4x fa-fw fa-pull-left fa-info-circle", message);
	});				
	
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

	// Not sure what this does?
	$('#fileupload').addClass('fileupload-processing');
	
	$.ajax({
		// Uncomment the following to send cross-domain cookies:
		//xhrFields: {withCredentials: true},
		// data: $('#datasetID').val(), 	// pass information on the dataset (= folder) (OLD CODE)
		data: {								// pass information on the dataset (= folder)	
			dataset: $('#datasetID').val()
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

