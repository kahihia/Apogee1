
$(document).ready(function(){
	addAuthenticationFunctionality();
})

function addAuthenticationFunctionality(){
	$('#authenticate_btn').click(function(e){
  		e.preventDefault();
  		auth_key = document.getElementById('auth_key').value;

		let authUrl = '/api/' + auth_key +'/authorization/';
    	$.ajax({
     		method: 'GET',
      		url: authUrl,
      		success: function(data){
      			$('#authentication_confirmation').text("Your account has been authorized");
        		console.log("True");
      		}, 
      		error: function(data){
      			$('#authentication_confirmation').text("We could not authorize your account");
        		console.log("False");      
      		}
    	})
	})
}