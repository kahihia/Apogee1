$(document).ready(function(){
	let currSelected ="#general_btn"

	$('#general_btn').click(function(e){
  		e.preventDefault();
  		fillSelected(this, "#general_btn")
  		// $(this).removeClass('btn btn-outline-secondary')
  		// $(this).addClass('btn btn-secondary')
  		// $(lastClick).removeClass('btn btn-secondary')
  		// $(lastClick).addClass('btn btn-outline-secondary')
  		// lastClick = "#general_btn"

  	})

	$('#lottery_btn').click(function(e){
		e.preventDefault();
		fillSelected(this, "#lottery_btn")
		// $(this).removeClass('btn btn-outline-secondary')
  // 		$(this).addClass('btn btn-secondary')
  // 		$(lastClick).removeClass('btn btn-secondary')
  // 		$(lastClick).addClass('btn btn-outline-secondary')
  // 		lastClick = "#lottery_btn"
	})

	$('#bid_btn').click(function(e){
		e.preventDefault();
		fillSelected(this, "#bid_btn")
		// $(this).removeClass('btn btn-outline-secondary')
  // 		$(this).addClass('btn btn-secondary')
  // 		$(lastClick).removeClass('btn btn-secondary')
  // 		$(lastClick).addClass('btn btn-outline-secondary')
  // 		lastClick = "#bid_btn"
	})

	$('#buyout_btn').click(function(e){
		e.preventDefault();
		fillSelected(this, "#buyout_btn")

	})

	function fillSelected(button, name){
		$(button).removeClass('btn btn-outline-secondary')
  		$(button).addClass('btn btn-secondary')
  		$(currSelected).removeClass('btn btn-secondary')
  		$(currSelected).addClass('btn btn-outline-secondary')
  		console.log(currSelected)
  		currSelected = name
	}
});