
function setupChatRoom(room_id){
    // When we're using HTTPS, use WSS too.
    var room_id = Number($('#party-room-id').text())
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    var chatsock = new ReconnectingWebSocket(ws_scheme + '://' + window.location.host + "/ws/events/?room_id=" + room_id );

    chatsock.onopen = function () {
        console.log("Connected to chat socket");
    };
    chatsock.onclose = function () {
        console.log("Disconnected from chat socket");
    }

    chatsock.onmessage = function(message) {
        console.log(message)
        var data = JSON.parse(message.data);
        var chat = $("#chat")
        var ele = $('<div class="col-xs-12"></div>')

        ele.append(
            $("<p></p>").text(data.timestamp)
        )
        ele.append(
            $("<p></p>").text(data.room_id)
        )
        ele.append(
            $("<p></p>").text(data.message)
        )
        
        chat.append(ele)
    };
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
