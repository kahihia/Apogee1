function loadPartyListContainer(partyContainerID){
  renderPartyList(partyContainerID);
  addStarFunctionality();
}

function renderPartyList(partyContainerID){
  // this is the set of events in the api
  let query = getParameterByName('q');
  let partyList = [];
  // this links to the following page in the api
  let nextPartyUrl;
  // this is the selector for where we're putting the party info
  let partyContainer;
  if (partyContainerID){
    partyContainer = $('#' + partyContainerID)
  } else {
    partyContainer = $('#party-container')
  }
  // url that allows us to get the api data. second is the default
  // data url should be defined in the container specified in the HTML
  let initialUrl = partyContainer.attr('data-url') || '/api/events/';
  // these are repeatedly used, so they've been converted to variables
  // some should eventually be references to a dictionary
  let star_active = '<i class="fa fa-star yellow-color" aria-hidden="true"></i>';
  let star_inactive = '<i class="fa fa-star grey-color" aria-hidden="true"></i>';
  let free = 'FREE';
  let joined = '';
  let joined_lottery = 'Entry Purchased';
  let joined_bid = 'Bid submitted';
  let joined_buy = 'Event Purchased';
  let lottery_icon = '<i class="fas fa-ticket-alt grey-color" data-toggle="tooltip" data-placement="top" title="Lottery"></i>';
  let bid_icon = '<i class="fas fa-gavel grey-color" data-toggle="tooltip" data-placement="top" title="Auction"></i>';
  let buy_icon = '<i class="fa fa-donate grey-color" data-toggle="tooltip" data-placement="top" title="Buy Now"></i>';
  let closed_icon = '<i class="fas fa-ban grey-color"></i>';
  let check_icon = '<i class="fas fa-check-circle"></i>';

  fetchParties();
  $('#loadmore').click(function(event){
    event.preventDefault()

    // assuming there are more events, get and show them
    if (nextPartyUrl) {
      fetchParties(nextPartyUrl)
    }
  })

  // this calls to the API and gets the party data for the thumbnails
  function fetchParties(url){
    let fetchUrl;

    // if there isnt a url passed, its the first api page, 
    // which is just events from following
    if (!url) {
      fetchUrl = initialUrl
    } else {
      fetchUrl = url
    }
    // actual call to api
    $.ajax({
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
          if (data.next.includes('https:')) {
            nextPartyUrl = data.next
          } else {
            nextPartyUrl = data.next.replace('http', 'https')
          }
          $('#loadmore').css('display', 'inline-block')
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
  }

  function parseParties(){
    // partylist should be filled with parties from the fetch call
    if (partyList == 0) {
      partyContainer.append("<div class='text-center p5'> No results found ☹</div>")
    } else {
      // make global variable, make responsive
      handSize = 3
      // this iterates through the number of hands in the party list, 
      // then through the number of cards per hand, then formats the 
      // party and adds it to the HTML. each hand is its own div
      // for (let deck = 0; deck < partyList.length; deck += handSize) {
      //   let deckHTML = '<div class="card-deck mb-4">'
      //   for (let card = 0; card < handSize; card++) {
      //     let cardIndex = deck + card
      //     if (cardIndex < partyList.length) {
      //       let partyValue = partyList[cardIndex]
      //       let partyFormattedHtml = formatParty(partyValue)
      //       deckHTML = deckHTML + partyFormattedHtml
      //     }
      //   }
      //   deckHTML = deckHTML + '</div>'
      //   partyContainer.append(deckHTML)
      // }
      for (let index=0; index<partyList.length; index+=1) {
        let partyValue = partyList[index]
        let partyFormattedHtml = formatParty(partyValue)
        partyContainer.append(partyFormattedHtml)
        addStarFunctionality()
      }
    }
  }


  function formatParty(partyValue){
    // this sets the star color depending on whether or not 
    // its been starred by the request user
    let verb = star_inactive
    if (partyValue.did_star){
      verb = star_active
    }

    // this sets the text version of the price
    let price = '$' + partyValue.cost
    if (partyValue.cost == 0) {
      price = free
    }
    if (partyValue.event_type == 2){
      price = '$' + partyValue.minimum_bid
    }

    // this checks the event type and sets the correct icon
    let type_icon = ''
    if (partyValue.event_type == 1) {
      type_icon = lottery_icon
    } else if (partyValue.event_type == 2) {
      type_icon = bid_icon
    } else if (partyValue.event_type == 3) {
      type_icon = buy_icon
    }

    // adds small closed icon if event is closed. the tooltip explains the icon
    let closed_display = ''
    if(partyValue.user.is_verified){
      check_icon = '<i class="fas fa-check-circle"></i>';
    }
    else{
      check_icon = '';
    }
    if (!partyValue.is_open) {
      closed_display = '<span class="float-right" data-toggle="tooltip" data-placement="top" title="Event Closed">' + closed_icon + '</span>'
    }
    // this is the thumbnail formatting. its built on the
    // card model from bootstrap. it has a top image, a body section 
    // for the title and description, and a footer for name, time, 
    // event type, and star
    let container =  
    '<div class="card home-card mr-4">' + 
      '<a class="text-light" style="height: 170px" href="/events/' + partyValue.id + '"">' +
        '<div class="card-img-top" style="background-image: url('+ partyValue.thumbnail_url + ')"></div>' + 
      '</a>' +
      '<div class="card-body">' + 
        '<a class="text-light" href="/events/' + partyValue.id + '" style="text-decoration: none;">' +
          '<h5 class="card-title">' + partyValue.short_title + closed_display + '</h5>' +
        '</a>' +
      '</div>' + 
      '<div class="card-footer">' + 
        '<small class="text-muted">With ' + 
          '<a class="text-light" href="' + partyValue.user.url + '">'+ partyValue.user.username + 
          '<span> ' + check_icon + '</span></a>' + 
          '<span class="float-right">' + price + ' ' + type_icon + '</span>' +
          '<br>' + partyValue.party_time_display + 
        '</small>' + 
        '<span class="float-right">' + 
          '<a class="starBtn text-dark" data-id="' + partyValue.id + '">' + verb + '</a>' + 
        '</span>' + 
      '</div>' + 
    '</div>'

    // just return it immediately
    return sanitizeHtml(container, {
                                      allowedClasses: { 'div': [ 'card','home-card', 'mr-4', 'col-xs-12','col-md-4','col-lg-2','col-xl-2', 'col-xs-12', 'col-md-3', 'col-lg-3',
                                                                  'text-light', 'card-img-top', 'card-body', 'card-title', 'card-text', 
                                                                  'card-footer', 'text-muted', 'float-right', 'starBtn', 'text-dark'],
                                                        'p': [ 'card','home-card','col-xs-12','col-md-4','col-lg-2','col-xl-2',
                                                                  'text-light', 'card-img-top', 'card-body', 'card-title', 'card-text', 
                                                                  'card-footer', 'text-muted', 'float-right', 'starBtn', 'text-dark'],
                                                        'span': [ 'card','home-card','col-xs-12','col-md-4','col-lg-2','col-xl-2',
                                                                  'text-light', 'card-img-top', 'card-body', 'card-title', 'card-text', 
                                                                  'card-footer', 'text-muted', 'float-right', 'starBtn', 'text-dark'],
                                                        'small': [ 'text-muted'],
                                                        'img': [ 'card-img-top'],
                                                        'i': [ 'fa', 'fa-sta', 'yellow-color', 'grey-color', 'fas', 'fa-ticket-alt', 
                                                                'fa-gavel', 'fa-donate', 'fa-ban', 'fa-star', 'fa-check-circle'],
                                                        'h5': [ 'card','home-card','col-xs-12','col-md-4','col-lg-2','col-xl-2',
                                                                  'text-light', 'card-img-top', 'card-body', 'card-title', 'card-text', 
                                                                  'card-footer', 'text-muted', 'float-right', 'starBtn', 'text-dark'],
                                                        'a': [ 'card','home-card','col-xs-12','col-md-4','col-lg-2','col-xl-2',
                                                                  'text-light', 'card-img-top', 'card-body', 'card-title', 'card-text', 
                                                                  'card-footer', 'text-muted', 'float-right', 'starBtn', 'text-dark']},
                                      allowedTags: [ 'p', 'em', 'strong', 'div', 'a', 'img', 'span', 'h5', 'small', 'i', 'br' ],
                                      allowedAttributes: {
                                                            '*': [ 'href', 'align', 'alt', 'center', 'bgcolor', 'data-*', 'src', 'style', 'aria-*', 'title']
                                                        }
                                    })
  }

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
}

  function parseSingle(){
    let partyValue = partyList[0]

    let partyFormattedHtml = formatSingle(partyValue)
    partyContainer.append(partyFormattedHtml) 
  }
 // this accesses the event data for a single detail event
  function fetchSingle(fetchOneId){
    // leading slash appends it to the base url. 
    // no leading slash sends it to the url of the page its on
    // which would be /events/id/api/events/id 
    let fetchDetailUrl = '/api/events/' + fetchOneId + '/'
    // actual call to api
    $.ajax({
      url: fetchDetailUrl, 
      method: 'GET', 
      success: function(data){
        console.log(data)
        partyList = data.results
        parseSingle()
        updateHashLinks()
      }, 
      error: function(data){
        console.log('error')
        console.log(data)
      }
    })
  }
