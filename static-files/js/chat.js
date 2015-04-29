/**
 * Created by tadej on 29.04.15.
 */

setInterval(
    function update() {
        var id = $('.message:last').attr('id');

        $.post('/update_message',
            {
                id: id
            },
            function (response) {
                var mess = response.result
                for (i = 1; i < mess.length; i++) {
                    var message = mess[i];
                    var delete_id = message.id - 39
                    var first_message = $('#ground p:first').attr('id')
                    if (delete_id == first_message) {
                        $('#ground p:first').remove()
                    }
                    $('#ground').append('<p class="message" id="' + message.id + '"><b>' + message.user + '</b>: ' + message.text + '</p>')
                }
            }
        );
    }
    , 500)


function send_message() {
    var user = document.getElementById('user').value;
    var text = document.getElementById('text').value;

    xhttp = new XMLHttpRequest();
    xhttp.open('POST', 'send_message', true);
    xhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    var message = 'user=' + user + '&text=' + text;
    xhttp.send(message);

}

