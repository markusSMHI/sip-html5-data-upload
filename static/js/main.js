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

$(function () {
    'use strict';
	
	// Initialize the jQuery File Upload widget:
    $('#fileupload').fileupload({
        // Uncomment the following to send cross-domain cookies:
        //xhrFields: {withCredentials: true},
        url: 'upload'
		//datasetfolder: $('#datasetID').val()		
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
	//$('#fileupload').addClass('fileupload-processing');
	
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
	}).done(function (result) {
		$(this).fileupload('option', 'done')
			.call(this, $.Event('done'), {result: result});
	});	
	
	// }).always(function () {
		// $(this).removeClass('fileupload-processing');	// Not sure what this does?
	// }).done(function (result) {
		// $(this).fileupload('option', 'done')
			// .call(this, $.Event('done'), {result: result});
	// });


});
