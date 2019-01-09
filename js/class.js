/*
* @Date:   2017-04-06 09:39:48
* @Last Modified time: 2017-04-12 10:50:56
*/

'use strict';

function classInit() {
    this.str = "str";
    this.num = 1.23;
    this.bool = true;
    console.log(typeof this.str, typeof this.num, typeof this.bool);
}

/**
 * 优先使用构造函数的属性
 * @type {String}
 */
classInit.prototype.str = "new str"
classInit.prototype.def = function (arg) {
    console.log(arg);
}


var instance = new classInit();
instance.def('function');
console.log(instance.str);

console.log("#################################");

var instance1 = new classInit();
instance.def('function1');
console.log(instance1.str);