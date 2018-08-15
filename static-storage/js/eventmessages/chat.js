var globalMessageIds = []

function setupChatRoom(){
    // When we're using HTTPS, use WSS too.
    var room_id = Number($('#party-room-id').text())
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    var chatsock = new ReconnectingWebSocket(ws_scheme + '://' + window.location.host + "/ws/events/?room_id=" + room_id );

    chatsock.onopen = function () {
        console.log("Connected to chat socket");
    }

    chatsock.onclose = function () {
        console.log("Disconnected from chat socket");
    }

    chatsock.onmessage = function(message) {
        appendMessage(JSON.parse(message.data))
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

function appendMessage(message) {
        globalMessageIds.push(message)
        var chat = $("#chat")
        var ele = $('<div class="col-xs-12"></div>')

        ele.append(
            $("<p class='message-timestamp'></p>").text(moment(message.timestamp).local().format('HH:mm:ss MM-DD-YY'))
        )
        ele.append(
            $("<p class='message-username'></p>").text(message.username)
        )
        ele.append(
            $("<p class='message-message'></p>").text(message.message)
        )
        
        chat.append(ele)
        var chatBox = document.getElementById("chat");
        chatBox.scrollTop = chatBox.scrollHeight;
}

function getMessages(num, skip, callback){
    /*  Gets messages from the api, 
        * num is the number of messages you want
        * skip is the offset from a message
        - setting num to false gets latest */
    var room_id = Number($('#party-room-id').text())
    var payload = {
        "room_id": room_id,
        "skip": skip,
        "num": num
    }

    $.ajax({
        type: "POST",
        url: "/api/messages/",
        headers: {'X-CSRFToken': Cookies.get("csrftoken")},
        data: payload
    })
    .done(function( data ) {
        callback(data.messages)
    });
}
