// $('input[type=number]').on('mouseup keyup', function () {
//   $(this).val(Math.min(10, Math.max(2, $(this).val())));
// });



$(document).ready(function(){
	addCheckNumber();
})

function addCheckNumber(){

	$('#paypal-input').on('mouseup keyup', function () {
		// milisecondDelay = 500
		// milisecondDelay += Date.now();
  //  		while(Date.now() < milisecondDelay){}
		$(this).val(Math.min(1000, Math.max(10, $(this).val())));
	});
}