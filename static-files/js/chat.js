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
                var mess = response.result;
                for (i = 1; i < mess.length; i++) {
                    var message = mess[i];
                    var delete_id = message.id - 39;
                    var first_message = $('#ground p:first').attr('id')
                    if (delete_id == first_message) {
                        $('#ground p:first').remove()
                    }
                    $('#ground').append('<p class="message" id="' + message.id + '"><b>' + message.user + '</b>(' + message.time + '):' + message.text + '</p>')
                }
            }
        );

        var user_id = $('.user_online:last').attr('id');
        if (user_id == undefined) {
            user_id = 1
        }
        $.post('/update_user',
            {
                id: user_id
            },
            function (response) {
                var user = response.result;
                if (user != undefined) {
                    for (i = 0; i < user.length; i++) {
                        var user_online = user[i];
                        $('#user_online').append('<p id="' + user_online.id + '" class="user_online"> <b>' + user_online.user + '</b></p>')
                    }
                }
            }
        );
    }
    , 1000);



function send_message() {
    var user = document.getElementById('user').value;
    var text = document.getElementById('text').value;

    xhttp = new XMLHttpRequest();
    xhttp.open('POST', 'send_message', true);
    xhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    var message = 'user=' + user + '&text=' + text;
    xhttp.send(message);
    $('#text').each(function () {
        $(this).val('')
    });

}

$(document).ready(function () {
    $("#ground .touch").click(function () {
        var name = $(this).text();
        $('#text').each(function () {
            $(this).val(name + ',');
        });
    });
});

//Почемуто удаляет не то что надо. Мигает.

setInterval(
    function delete_user() {
        $.post('/user_delete')}, 5000);

setInterval(
    function online_user() {
        $("#user_online p").each(function () {
            var user_id = $(this).attr('id');
            var online_user = 1;

            $.post('/delete_user_update',
                {
                    id: user_id
                },
                function (response) {
                    online_user= response.result;
                    if (online_user == 0) {
                        $('#user_online p#'+user_id).remove();
                    }
                });
        });
    }
    , 5000);