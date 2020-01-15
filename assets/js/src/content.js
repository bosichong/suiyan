/**
 * 
 * 用来读取markdown内容并加载到页面中
 * 
 */

var conname = suiyan.getQueryVariable('p'); //获得要加载Markdown文章的序列号。
if (conname == false) conname = 0;
var mkurl = './articles/' + conname + '.md'; //组装URL地址
var inx = 1;



// loadMarkdown(mkurl,'rt');//JS 原生AJAX加载.MD。
$(document).ready(function () {



    $.when(
        $.get(mkurl, function (data, status) {
            // alert(marked(data));
            $("#rt").html(marked(data)); //Markdown解析并加载日志

        }),
        $.getJSON("blog_data.json",
            function (data, textStatus, jqXHR) {
                var bcon = data.length;
                var inx = data.findIndex((item) => {
                    return item['url'] == conname;
                });


                if (inx <= 0) {
                    $('.pr').html('到头啦！(*￣︶￣)');
                } else {
                    var el = data[inx - 1]
                    var ltitle = el.title;
                    var lurl = 'p.html?p=' + data[inx - 1].url;
                    $('.pr').html('<a href="' + lurl + '">' + ltitle + ' <i class="fa fa-long-arrow-left" aria-hidden="true"></i> <i class="fa fa-long-arrow-left" aria-hidden="true"></i></a> ');
                }


                if (inx >= bcon - 1) {
                    $('.ne').html('到头啦！(*￣︶￣)');
                } else {
                    var el = data[inx + 1]
                    var rtitle = el.title;
                    var rurl = 'p.html?p=' + data[inx + 1].url;
                    $('.ne').html('<a href="' + rurl + '"> <i class="fa fa-long-arrow-right" aria-hidden="true"></i> <i class="fa fa-long-arrow-right" aria-hidden="true"></i>' + rtitle + '</a>');

                }

                

            }
        )
    ).then(function () {
        //判断AJAX加载完毕加载代码美化CSS
        $('pre code').each(function (i, block) {
            hljs.highlightBlock(block);
        });
        $("img").addClass("img-fluid");
        //修改博客文章页的title
        let str = $(".title").text();
        $("title").text(str);

        




    })




});