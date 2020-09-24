$(document).ready(function () {

    $('.car-all').click(function () {
        $('.car-monthlisting').slideToggle(500);
        $(this).html() == "折叠所有" ? $(this).text('展开所有') : $(this).text('折叠所有');

    });

    $('.car-yearmonth').click(function () {
        // alert('ok');
        $(this).next().slideToggle(500);

    });




});