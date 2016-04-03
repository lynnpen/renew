$(document).ready(function () {
    namespace = '/chat';
    var socket = io.connect('http://' + document.domain + ':' + location.port + namespace);
    $('form#emit').submit(function (event) {
        socket.emit('my event', {data: $('#m').val()});
        $('#m').val('');
        return false;
    });
    socket.on('my response', function (msg) {
        $('#messages').append($('<li>').text(msg.data));
        $('#box').scrollTop($('ul#messages').height());
    });
    socket.on('login', function (msg) {
        $('#status').text(msg.data);
    });
});
