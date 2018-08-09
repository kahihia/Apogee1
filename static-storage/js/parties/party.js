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

// this allows search along hashtags. its called upon creation
// could be useful for categorization
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

function addJoinFunctionality(){
  $(document.body).on("click", '.joinBtn', function(e){
    e.preventDefault()

    let this_ = $(this)
    // selector for the button. makes sure we have the event id 
    let partyID = this_.attr('data-id')
    let partyType = this_.attr('event-id')
    console.log("The party is "+partyType)
    // api endpoint
    let joinedUrl;
    if(partyType == 1 || partyType == 3){
      joinedUrl = '/api/events/' + partyID + '/join/'
    }
    else{
      let bid = document.getElementsByName("bid_amount")[0].value
      joinedUrl = '/api/events/' + partyID + '/join/'+ bid
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
          this_.text(joined)
        }
        console.log(this_)
        console.log(data.min_bid)
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
  $(document.body).on("click", '.starBtn', function(e){
    e.preventDefault()
    let this_ = $(this)
    // selector for the button. makes sure we're starring the correct button
    let partyID = this_.attr('data-id')
    // api endpoint
    let starredUrl = '/api/events/' + partyID + '/star/'
    // ajax is what actually accesses the API
    $.ajax({
      method: 'GET',
      url: starredUrl,
      success: function(data){
        // the api handles updating the database and the method below
        // updates the color, so nothing happens on success
      }, 
      error: function(data){
        console.log('error')
        console.log(data)
      }
    })
  })
// this controls the display color of the favorite button
// its linked to a different class to ensure nothing wierd happens 
// with the click trigger
  $(document.body).on("click", '.fa-star', function(e){
    e.preventDefault()
    let this_ = $(this)
    // one of these classes is activated by the formatting below, 
    // so the two toggles are never on at the same time
    this_.toggleClass('grey-color')
    this_.toggleClass('yellow-color')
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