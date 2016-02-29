
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
	
	// $( "#datasetnameID" ).click(function() {	
		// var message = "The dataset name should be as specific as possible and contain the variable and source of data (in that order). The name must start with a letter and may not contain spaces or special characters.";
		// setMessage("alert alert-success", "fa fa-4x fa-fw fa-pull-left fa-info-circle", message);
	// });				

});

