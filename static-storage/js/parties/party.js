function updateHashLinks(){
  // this is where the actual title and description are held
  // the span allows up to properly id the hashtags in the description
  // it will not highlight anf link a hashtag in the title
  $('.description').each(function(data){
    let hashtagRegex = /(^|\s)#([\w\d-]+)/g // pulls hashtags
    let usernameRegex = /(^|\s)@([\w\d-]+)/g // pulls user mentions
    let currentHtml = $(this).html()
    let newText;
    // the regex returns stuff before and after
    // the replace puts the tag in and then makes a link for the text
    newText = currentHtml.replace(hashtagRegex, '$1<a class="text-dark" href="/tags/$2/">#$2</a>')
    newText = newText.replace(usernameRegex, '$1<a class="text-dark" href="/profiles/$2/">@$2</a>')
    $(this).html(newText)
  })
}


function addRequestFunctionality(){
   $(document.body).on("click", '.requestBtn', function(e){
    e.preventDefault();
    alert("Requesting stuff");
   }
}

function addJoinFunctionality(){
  $(document.body).on("click", '.joinBtn', function(e){
    e.preventDefault();

    let this_ = $(this)
    // selector for the button. makes sure we have the event id 
    let partyID = this_.attr('data-id')
    let partyType = this_.attr('event-id')
    console.log("The party is "+partyType)
    // api endpoint
    let joinedUrl;
    if(partyType == 1 || partyType == 3||partyType==4){
      joinedUrl = '/api/events/' + partyID + '/join/'
    }
    else{
      let bid = document.getElementsByName("bid_amount")[0].value
      joinedUrl = '/api/events/' + partyID + '/join/'+ bid
    }
    if(partyType==4){
      let is_owner = document.getElementsByName("is_owner")[0].value
      console.log("RUTHEOWNER")
      console.log(is_owner)
    }
    
    // ajax accesses the api
    $.ajax({
      method: 'GET',
      url: joinedUrl,

      success: function(data){
        if(partyType == 1){
          document.getElementsByName("num_joined")[0].innerHTML = data.num_joined 
        }
        if(partyType == 2){
          document.getElementsByName("min_bid")[0].innerHTML = data.min_bid 
        }
        if(partyType == 3){
          document.getElementsByName("num_curr_winners")[0].innerHTML = 
          data.num_curr_winners 
        }
        if(data.error_message!=""){
          alert(data.error_message)
        }
        if(data.error_message == ''){
          this_.prop('disabled', true)
          this_.text('Joined')
        }
        console.log(this_)
        console.log(data.min_bid)
        location.reload();
        // the api handles updating the database 
      }, 
      error: function(data){
        console.log('error')
        console.log(data)
      }
    })
  })
}


// this is the favorite function. It wil be instrumental in enabling 
// users to track events as they progress.
// its built to trigger on click for any button with the correct class
function addStarFunctionality(){
  $('.starBtn').unbind("click")
  $('.starBtn').click(function(e){
    let this_ = $(this)
    var that = this_
    // selector for the button. makes sure we're starring the correct button
    let partyID = this_.attr('data-id')
    // api endpoint
    let starredUrl = '/api/events/' + partyID + '/star/'
    // ajax is what actually accesses the API
    $.ajax({
      method: 'GET',
      url: starredUrl,
      success: function(data){
        that.children('.fa-star').eq(0).toggleClass('grey-color')
        that.children('.fa-star').toggleClass('yellow-color')
        console.log(data)
      }, 
      error: function(data){
        console.log('error')
        console.log(data)
      }
    })
  })

}

// Adds report API call to report button
function addReportFunctionality(){
  $(document.body).on("click", '.reportBtn', function(e){
    e.preventDefault();
    let this_ = $(this);
    let partyID = this_.attr('data-id');
    let reportUrl = '/api/events/' + partyID + '/report/';
    $.ajax({
      method: 'GET',
      url: reportUrl,
      success: function(data){
        console.log("Successful Report");
      }, 
      error: function(data){
        console.log("Unsuccessful Report");      
      }
    })
  })
}





function getParameterByName(name, url) {
  if (!url) url = window.location.href;
  name = name.replace(/[\[\]]/g, "\\$&");
  let regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
    results = regex.exec(url);
  if (!results) return null;
  if (!results[2]) return '';
  return decodeURIComponent(results[2].replace(/\+/g, " "));
}