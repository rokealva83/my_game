/**
 * Created by tadej on 04.03.15.
 */


/**(function ($) {
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
})(jQuery);*/

(function ($) {
    $(document).ready(function () {
        $('select').change(function () {
            $(this).find('option:selected').each(function () {

                var name = $(this).text();

                var selName = $(this).parent('select').attr('name');

                var selId = $(this).parent('select').attr('id');

                var block = $(this).parents('li').find('label').text();

                var res_block = $('#block_design_left');

                if (/side/.test(selName)) {

                    var needId = $(this).parent('select').prev().attr('id');
                    var ind = $(this).index();

                    if (ind >= 4) {
                        ind += 1;
                    }
                    var flag = true

                } else {
                    var flag = false;
                }

                if (flag == true) {

                    var ct = res_block.find('li').find('.' + needId).detach();
                    res_block.find('li').eq(ind).append(ct);

                } else {

                    if (res_block.find('ul li:gt(0)').find('.' + selId).length > 0) {
                        var mainInfo = res_block.find('li:gt(0)').find('.' + selId).parent();

                    } else {

                        var mainInfo = res_block.find('ul li:first');
                    }

                    if (mainInfo.children('.' + selId).length == 0) {

                        mainInfo.append('<div class="' + selName + ' ' + selId + '"><h4>' + block + '</h4></div>');

                    } else {

                        $(mainInfo.children('.' + selId)).empty();

                    }

                    mainInfo.find('.' + selId).append('<p><strong>' + name + '</strong></p>');

                    var data = $(this).data();

                    $.each(data, function (key, val) {
                        mainInfo.find('.' + selId).append(key + ": " + val + "<br>");
                    });

                }
            });
        });
    });
})(jQuery);