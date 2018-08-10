(function($){ 
// When we're using HTTPS, use WSS too.
var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
var chatsock = new ReconnectingWebSocket(ws_scheme + '://' + window.location.host + "/ws" + window.location.pathname);

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
print('hooked')
$("#chatform").on("submit", function(event) {
    event.preventDefault()
    var message = {
        handle: $('#handle').val(),
        message: $('#message').val(),
    }
    chatsock.send(JSON.stringify(message));
    $("#message").val('').focus();
    return false;
});
})(jQuery);