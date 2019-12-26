/**
 * 站点页面模板
 */

// 左侧导航导航
// loadHtml('./templates/side.html','lt');//JavaScript原生AJAX
$(document).ready(function () {


    // 左侧导航导航
    $(".header").load("/assets/templates/side.html", function (response, status, request) {
        if (status == "success")
            console.log("左侧导航加载成功！");
    });

    // footer.html
    $(".footer").load("/assets/templates/footer.html", function (response, status, request) {
        if (status == "success")
            console.log("底部导航加载成功！");

    });

    //加载blog配置数据,并填充数据到页面
    $.getJSON("config.json", function (data, textStatus, jqXHR) {
        // alert(data.blog_name);
        //站点信息填充
        suiyan.config = data;
        $("title").text(data.blog_name + data.meta_description);
        $("meta[name='description']").attr("content", data.meta_description);
        $("meta[name='author']").attr("content", data.blog_author);
        //blog基本信息
        $(".blog-name a").text(data.blog_name); //bolg名称
        $(".blog-description").text(data.blog_description);

        //循环添加SNS
        (function (data, ul) {
            for (let i = 0; i < data.length; i++) {
                var lihtml = $('<li><a href="' + data[i].url + '" target="blank_blank"><i class="fa fa-' + data[i].ico + ' fa-lg"></li></a></i>');
                ul.append(lihtml);

            }

        })(data.blog_sns, $(".social-list"));

        //循环添加导航
        (function (data, ul) {
            for (let i = 0; i < data.length; i++) {
                var lihtml = $('<li class="nav-item "><a class="nav-link" href="' + data[i].url + '"><i class="fa fa-' + data[i].ico + ' fa-lg"></i> ' + data[i].text + '</a></li>');
                ul.append(lihtml);

            }

        })(data.nav, $(".blog-nav"));

       
    });








});