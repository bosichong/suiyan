var suiyan = {} //命名一个自己用的空间




//首页搜索结果
suiyan.getsearch = function (data, k) {
    var arr = [];
    data.forEach(function (item, i) {
        var key = item.title;
        var regex = new RegExp(k, 'i');//创建RegExp对象。
        console.log(regex);
        var result = regex.test(key);
        if (k !== '' && result) {
            arr.push(item)
        }
    });
    return arr;
}





/**
 * 站点页面模板
 */

// 左侧导航导航
// loadHtml('./templates/side.html','lt');//JavaScript原生AJAX
$(document).ready(function () {

    var scon = 100
    $('.hide').each(function (index, element) {
        $(this).fadeIn(scon);
        scon += 100;

    });
    $.getJSON("./blog_data.json", function (blogdata, textStatus, jqXHR) {
        suiyan.blog_data = blogdata;

        // 搜索按钮
        $('.search').click(function (e) {
            var key = $('#skey').val();
            var sdata = suiyan.getsearch(suiyan.blog_data, key)
            var shtmlstr = '';
            if (sdata != '') {
                shtmlstr += '<ul class="car-list navbar-nav">'
                for (let index = 0; index < sdata.length; index++) {
                    const el = sdata[index];
                    // 处理路径，是结果保证为blog的根目录
                    if (el.url.indexOf("/")){
                        el.url = el.url.split("/").pop();
                    }
                    // 处理win路径
                    if (el.url.indexOf("\\")){
                        el.url = el.url.split("\\").pop();
                    }

                    shtmlstr += '<li class="list-group-item"><a href="./' + el.url + '.html">' + el.title + '</a> <span title="发布日期">' + el.time + '</span></li>';
                }
                shtmlstr += '</ul>'
            } else {
                shtmlstr = '<p>没有搜到任何结果哦！</p>'
            }
            $('.search-list').html(shtmlstr);

        });

    });




});$(document).ready(function () {

    $('.car-all').click(function () {
        $('.car-monthlisting').slideToggle(500);
        $(this).html() == "折叠所有" ? $(this).text('展开所有') : $(this).text('折叠所有');

    });

    $('.car-yearmonth').click(function () {
        // alert('ok');
        $(this).next().slideToggle(500);

    });




});