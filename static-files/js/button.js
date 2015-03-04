/**
 * Created by tadej on 30.01.15.
 */

$(document).ready(function () {

    $(".menu_button").mouseover(function () {
        $(this).css("color", "white");
        $(this).css("background", "#343434");
        $(this).animate({marginLeft:"20px", boxShadow:'10px 10px 15px #191919'}, 500)
    });
    $(".menu_button").mouseout(function () {
        $(this).css("color", "black");
        $(this).css("background", "#616161");
        $(this).animate({marginLeft:"0px", boxShadow: "15px"}, 500)
    });

    $(":contains('Information')").click(function(){
        $(this).slideDown(1000);
    });
});


