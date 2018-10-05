
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
      			if(data.authenticated==true){
      				$('#authentication_confirmation').text("	Your account has been authorized");
        			console.log("True");
      			}
      			else{
      				$('#authentication_confirmation').text("	We could not authorize your account");
        			console.log("False");      
      			}
      		}, 
      		error: function(data){

      		}
    	})
	})
}