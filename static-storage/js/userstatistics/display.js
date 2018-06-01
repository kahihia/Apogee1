$(document).ready(function(){
	let currSelected ="#general_btn";
	let fetchUrl = '/api/statistics/'
    .ajax({
	    url: fetchUrl, 
	    data: {
	      'q': query
	    },
	    method: 'GET', 
	    success: function(data){
	      // the .results is required because of our pagination
	      // it sets a new datagrouping outside of the data we're using
	      // to describe what the call retrieved
	      partyList = data.results

	      // if there are more pages in the API, the loadmore appears
	      if (data.next) {
	        nextPartyUrl = data.next
	      } else {
	        $('#loadmore').css('display', 'none')
	      }
	      // it then calls the parse to format them and updates the usernames and 
	      // and hashtags
	      parseParties()
	      updateHashLinks()
	    }, 
	    error: function(data){
	      console.log('error')
	      console.log(data)
	    }
  })



	$('#general_btn').click(function(e){
  		e.preventDefault();
  		fillSelected(this, "#general_btn");

  	})

	$('#lottery_btn').click(function(e){
		e.preventDefault();
		fillSelected(this, "#lottery_btn");
	})

	$('#bid_btn').click(function(e){
		e.preventDefault();
		fillSelected(this, "#bid_btn");
	})

	$('#buyout_btn').click(function(e){
		e.preventDefault();
		fillSelected(this, "#buyout_btn");

	})




// This Function grabs the html button, changes its class to reflect that
// it has been clicked (filling it) and then removing the filling on the
// previously clicked button
	function fillSelected(button, name){
		$(button).removeClass('btn btn-outline-secondary');
  		$(button).addClass('btn btn-secondary');
  		$(currSelected).removeClass('btn btn-secondary');
  		$(currSelected).addClass('btn btn-outline-secondary');
  		currSelected = name;
	}
});