
$(document).ready(function(){
	addAuthenticationFunctionality();
})

function addAuthenticationFunctionality(){
	$('#authenticate_btn').click(function(e){
  		e.preventDefault();
  		alert(document.getElementById('auth_key').value);
 //  		let this_ = $(this);
 //    	let partyID = this_.attr('data-id');
 //    	let reportUrl = '/api/events/' + partyID + '/report/';
 //    	$.ajax({
 //     		method: 'GET',
 //      		url: reportUrl,
 //      		success: function(data){
 //        		console.log("Successful Report");
 //      		}, 
 //      		error: function(data){
 //        		console.log("Unsuccessful Report");      
 //      		}
 //    	})
	})
}