/*
* @Date:   2017-04-05 13:46:52
* @Last Modified time: 2017-04-05 13:50:37
*/
/**
 * @回调函数 函数接收其它函数作为参数
 *
 * @libuv nodejs 基于事件驱动和非阻塞 I/O 模型的多线程实现
 * @V8 只有一个 javascript 解释器实例，运行在主线程，可以调用 libuv 的 io/timer
 * @info nodejs 的异步集中在 I/O 和 Timer 调用这一块，其他的地方没有
 *
 * @warn 回调函数是 javascript 处理异步函数调用返回值的方法
 * @warn 回调函数不一定都是异步执行的，而异步必须带一个回调函数
 */
function execute(data, cb) { cb(data); };
execute("Hello Callback", function(word) { console.log(word) });

const isAsync = false;
/**
 * @同步变异步
 */
function execute１(data, cb1, cb2, cb3) {
    console.log(data);
    switch(isAsync) {
        /**
         * @同步
         * 11111
         * 22222 1
         * 22222 2
         * 22222 3
         * 33333
         */
        case false:
            cb1();
            cb2();
            cb3();
            break;
        /**
         * @异步
         * 11111
         * 33333
         * 22222 3
         * 22222 2
         * 22222 1
         */
        case true:
            /**
             * @setImmediate 在当前"任务队列"的尾部注册事件，在下一轮 Event Loop 执行
             * @setTimeout 在当前"任务队列"的尾部注册事件，在下一轮 Event Loop 执行
             * @`process.nextTick` 在当前"执行栈"尾部－－下一轮 Event Loop 之前－－触发函数
             *
             * @warn 递归的 process.nextTick 须改成 setImmediate
             *
             * @info Event Loop
             *
             * @info setImmediate setTimeout process.nextTick 分别在不同的队列执行
             * @info process.nextTick 执行最快
             * @info setTmmediate 能保证每次 tick 都执行
             * @info setTimeout 是 libuv 的 Timber 保证，可能会有所延迟
             *
             * @info 主线程执行完同步任务，读取"任务队列"，执行异步任务，循环往复
             * @info 一轮 Event Loop 执行一层 setImmediate
             * @info 如果 setTimeout 间隔 <= 4ms，算成 4ms
             * @info 只有 cpu 有空的时候，才能执行 setTimeout(setTimeout 可能延期执行)
             * @info 由于 cpu 切片， setImmediate 和 setTimeout 的先后顺序不确定
             */
            setImmediate(cb1);
            setTimeout(() => cb2(), 0);
            process.nextTick(cb3);
            break;
    }
    console.log('33333');
}
execute１(
    '11111',
    function() { console.log('22222', 1); },
    function() { console.log('22222', 2); },
    function() { console.log('22222', 3); },
);
