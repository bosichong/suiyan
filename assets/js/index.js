$(document).ready(function () {
    //加载首页的blog数据
    $.getJSON("blog_data.json", function (blogdata, textStatus, jqXHR) {
        suiyan.blog_data = blogdata;


        $.when( //加载blog配置数据
            $.getJSON("config.json", function (data, textStatus, jqXHR) {
                suiyan.config = data;
            })).then(function () {
            // 翻页及首页调用数据
            $("#suiyanpage").jqPaginator({
                // totalPages: 100,//分页总数
                totalCounts: suiyan.blog_data.length, //设置分页的总条目数
                visiblePages: 1, //设置最多显示的页码数（例如有100也，当前第1页，则显示1 - 7页）
                pageSize: suiyan.config.blog_list, //设置每一页的条目数
                currentPage: 1, //当前页码
                prev: '<button type="button" class="prev btn btn-primary">Previous</button>',
                next: '<button type="button" class="next btn btn-primary">Next</button>',
                page: '<button type="button" class="page btn btn-primary">{{page}} / {{totalPages}} </button>',
                onPageChange: function (n) {
                    $('.data-list').html('');
                    var endp = n * suiyan.config.blog_list;
                    var startp = endp - suiyan.config.blog_list

                    for (let index = startp; index < endp; index++) {
                        const element = blogdata[index];
                        var mkurl1 = suiyan.geturl(element.url);

                        $.when(
                            $.get(mkurl1, function (data, status) {
                                var blogmd = marked(data); //Markdown解析并加载日志
                                htmlString = '<div class="b_data list-group-item">' + blogmd + '</div>';
                                $('.data-list').append(htmlString);


                            })).then(function () {
                            //判断AJAX加载完毕加载代码美化CSS
                            $('pre code').each(function (i, block) {
                                hljs.highlightBlock(block);
                                $("img").addClass("img-fluid");
                            });
                        })

                    }

                }
            });


        });












    });










});
