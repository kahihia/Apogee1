// $('input[type=number]').on('mouseup keyup', function () {
//   $(this).val(Math.min(10, Math.max(2, $(this).val())));
// });



$(document).ready(function(){
	alert("Here I am")
	addCheckNumber();
})

function addCheckNumber(){
	$('#paypal-input').on('mouseup keyup', function () {
		$(this).val(Math.min(1000, Math.max(10, $(this).val())));
	});
}