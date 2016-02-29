


function checkFilename(filename){
	if (/[^a-z0-9]/gi.test(filename)) {  // anything but a-zA-Z0-9 - add other permitted characters to suit
		return false;
	}
	else{
		return true;
	}
}
	
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

	
function validateForm(){	
	
	//return true;
	
	//e.preventDefault();
	
	bootbox.prompt({
		title: "Zip filename",
		value: $('#datasetnameID').val(),
		
		callback: function(result) {
			if (result === null) {
				console.log("Cancelled");
				return false;
			} else {
				// check if a valid filename					
				if(checkFilename(result)){
					$('#zipfilenameID').val(result);  
					console.log("valid zipfilename");
					//$('#downloadallForm').submit();
					return true;
				}
				else{
					setMessage("alert alert-danger", "fa fa-4x fa-fw fa-pull-left fa-exclamation-triangle", "Invalid zip filename! Please try again.")
					return false;
				}
			}
		}	           
	})
  
}


$(function () {
	
	// $('#downloadallForm').on('submit', function(e){
	
        // e.preventDefault();
		
		// bootbox.prompt({
			// title: "Zip filename",
			// value: $('#datasetnameID').val(),
			
			// callback: function(result) {
				// if (result === null) {
					// console.log("Cancelled");
					// //return(false);
				// } else {
					// // check if a valid filename					
					// if(checkFilename(result)){
						// $('#zipfilenameID').val(result);  
						// console.log("valid zipfilename");
						// $('#downloadallForm').submit();
					// }
					// else{
						// setMessage("alert alert-danger", "fa fa-4x fa-fw fa-pull-left fa-exclamation-triangle", "Invalid zip filename! Please try again.")
						// //return(false);
					// }
				// }
			// }	           
        // })
    // })
	
	
	// $('#downloadallID').click(function() {			

		// var datasetname = $('#datasetnameID').val();
		// var servertype = $('#servertypeID').val();
				
		// bootbox.prompt({
		  // title: "Zip filename",
		  // value: datasetname,
		  // callback: function(result) {
			  // if (result === null) {
			  // console.log("Cancelled");
			// } else {
				// // check if a valid filename					
				// if(checkFilename(result)){
					// $.ajax({
					// type: "POST",
					// url: "/downloadall",					
					// data: JSON.stringify({'datasetname': datasetname, 'servertype': servertype, 'zipfilename': result}),
					// contentType: "application/json; charset=utf-8",
					// dataType: "json",
					// success: function(data){
						// console.log(data);
						// },
					// failure: function(errMsg) {
						// alert(errMsg);
						// }
					// });				
				// }
				// else{
					// setMessage("alert alert-danger", "fa fa-4x fa-fw fa-pull-left fa-exclamation-triangle", "Invalid zip filename! Please try again.")
				// }
			// }
		  // }
		// });		

	// })	
	
});