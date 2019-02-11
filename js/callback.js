/*
* @Date:   2017-04-05 13:46:52
* @Last Modified time: 2017-04-05 13:50:37
*/
/*
回调函数：函数接收其它函数作为参数
*/
function execute(data, cb) {
    cb(data);
}
execute("Hello Callback", function(word) { console.log(word) });


const isAsync = false;
/*
同步变异步
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
             *
             * @description Event Loop
             * @description 主线程执行完同步任务，读取"任务队列"，执行异步任务，循环往复
             * @description Event Loop 先执行 setImmediate 回调，再执行 timer(setTimeout) 回调
             * @description 一轮 Event Loop 执行一层 setImmediate
             * @description 如果 setTimeout 间隔 <= 4ms，算成 4ms
             * @description 只有 cpu 有空的时候，才能执行 setTimeout(setTimeout 可能延期执行)
             * @description 由于 cpu 切片， setImmediate 和 setTimeout 的先后顺序不确定
             *
             * @`process.nextTick` 在当前"执行栈"尾部－－下一轮 Event Loop 之前－－触发函数
             * @warn 递归的 process.nextTick 须改成 setImmediate
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
