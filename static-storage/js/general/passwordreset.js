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
      			if(data.account_found==true){
      				$('#authentication_confirmation').text("	We have sent you a password reset token");
        			console.log("True");
      			}
      			else{
      				$('#authentication_confirmation').text("	We could not find an account with that email address");
        			console.log("False");      
      			}
      		}, 
      		error: function(data){

      		}
    	})
	})
}