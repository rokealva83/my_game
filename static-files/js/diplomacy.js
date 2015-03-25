/**
 * Created by tadej on 24.03.15.
 */


$(document).ready(function () {
    $('a.answer img').hover(function () {
            srcImg = $(this).attr('src');
            $(this).attr('src', '/static/images/mail/answer_active.png');
        },
        function () {
            $(this).attr('src', srcImg);
        });

    $('a.forward img').hover(function () {
            srcImg = $(this).attr('src');
            $(this).attr('src', '/static/images/mail/forward_active.png');
        },
        function () {
            $(this).attr('src', srcImg);
        });

    $("input.remove").hover(function () {
            srcImg = $(this).attr('src');
            $(this).attr('src', '/static/images/mail/remove_active.png');
        },
        function () {
            $(this).attr('src', srcImg);
        });

    $('a.view img').hover(function () {
            srcImg = $(this).attr('src');
            $(this).attr('src', '/static/images/mail/plus_n.png');
        },
        function () {
            $(this).attr('src', srcImg);
        });
})