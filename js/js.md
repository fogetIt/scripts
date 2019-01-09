##### 自执行函数
```javascript
/**
 * ;    分隔符，防止压缩合并多个js文件时忘记写分隔符
 * !    自执行函数标志，引入js文件就自动执行
 */
;!function funName(arg) {
    ...
}
```

##### 类
```javascript
/**
 * 为jQuery类添加类方法(静态方法)
 */
jQuery.extend(object)
/**
 * 用一/多个其他对象来扩展一个对象，返回被扩展的对象
 */
jQuery.extend(target, object1, [objectN])
/**
 * 对jQuery.prototype进得扩展
 * 为jQuery类添加成员函数
 * jQuery.fn.extend = jQuery.prototype.extend
 */
jQuery.fn.extend(object);
```
##### 执行顺序
- JavaScript执行引擎并非一行一行地分析和执行程序，而是一段一段地分析执行的
- 在分析执行同一段代码中，定义式的函数会被提取出来优先执行
    ```javascript
    // 定义式的函数
    function funName(){...}
    // 非定义式的函数
    var funName = function(){...}
    ```
- 函数定义执行完后，才会按顺序执行其他代码


##### 默认参数
```javascript
function(arg){ var arg = arg || {}; }
```