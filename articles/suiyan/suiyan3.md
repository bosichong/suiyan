---
title:这是一个快速学习JavaScript的学习笔记3
author:J.sky
time:2019-12-23 11:53:19
tag:JavaScript
---

## JavaScript中的对象

JavaScript 定义了 5 种原始数据类型：

    string
    number
    boolean
    null
    undefined

除了这些都是对象，对象是包含变量的变量。


    //JavaScript对象
    //定义对象
    var p = {fname:"javascript",lname:"function"}
    p.oname = "java";//对象添加属性
    //forin 遍历对象属性。
    for (k in p ){console.log(p[k]);}
    delete p.oname;
    console.log(p.oname);//undefined
    p.f = function (s) { console.log(s)}//方法
    p.f('定义对象中的方法。')

    // 定义类
    function Person(name,age){
        this.name = name;
        this.age = age;
    }



## <p id="m1">JavaScript 对象原型</p>

**所有 JavaScript 对象都从原型继承属性和方法。**

Object.prototype 位于原型继承链的顶端：

为对象添加属性和方法：



    // 接上边的例子
    //通过prototype添加属性和方法。
    Person.prototype.where = 'china';
    Person.prototype.sayHello = function() {alert(this.name+" hello "+this.where)}
    p1.sayHello();


