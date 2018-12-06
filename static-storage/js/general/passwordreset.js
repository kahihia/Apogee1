$(document).ready(function(){
	addAuthenticationFunctionality();
})

function addAuthenticationFunctionality(){
	$('#email_btn').click(function(e){
  		e.preventDefault();
  		email = document.getElementById('email').value;

		let passwordResethUrl = '/api/' + email +'/password_reset/';
    	$.ajax({
     		method: 'GET',
      		url: passwordResethUrl,
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