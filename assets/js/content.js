/**
 * 
 * 用来读取markdown内容并加载到页面中
 * 
 */

var conname = suiyan.getQueryVariable('p'); //获得要加载Markdown文章的序列号。
if (conname == false) conname = 0;
var mkurl = './articles/' + conname + '.md'; //组装URL地址

// loadMarkdown(mkurl,'rt');//JS 原生AJAX加载.MD。
$(document).ready(function () {



    $.when(
        $.get(mkurl, function (data, status) {
            // alert(marked(data));
            $("#rt").html(marked(data)); //Markdown解析并加载日志
    
        })
        ).then(function () {
        //判断AJAX加载完毕加载代码美化CSS
        $('pre code').each(function (i, block) {
            hljs.highlightBlock(block);
        });
    })




});