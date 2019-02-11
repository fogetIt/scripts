/*
* @Date:   2017-04-06 09:39:48
* @Last Modified time: 2017-04-12 10:50:56
*/
'use strict';

function Class() {
    this.str = "str";
}
/**
 * 优先使用构造函数的属性
 * @type {String}
 */
Class.prototype.str = "new str"
Class.prototype.getStr = function() {
    console.log(this.str);
}

var instance1 = new Class();
var instance2 = new Class();

console.log(instance1.str); // str
console.log(instance2.str); // str
instance1.getStr(); // str
instance2.getStr(); // str
