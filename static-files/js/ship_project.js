/**
 * Created by tadej on 04.03.15.
 */


(function ($) {
    $(document).ready(function () {
        $('select').change(function () {
            $("select option:selected").each(function (e) {
                var name = $(this).text();
                var data = $(this).data();
                $(".hull").empty().append(name + '<br>');
                $.each(data, function (key, val) {
                    $(".hull").append(key + ": " + val + "<br>");
                });
            });
        });
    });
})(jQuery);