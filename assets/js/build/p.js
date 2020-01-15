/* BuildTime:January15,202010:50:49 */
var suiyan = {} //命名一个自己用的空间




//首页搜索结果
suiyan.getsearch = function (data, k) {
    var arr = [];
    data.forEach(function (item, i) {
        var key = item.title;
        if (k !== '' && key.indexOf(k) > -1) {
            arr.push(item)
        }
    });
    return arr;
}


//首页加载数据ajax地址拼装
suiyan.geturl = function (url) {
    var mkurl = './articles/' + url + '.md'; //组装ajaxURL地址
    return mkurl;
}

//日志归档排序
suiyan.formatData = function (data) {
    var arr = [];
    data.forEach(function (item, i) {
        var tmpDate = new Date(item.time.split('-').join('/'));//兼容safari 出现 invalid
        var month = tmpDate.getMonth() + 1;
        var year = tmpDate.getFullYear();
        if (i === 0) {
            var tmpObj = {};
            tmpObj.date = year + '年' + month + '月';
            // console.log(year);
            
            tmpObj.data = [];
            tmpObj.data.push(item);
            arr.push(tmpObj);
            
        } else {
            if (arr[arr.length - 1]['date'] === (year + '年' + month + '月')) {
                arr[arr.length - 1]['data'].push(item);
            } else {
                var tmpObj = {};
                tmpObj.date = year + '年' + month + '月';
                tmpObj.data = [];
                tmpObj.data.push(item);
                arr.push(tmpObj);
            }
        }

    });
    return arr;
}

//根据TAG重新分组数据
suiyan.format_tags_data = function (data) {
    var arr = []
    data.forEach(function (item, i) {
        var t = item.tag;
        // console.log(t);
        if (i === 0) {
            //第一次循环 创建一个TAG
            var tmpObj = {};
            tmpObj.tag = t;
            tmpObj.data = [];
            tmpObj.data.push(item);
            arr.push(tmpObj);
        } else {
            //如果不是第一次，就和上一次的比较TAG，如果相同，添加
            isok = true;
            for (let index = 0; index < arr.length; index++) {
                const element = arr[index];
                if (element['tag'] === t) {
                    element['data'].push(item);
                    isok = false;
                    break;
                }

            }

            if (isok) {
                var tmpObj = {};
                tmpObj.tag = t;
                tmpObj.data = [];
                tmpObj.data.push(item);
                arr.push(tmpObj);
            }
            // if (arr[arr.length - 1]['tag'] === t) {
            //     arr[arr.length - 1]['data'].push(item);
            // } else {
            //     var tmpObj = {};
            //     tmpObj.tag = t;
            //     tmpObj.data = [];
            //     tmpObj.data.push(item);
            //     arr.push(tmpObj);
            // }

        }


    });
    console.log(arr);

    return arr;
}



//返回当前TAG相关的JSON数据
suiyan.get_tag_json = function (data, key) {
    var s = {};
    data.forEach(function (item, i) {
        if (item.tag == key) {
            s = item;
        }


    });
    return s;
}

/**
 * JS获取url参数
 * @param {*} variable 
 */
suiyan.getQueryVariable = function (variable) {
    var query = window.location.search.substring(1);
    var vars = query.split("&");
    for (var i = 0; i < vars.length; i++) {
        var pair = vars[i].split("=");
        if (pair[0] == variable) {
            return pair[1];
        }
    }
    return (false);
}



// /**
//  * 加载Markdown文档并解析
//  */
// function loadMarkdown(url, id) {
//     var xmlhttp;
//     if (window.XMLHttpRequest) {
//         //  IE7+, Firefox, Chrome, Opera, Safari 浏览器执行代码
//         xmlhttp = new XMLHttpRequest();
//     } else {
//         // IE6, IE5 浏览器执行代码
//         xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
//     }
//     xmlhttp.onreadystatechange = function () {

