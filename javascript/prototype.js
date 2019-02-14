/*
* @Date:   2017-04-06 09:39:48
* @Last Modified time: 2017-04-12 10:50:56
*/
'use strict';

function Cls() {
    var a = 'a'; // 私有变量(外部无法访问)
    this.c1 = 'c'; // 实例变量(对象无法访问)
    this.c2 = [];
    this.print1 = function() {
        console.log(this.c1, this.c2);
    }
}
Cls.b = 'b'; // 静态变量(实例无法访问)

var instance1 = new Cls();
console.log(Cls.a, instance1.a);   // undefined undefined
console.log(Cls.b, instance1.b);   // b undefined
console.log(Cls.c1, instance1.c1); // undefined 'c'
console.log();
/**
 * 实例变量互不影响
 */
var instance2 = new Cls();
instance1.c1 = 'cc';
instance2.c2.push('hello');
console.log(instance1.c1, instance2.c1); // 'cc' 'c'
console.log(instance1.c2, instance2.c2); // [] [ 'hello' ]
console.log();
/**
 * 每个实例都要保持一份方法的复制，这是不科学的
 */
Cls.prototype.print2 = function() { console.log(this.c1, this.c2); };
instance1.print1(); // cc []
instance2.print1(); // c [ 'hello' ]
console.log(instance1.print1 === instance2.print1); // false
instance1.print2(); // cc []
instance2.print2(); // c [ 'hello' ]
console.log(instance1.print2 === instance2.print2); // true
console.log();
/**
 * @原型链
 * 普通对象(最下级实例对象)没有 propotype ，但是有 __proto__ 属性
 * __propo__ 指向用于创建自身的原型对象的 prototype
 * 实例-->对象原型--> object --> null 之间有一条链式关系，所有 JS 对象都是一级一级克隆下来的
 *
 * 补充，原型链在不同的引擎中，实现略有不同，如：
 * __propo__ 是否属于 prototype
 * prototype 是否包含一个 construcotr
 */
console.log(instance1.prototype, instance1 instanceof Cls); // undefined true
console.log(instance1.__proto__ === Cls.prototype); // true
console.log(Cls.__proto__ === Function.prototype); // true
console.log();
/**
 * @多继承
 * 把方法拿来给对象用(对象可以通过继承拥有任意对象的任意方法)
 * func.call(obj, arg, ...)
 * func.apply(obj, [arg, ...])
 */
function add(a, b) { console.log(a + b); };
function sub(a, b) { console.log(a - b); };
add.call(sub, 4, 2); // 6

function A() {
    this.a = 123;
    this.print = function() { console.log(this.a); };
}

function B() {
    this.a = 456;
    new A().print.call(this);
}
new B(); // 456

function C() {
    this.a = 456;
}
new A().print.call(new C()); // 456

function D() {
    A.call(this);
    this.a = 456;　// 注意
}
new D().print(); // 456