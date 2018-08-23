$(document).ready(function(){
	addCheckboxFunctionality();
});
function addCheckboxFunctionality(){
	$('#tos').click(function(e){
  		e.preventDefault();
  		submit = document.getElementById("submit");
    	if (this.checked == true) submit.disabled = false;
    	else submit.disabled = true;
  	})
}
