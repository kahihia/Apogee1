var globalMessageIds = []

function setupChatRoom(){
    // When we're using HTTPS, use WSS too.
    var room_id = Number($('#party-room-id').text())
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    var chatsock = new ReconnectingWebSocket(ws_scheme + '://' + window.location.host + "/ws/events/?room_id=" + room_id );

    chatsock.onopen = function () {
        console.log("Connected to chat socket");
    }

    chatsock.onclose = function (e) {
        console.log("Disconnected from chat socket", e);
    }

    chatsock.onmessage = function(rawMessage) {
        var message = JSON.parse(rawMessage.data)
        if (!message.error) {
            try{
                appendMessage(JSON.parse(message))
            } catch(e) {
                appendMessage(message)
            }
        } else {
            alert("Must be logged in to post a message")
        }
    }

    $("#chatform").on("submit", function(event) {
        event.preventDefault()
        var message = {
            command: 'send',
            room_id: room_id,
            message: $('#message').val(),
        }
        chatsock.send(JSON.stringify(message));
        $("#message").val('').focus();
        return false;
    });
}

function writeLetter() {
    var letter = ["Hello, is it you? Is it actually you? You've come to my website?",
                    "GTFO. Unless its you NSA, like really didn't mean that.",
                    "Please dont take away all my internet rights again",
                    "IS IT FRANCE? IS IT FRANCE NSA? Jk you guys are alright",
                    "You have a hard job but damn this whole tapping everyone for signals seems,",
                    "like a step in the wrong direction.",
                    "Like I know the russians have all our routers backdoored",
                    "even in that super coldwar, WAIT FOR MY SIGNAL, SLEEPER",
                    "kinda way but still I think the mass collection of metadata",
                    "is a step to far, at least have a legal process to be able to access it",
                    "some level of transparency, I'm willing to sacrifice some safety for that.",
                    "So that at least some can be held accountable.",
                    "Peace."]
    $("#message").css('display', 'none')
    for (var i = 0; i < letter.length; i++) {
        var line = letter[i]
        appendMessage({message: line})
    }
}

function appendMessage(message, prepend) {
        var username = sanitizeHtml(message.username)
        var message = sanitizeHtml(message.message)
        globalMessageIds.push(message)
        var chat = $("#chat")
        var ele = $('<div class="col-xs-12"></div>')

        var messageField = $("<div class='message-container'></div")

        var messageText = $("<p class='message'></p>")
        messageText.append($("<span class='message-username'></span>").text(username + ' : '))
        messageText.append($("<span class='message-message'></span").text(message))

        messageField.append($("<p class='message-timestamp'></p>").text(moment(message.timestamp).local().format('hh:mm a MM-DD')))
        messageField.append(messageText)
        ele.append(messageField)
        
        if (prepend) {
            chat.prepend(ele)
        } else {
            chat.append(ele)
        }
}

var messagePaginatorGlobal = null

function checkSpawnGetMore(){
    // Check if more messages
    console.log(messagePaginatorGlobal)
    if (messagePaginatorGlobal != null) {
        $("#histLoad").css('display','block')
        $("#histLoad").unbind('click')
        $("#histLoad").click(function(){
            getMessages(messagePaginatorGlobal, function(messages){
                messages.reverse()
                messages.forEach(function(m){
                  appendMessage(m, true)
                });
            })
        })
    } else {
        $("#histLoad").css('display','none')
        return
    }
}

function getCookie(name) {
  var value = "; " + document.cookie;
  var parts = value.split("; " + name + "=");
  if (parts.length == 2) return parts.pop().split(";").shift();
}

function getMessages(url, callback){
    /*  Gets messages from the api, 
        * num is the number of messages you want
        * skip is the offset from a message
        - setting num to false gets latest */
    var room_id = Number($('#party-room-id').text())
    $.ajax({
        type: "GET",
        url: url || "/api/messages/" + room_id,
          headers: {
            "X-CSRFToken": getCookie("csrftoken")
          },
    })
    .done(function( data ) {
        messagePaginatorGlobal = data.next
        checkSpawnGetMore()
        callback(data.results.reverse(), true)
    }).fail(function(e){
        console.log(e)
    })
}
