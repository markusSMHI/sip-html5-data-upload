// FROM UPLOAD.JS


		// var activeUploads = $('#fileupload').fileupload('active');		
		
		// var files = $('#fileupload').each(function () {
			// $(this).fileupload({
				// fileInput: $(this).find('input:file')
			// });
		// });		
		
		// $('tbody.files tr').each(function(i, e) {
			// //according to @Brandon's comment it's now p.name
			// var name = $(e).find('p.name').text(); 
			// console.log(e)		
		// });
		
        //var fileUploadButtonBar = this.element.find('.fileupload-buttonbar'),			
		// bootbox.prompt({
		  // title: "Please set the name of the zip file",
		  // value: "zipped",
		  // callback: function(result) {
			// if (result === null) {			  
			  // console.log("No name given, using default name");
			  // zip(value);
			  // } else {			  
			  // zip(value);
			  // console.log(value);						  
			// }
		  // }
		// });		

		

// function validateForm() {	
	
    // var datasetname = document.getElementById("datasetnameID").value;	
	// var re = /^[a-zA-Z].*/;	
    // if (re.test(datasetname))
	// {		
        // return true;
    // } else{	
	
		// setMessage("alert alert-warning", "fa fa-4x fa-fw fa-pull-left fa-exclamation-triangle", "Dataset name is not valid. The name should start with a letter and may not contain spaces or special characters. Please try again.");
        // return false;
    // }
// }



	
function validateForm(){	
	
	//return true;
	
	//e.preventDefault();
	
	// bootbox.prompt({
		// title: "Zip filename",
		// value: $('#datasetnameID').val(),
		
		// callback: function(result) {
			// if (result === null) {
				// console.log("Cancelled");
				// return false;
			// } else {
				// // check if a valid filename					
				// if(checkFilename(result)){
					// $('#zipfilenameID').val(result);  
					// console.log("valid zipfilename");
					// //$('#downloadallForm').submit();
					// return true;
				// }
				// else{
					// setMessage("alert alert-danger", "fa fa-4x fa-fw fa-pull-left fa-exclamation-triangle", "Invalid zip filename! Please try again.")
					// return false;
				// }
			// }
		// }	           
	// })
  
}


// FROM DOWNLOAD
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



// FROM SELECTSERVER
	// $( "#datasetnameID" ).click(function() {	
		// var message = "The dataset name should be as specific as possible and contain the variable and source of data (in that order). The name must start with a letter and may not contain spaces or special characters.";
		// setMessage("alert alert-success", "fa fa-4x fa-fw fa-pull-left fa-info-circle", message);
	// });		