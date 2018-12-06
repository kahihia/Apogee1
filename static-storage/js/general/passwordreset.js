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
              jQuery('#email').remove();
              jQuery('#email_btn').remove();
              input = jQuery('<input size="6" type="text" id="password_token" name="password_token" value="" maxlength="6">');
              jQuery('#div_auth_key').append(input);
              input = jQuery('<input type="submit" value="Token" class="btn btn-primary-new ml-3" id ="token_btn">');
              jQuery('#div_auth_key').append(input);
      			}
      			else{
      				$('#authentication_confirmation').text("	We could not find an account with that email address");   
      			}
      		}, 
      		error: function(data){

      		}
    	})
	})
}