---
title:这是一个快速学习JavaScript的学习笔记1
author:J.sky
time:2017-12-21 10:54:19
tag:JavaScript
---


## JavaScript的代码写在哪里？

`JavaScript`变量名区分大小写。

`;`用来分隔语句，如果语句是一行的情况下，可以省略（有些情况下是不行的）。

`HTML`代码中嵌入 `<script>  </script>`

外部引用：`<script src="./js/main.js"></script>`，放在`<head>`或`<body>`标签内。

## <p id='m1'>语法结构</p>

### 注释

```JavaScript
// 单行注释

/*
*这是一段注释
*/

/* 这也是一段注释 */
```

### 数据类型

包括数值，字符串，布尔和对象(object)，还有两个特殊类型如下：

```JavaScript

null //空
undefined //未定义变量

```

JavaScript变量是无类型的，可以被赋予任何类型的值。


### 数字

```
11
10090

0Xff//十六进制

3.14
1.11e23

```

### 算术运算

```

1+2
8-4
2*5
7/4
9%2 //取余数

i++
j--

```

### 文本字符串

```
JavaScript是一种面向对象的语言\ //（\）可以换行
// 也可以用 \n 换行。

var s = "hello world"+"你好 世界"
s.length //字符串长度
```

字符串可以用""或'',当在HTML中编写JavaScript的时候，可以使用其中的一种来确认引号的风格。用`\`来转义一些特殊字符。

### 布尔值

`true flase`

### <p id='m2'>声明变量、常量</p>

```
var a;
var b ,c;
var d=1,f=77,g='abc';
var kk;//如果变量没有指定初始值，它的初始值就是undefined

var glo = 44; //全局变量不可删除
glo1 = 22; //可以删除的全局变量。
delete glo1;//删除

//见 test.html test.js
const NB998 = 'nb998';
document.querySelector('.aa').textContent = NB998;

```

### eval()

出于JavaScript安全，不建议使用`eval()`

```
eval("4+8") // 12

```

### 三元运算符

?左边是布尔条件，右边是可选择的结果,用`:`分隔开。

```
var x = -8;
alert(x > 0 ? x : -x) //求x的绝对值 结果为8

```
