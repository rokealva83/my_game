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
        //записываем блоки с данными для быстрого обращения
        var res_block = $('#block_design_left .hull li');

        //Функция определения селектора сторон
        function checkSide(index) {
            if (index) {
                return true;
            } else {
                return false;
            }
        }

        //Функция переноса информации по сторонам
        function setSide(value, id, name) {
            //Если индекс больше или равен 4, добавляем +1
            if (value >= 4) {
                value++;
            }
            //Проверяем наличие заголовка и совпадение в нём текста
            //если нет совпадений по критериям
            if (res_block.eq(value).find('h5:visible').text() != name && res_block.eq(value).find('h5:visible').length == 0) {
                //Клонируем заголовок с блока переноса
                var catTitle = res_block.find('#' + id).siblings('h5').clone();
                //Вставляем в блок, в который перенос
                res_block.eq(value).find('h4').after(catTitle);
            }
            //Проверяем, есть ли ещё блоки с данными
            if (res_block.find('#' + id).siblings('div').length == 0) {
                //Если нет - удаляем заголовок
                res_block.find('#' + id).siblings('h5').remove();
                //Вырезаем блок
                var block = res_block.find('#' + id).detach();
            } else {
                //Если есть, то вырезаем только блок
                var block = res_block.find('#' + id).detach();
            }
            //Вставляем блок
            res_block.eq(value).append(block);
        }

        //функция вывода информации
        function whileData(optName, optData, selId, selCat, optInd, optVal, needId, classLabel) {

            //Определение селектора сторон
            var side = checkSide(optInd);
            //если не сторона
            if (!side) {
                //ищем во всех блоках
                if (res_block.find('#' + selId).length != 0) {
                    //Если не в первом, получаем номер блока
                    var num = res_block.find('#' + selId).parent().index();
                } else {
                    //Если не находим, то добавляем в первый блок
                    var num = 0;
                }
                var mainBlock = res_block.eq(num);

                //Определяем, есть ли заголовок категории
                if (mainBlock.find('h5').text(selCat).length == 0) {
                    //Если нет - выводим название категории
                    mainBlock.find('h4').after('<h5 class="' + classLabel + '">' + selCat + '</h5>');
                }

                //Определяем, есть ли такой блок
                if (mainBlock.find('#' + selId).length == 0) {
                    mainBlock.append('<div id="' + selId + '" class="' + classLabel + '"></div>');
                } else {
                    //Если есть - очищаем
                    mainBlock.find('#' + selId).empty();
                }

                //вывод дата-аттрибутов
                $.each(optData, function (key, val) {
                    mainBlock.find('#' + selId).prepend('<p class="' + key + '">' + key + ': <span>' + val + '</span>' + '</p>');
                });

                //Добавляем название выбранной опции
                mainBlock.find('#' + selId).prepend('<h6>' + optName + '</h6>');
            } else {
                //если сторона, запускаем функцию переноса
                setSide(optVal, needId, optName);
            }
            //Выставляем значения сумм. информации по умолчанию
            var mass = 0;
            var power_consuption = 0;
            var produced_energy = 0;
            //Собираем информацию по всем блокам
            res_block.children('div').children('p').each(function () {
                //Если один из нужных блоков
                if ($(this).hasClass('mass') || $(this).hasClass('power_consuption') || $(this).hasClass('produced_energy')) {
                    //Сохраняем и слаживаем значения
                    if ($(this).hasClass('mass')) {
                        mass += parseFloat($(this).find('span').text());
                    } else if ($(this).hasClass('power_consuption')) {
                        power_consuption += parseFloat($(this).find('span').text());
                    } else {
                        produced_energy += parseFloat($(this).find('span').text());
                    }
                }
            });
            //Передаём данные функции вывода суммю информации
            summData(mass, power_consuption, produced_energy);
        }

        //Функция вывода суммарной информации
        function summData(mass, power_consuption, produced_energy) {
            //Очищаем блок сумм. информации для каждого пересчёта
            res_block.eq(4).children('h4').siblings().remove();
            //Обновляем данные
            res_block.eq(4).children('h4').after(
                '<p class="mass">Масса: ' + mass + '</p>' + '<p class="mass">Потребление энергии: ' + power_consuption + '</p>' + '<p class="mass">Производство энергии: ' + produced_energy + '</p>');
        }

        $(document).on('change', '.design_tabs select', function () {
            //Получаем информацию и передаём функции вывода
            var opt = $(this).find('option:selected');
            var name = opt.text();
            var id = opt.parent().attr('id');
            var category = opt.parents('li').find('label').text();
            var sideInd = $(this).index();
            var sideVal = parseInt($(this).val());
            var classLabel = $(this).parents('li').find('label').prev().attr('class');
            var data = opt.data();
            if (sideInd) {
                var needId = $(this).prev().attr('id');
            } else {
                var needId = $(this).attr('id');
            }
            whileData(name, data, id, category, sideInd, sideVal, needId, classLabel);
        });

        //Функция скрытия по переключению табов
        function tabs(cl) {
            //Скрываем всех потомков с данными в блоках, кроме сумм. информации
            res_block.parent().children(":not('li:eq(4)')").find('h4').siblings().hide();
            //Отображаем нужные потомки
            res_block.children('.' + cl).show();
        }

        $(document).on('click', '.design_tabs label', function () {
            var classLabel = $(this).prev().attr('class');
            tabs(classLabel);
        });

    });
})(jQuery);