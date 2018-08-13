
function setupChatRoom(handle){
    // When we're using HTTPS, use WSS too.
    var room_id = Number($('#party-room-id').text())
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    var chatsock = new ReconnectingWebSocket(ws_scheme + '://' + window.location.host + "/ws/events/?room_id=" + room_id );

    chatsock.onmessage = function(message) {
        var data = JSON.parse(message.data);
        var chat = $("#chat")
        var ele = $('<div class="col-xs-12"></div>')

        ele.append(
            $("<p></p>").text(data.timestamp)
        )
        ele.append(
            $("<p></p>").text(data.handle)
        )
        ele.append(
            $("<p></p>").text(data.message)
        )
        
        chat.append(ele)
    };
    $("#chatform").on("submit", function(event) {
        event.preventDefault()
        var message = {
            handle: room_id,
            message: $('#message').val(),
        }
        console.log(message)
        chatsock.send(JSON.stringify(message));
        $("#message").val('').focus();
        return false;
    });
}
