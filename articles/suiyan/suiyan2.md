---
title:这是一个快速学习JavaScript的学习笔记2
author:J.sky
time:2019-12-22 10:55:19
tag:JavaScript
---


## JavaScript语句

var和function是用来声明变量和语句的。
```JavaScript
var a,b,c=88;

```

### 条件语句

```JavaScript
//if else
var n = 2;
if (n == 1) {
    alert('ok')
} else {
    lert('no')
}


//switch
var m = 4;
switch (m) {
    case 1:
        alert('no')
        break;
    case 4:
        alert('yes')
    default: //如果条件都不符合执行
        break;
}

```

### 循环语句

* for - 多次遍历代码块
* for/in - 遍历对象属性
* while - 当指定条件为 true 时循环一段代码块
* do/while - 当指定条件为 true 时循环一段代码块


* break 语句“跳出”循环。
* continue 语句“跳过”循环中的一个迭代。

```JavaScript
//while 略
//do while 略

// for
var i = 0, j = 10;
for (i; i<j; i++) {
    console.log(i)
    
}

```

### function 

function用来声明一个函数。

```JavaScript
function myFunction(p1, p2) {
    return p1 * p2;              // 该函数返回 p1 和 p2 的乘积
}

var mf = myFunction(p1, p2) {
    return p1 * p2;              // 该函数返回 p1 和 p2 的乘积
}

//见 test.js
var mf = function myFunction(p1, p2) {
    return p1 * p2;              // 该函数返回 p1 和 p2 的乘积
}
document.querySelector("div").textContent = mf(6,2);//12

```

## <p id = 'm1'>匿名函数与闭包</p>

```JavaScript

//这是一个匿名函数
//匿名函数可以用来命名空间，且立即执行，避免变量污染。
(function(){console.log('匿名函数写法1')}());
//推荐第二种方法。
(function(s){console.log(s)})('匿名函数写法2');


//简书上一篇不错的JavaScript闭包的文章
//https://www.jianshu.com/p/80fb145d57d7
//闭包1
var add = (function () {
    var counter = 0;
    return function () {return counter += 1;}
})();
 
add();
add();
console.log(add());//=>3


//闭包2
;(function(){
    var a=1;
    var addOne=function(x){
        return x+a;
    }
    window.addOne=addOne;
})()
console.log(addOne(2));  // 3


```

