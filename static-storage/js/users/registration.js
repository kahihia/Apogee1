$(document).ready(function(){
	addCheckboxFunctionality();
});
function addCheckboxFunctionality(){
	$('#tos').change(function(e){
  		e.preventDefault();
  		submit = document.getElementById("submit");
  		submit_twitch = document.getElementById("submit_twitch")
    	if (this.checked == true) {
    		submit.disabled = false;
    		submit_twitch.disabled = false;
    	}
    	else {
        submit.disabled = true;
        submit_twitch.disabled = true;
      }
  	})
}
