
$(document).ready(function(){
	addAuthenticationFunctionality();
	alert("hey");
})

function addAuthenticationFunctionality(){
	$('authenticate_btn').click(function(e){
  		e.preventDefault();
  		alert("LOL");
  	})
 }