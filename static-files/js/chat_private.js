/**
 * Created by tadej on 30.04.15.
 */

setInterval(
function update_private() {
    $.post('/update_private_message', {},
        function (response) {
            var message = response.result;
            message = message[0]
            $('.private_message_text').append('<p><b>' + message.user + '</b></p>'+'<p disabled rows=4 style="width: 210px; overflow-wrap: break-word;">' + message.text + '</p>').css('display', 'block').animate({
                opacity: 1,
                top: '20%'
            }, 200);
        }
    );
    $('.close').click(function () {
        $('.private_message_text').animate({opacity: 0, top: '0%'}, 200, function () {
                $(this).css('display', 'none');
            }
        );
        $('.private_message_text p').remove();
    });

}
, 2000);


$(document).ready(function () {
    $("#user_online .user_online").click(function (event) {
        var name = $(this).find('b').text();
        $('#adress p').remove()
        var private_user_id = $(this).attr('id')
        event.preventDefault();
        $('.overlay').fadeIn(400, function () {
            $('.rent_window').css('display', 'block').animate({opacity: 1, top: '20%'}, 200);
        });
        $('#adress').append('<p id="' + private_user_id + '" style="text-align: center;  margin-top: 20px; margin-bottom: -15px;"><b>' + name + '</b></p>')
    });

    $('.close, .overlay').click(function () {
        $('.rent_window').animate({opacity: 0, top: '0%'}, 200, function () {
                $(this).css('display', 'none');

            }
        );
        $('#text_private').each(function () {
            $(this).val('')
        });
    });
});


function send_private_message() {
    var user = $('#adress p').attr('id');
    var text = document.getElementById('text_private').value;
    xhttp = new XMLHttpRequest();
    xhttp.open('POST', 'send_private_message', true);
    xhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    var private_message = 'user=' + user + '&text=' + text;
    xhttp.send(private_message);
    $('#text_private').each(function () {
        $(this).val('');
        $('#adress p').remove()
        $('.rent_window').animate({opacity: 0, top: '0%'}, 200, function () {
                $(this).css('display', 'none');
                $('.overlay').fadeOut(400);
            }
        );
    });
}