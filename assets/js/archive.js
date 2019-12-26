$(document).ready(function () {

    $.getJSON("blog_data.json", function (data, textStatus, jqXHR) {
        // console.log(suiyan.formatData(data));
        suiyan.formatjson = suiyan.formatData(data); //格式化数据
        var $cl = $('.car-list');
        
        for (let index = 0; index < suiyan.formatjson.length; index++) {
            const element = suiyan.formatjson[index];
            //  console.log(element.data);
            var lihtml = '';
            for (let index = 0; index < element.data.length; index++) {
                const el = element.data[index];
                lihtml += '<li class="list-group-item"><a href="p.html?p='+el.url+'">'+el.title+'</a> <span title="发布日期">'+el.time+'</span></li>';
                suiyan.con ++;
                
            }
            // alert(lihtml)
            $cl.append('<li class="nav-item "><span class="car-yearmonth meta" style="cursor:pointer;"><i class="fa fa-list-ul" aria-hidden="true"></i> ' + element.date + ' <span class="meta" title="文章数量">(共' + element.data.length + '篇文章)</span></span><ul class="car-monthlisting list-group" style="display: block;">'+lihtml+'</ul></li>');
        }

        $('.archives-meta').html('<span class="meta">共有文章:'+ data.length +'篇,最后更新:'+data[0].time+'</span>');


        $('.car-all').click(function () {
            $('.car-monthlisting').slideToggle(500);
            $(this).html() == "折叠所有" ? $(this).text('展开所有') : $(this).text('折叠所有');
    
        });
    
        $('.car-yearmonth').click(function () {
            // alert('ok');
            $(this).next().slideToggle(500);
    
        });



    });





});