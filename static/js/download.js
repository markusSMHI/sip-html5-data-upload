

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

function formatFileSize(bytes) {
	if (typeof bytes !== 'number') {
		console.log("nothing returned")
		return '';
	}
	if (bytes >= 1000000000) {	
		return (bytes / 1000000000).toFixed(2) + ' GB';
	}
	if (bytes >= 1000000) {
		return (bytes / 1000000).toFixed(2) + ' MB';
		console.log("mb returned")		
	}
	
	console.log("kb returned")		
	return (bytes / 1000).toFixed(2) + ' KB';
	

}

$(function () {
    'use strict';
	
	// // Initialize the jQuery File Upload widget:
    // $('#fileupload').fileupload({
        // // Uncomment the following to send cross-domain cookies:
        // //xhrFields: {withCredentials: true},
        // url: 'download'			
    // });
	
    // // Enable iframe cross-domain access via redirect option:
    // $('#fileupload').fileupload(
        // 'option',
        // 'redirect',
        // window.location.href.replace(
            // /\/[^\/]*$/,
            // '/cors/result.html?%s'
        // )
    // );

	// // Not sure what this does?
	// $('#fileupload').addClass('fileupload-processing');
	
	// $.ajax({
		// // Uncomment the following to send cross-domain cookies:
		// //xhrFields: {withCredentials: true},
		// // data: $('#datasetID').val(), 	// pass information on the dataset (= folder) (OLD CODE)
		// data: {								// pass information on the dataset (= folder)	
			// dataset: $('#datasetID').val()
		// },		
		// url: $('#fileupload').fileupload('option', 'url'),	// OLD ORIGINAL CODE           	
		// dataType: 'json',
		// context: $('#fileupload')[0],	
	// }).always(function () {
		// $(this).removeClass('fileupload-processing');	// Not sure what this does?
	// }).done(function (result) {
		// $(this).fileupload('option', 'done')
			// .call(this, $.Event('done'), {result: result});
	// });	
});

