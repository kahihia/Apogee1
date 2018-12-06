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
              input = jQuery('<input size="6" type="text" id="password_token" name="password_token" value="" maxlength="6"><p></p>');
              jQuery('#div_auth_key').append(input);
              input = jQuery('<input type="submit" value="Token" class="btn btn-primary-new ml-3" id ="token_btn">');
              jQuery('#div_auth_key').append(input);
              addTokenFunctionality();
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

function addTokenFunctionality(){
  $('#token_btn').click(function(e){
      e.preventDefault();
      token = document.getElementById('password_token').value;

    let passwordResethUrl = '/api/' + token +'/token/';
      $.ajax({
        method: 'GET',
          url: passwordResethUrl,
          success: function(data){
            if(data.token_found==true){
              $('#authentication_confirmation').text("  Enter in a new password");
              jQuery('#password_token').remove();
              jQuery('#token_btn').remove();
              new_line = jQuery('<p></p>')
              input = jQuery('<input type="password" name="password"> id ="password1"');
              jQuery('#div_auth_key').append(input);
              jQuery('#div_auth_key').append(new_line);
              input = jQuery('Enter it again');
              jQuery('#div_auth_key').append(input);
              input = jQuery('<input type="password" name="password"> id= "password2"');
              jQuery('#div_auth_key').append(input);
              jQuery('#div_auth_key').append(new_line);
              input = jQuery('<input type="submit" value="Submit" class="btn btn-primary-new ml-3" id ="password_btn">');
              jQuery('#div_auth_key').append(input);
            }
            else{
              $('#authentication_confirmation').text("  The token submitted is incorrect");   
            }
          }, 
          error: function(data){

          }
      })
  })
}