//         if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
//             // alert(document.getElementById(id));
//             document.getElementById(id).innerHTML = wrmk(xmlhttp.responseText);
//             // document.getElementById(id).innerHTML = "wrmk(xmlhttp.responseText)";
//             //<!-- highlight.js AJAX加载后执行 -->
//             hljs.initHighlighting.called = false;
//             hljs.initHighlighting();
//         }
//     }

//     xmlhttp.open("GET", url, true);
//     xmlhttp.send();

// }




// /**
//  * AJAX
//  */
// function loadHtml(url, id) {
//     var xmlhttp;
//     if (window.XMLHttpRequest) {
//         //  IE7+, Firefox, Chrome, Opera, Safari 浏览器执行代码
//         xmlhttp = new XMLHttpRequest();
//     } else {
//         // IE6, IE5 浏览器执行代码
//         xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
//     }
//     xmlhttp.onreadystatechange = function () {

//         if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
//             // alert(xmlhttp.responseText)
//             document.getElementById(id).innerHTML = xmlhttp.responseText;
//         }
//     }

//     xmlhttp.open("GET", url, true);
//     xmlhttp.send();

// }




// //获取第一个反斜杠后的内容
// suiyan.getLasturl = function (value) {
//     if (value !== null || value !== ''){ //使用split 进行分割，一定要进行字符串判空
//         var str = value.split("http://");
//         var index = str[1].indexOf("/") + 1;
//         return str[1].substring(index);
//     }
//     return null;
// }


/**
 * 站点页面模板
 */

// 左侧导航导航
// loadHtml('./templates/side.html','lt');//JavaScript原生AJAX
$(document).ready(function () {

    // footer.html
    $(".footer").load("assets/templates/footer.html", function (response, status, request) {
        if (status == "success")
            console.error("如果你能看到这里说明你已经很牛逼撩！欢迎进群讨论学习Q群:217840699");

    });




    //加载blog配置数据,并填充数据到页面
    $.getJSON("config.json", function (data, textStatus, jqXHR) {
        // alert(data.blog_name);
        //站点信息填充
        // $('#blogcss').attr("href", "assets/css/"+data.blogcss+".css");
        // $('#highlight').attr("href", "assets/plugins/highlight/styles/"+data.highlight+".css");

        suiyan.config = data;
        var metaheml = '<title>'+data.blog_name + data.meta_description+'</title>\
        <meta name="keywords" content="' + data.meta_keywords + '">\
        <meta name="description" content="' + data.meta_description + '">\
        <meta name="author" content="' + data.blog_author + '">';
        $("meta[name='viewport']").after(metaheml);

        //blog基本信息
        $(".blog-name a").text(data.blog_name); //bolg名称
        $(".blog-description").text(data.blog_description);
        $('.profile-image').attr("src", data.profile_image);




        //循环添加SNS
        (function (data, ul) {
            for (let i = 0; i < data.length; i++) {
                var lihtml = $('<li><a class="hide" href="' + data[i].url + '" target="blank_blank"><i class="fa fa-' + data[i].ico + ' fa-lg"></li></a></i>');
                ul.append(lihtml);

            }

        })(data.blog_sns, $(".social-list"));

        //循环添加导航
        (function (data, ul) {
            for (let i = 0; i < data.length; i++) {
                var lihtml = $('<li class="nav-item hide"><a class="nav-link" href="' + data[i].url + '"><i class="fa fa-' + data[i].ico + ' fa-lg"></i> ' + data[i].text + '</a></li>');
                ul.append(lihtml);

            }

        })(data.nav, $(".blog-nav"));

        //隐藏元素的动画
        var scon = 100
        $('.hide').each(function (index, element) {
            $(this).fadeIn(scon);
            scon += 100;

        });

    });


    $.getJSON("blog_data.json", function (blogdata, textStatus, jqXHR) {
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
                    shtmlstr += '<li class="list-group-item"><a href="p.html?p=' + el.url + '">' + el.title + '</a> <span title="发布日期">' + el.time + '</span></li>';
                }
                shtmlstr += '</ul>'
            } else {
                shtmlstr = '<p>没有搜到任何结果哦！</p>'
            }
            $('.search-list').html(shtmlstr);

        });

    });




});
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
