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



