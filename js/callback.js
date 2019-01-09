/*
* @Date:   2017-04-05 13:46:52
* @Last Modified time: 2017-04-05 13:50:37
*/

function execute(value, someFunction) {
    someFunction(value);
}
/**
 * 回调函数
 * 在函数接收参数的位置直接定义函数作为参数
 */
execute("Hello", function(word){console.log(word)});