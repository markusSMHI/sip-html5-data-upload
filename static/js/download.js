


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
		$('#messagetype').removeClass().addClass(messagetype);
		$('#messagefa').removeClass().addClass(messagefa);
		$('#messagetext').text(messagetext);
	}
		catch(err) {
			console.log(err.message);
	}
}
