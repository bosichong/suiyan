$(document).ready(function () {
    $.getJSON("blog_data.json", function (data, textStatus, jqXHR) {
        suiyan.tagsjson = suiyan.format_tags_data(data);
        // console.log(suiyan.tagsjson);
        //加载TAG 按钮
        var $tags = $('.tags');
        for (let index = 0; index < suiyan.tagsjson.length; index++) {
            const element = suiyan.tagsjson[index];
            $tags.append('<button class="tag-bt btn btn-info btn-sm" data-toggle="collapse" href="#collapseExample" role="button" aria-expanded="false" aria-controls="collapseExample"><span class="tagval">'+element.tag+'</span> <span class="badge badge-light">'+element.data.length+'</span></button>');
        }

        
        //tag按钮点击事件，点击后加载相关数据

        // $(".tag-bt").toggle(function(){
        //     $(this).siblings("btn").hiden();
        // },function(){
        //     $(this).siblings("btn").show();
        // });
        $('.tag-bt').click(function (e) { 
            $(this).siblings(".btn").fadeToggle(500);
            $('.tagcad').fadeToggle(500);
            var val = $(this).find('.tagval').text();
            // alert(val);
            // var arr = null;
            suiyan.tag_json = suiyan.get_tag_json(suiyan.tagsjson,val);
            // console.log(suiyan.tag_json);
            $('.card-header').text(suiyan.tag_json.tag);
            var $tagul = $('.card-body > ul').html('');
            var lihtml = '';
            for (let index = 0; index < suiyan.tag_json.data.length; index++) {
                const element = suiyan.tag_json.data[index];
                $tagul.append('<li>'+element.title+'</li>')
                lihtml += '<li class="list-group-item"><a href="p.html?p='+element.url+'">'+element.title+'</a> <span class="meta" title="发布日期">'+element.time+'</span></li>';
                
            }
            $tagul.html(lihtml);

            
            
        });


            
        });


    
});



