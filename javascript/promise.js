'use strict';
/**
 * 声明 promise
 * Promise.then(onFulfilled, OnRejected) => newPromise
 * onFulfilled    成功后执行函数
 * OnRejected     失败后执行函数
 *
 * 可以在 .then() 链中嵌入 .catch()
 * 当执行一堆 then() 的过程中出现错误的时候会找到最近的 .catch() 执行
 */
const p1 = new Promise((resolve, reject) => {
    resolve(111111);
});

const p2 = new Promise((resolve, reject) => {
    resolve(222222);
});

const arg = parseInt(process.argv.splice(2));
/**
 * 执行顺序
 */
if (arg === 1) {
    /**
     * 333333
     * 111111
     * 222222
     */
    p2.then(async res2 => {
        await p1.then(res1 => { console.log(res1); });
        console.log(res2);
    })
    console.log(333333)
} else if (arg === 2) {
    /**
     * 333333
     * 222222
     * 111111
     */
    p2.then(res2 => {
        p1.then(res1 => { console.log(res1); });
        console.log(res2);
    })
    console.log(333333)
} else if (arg === 3) {
    /**
     * 333333
     * 222222
     * 111111
     */
    p2.then(async res2 => {
        console.log(res2);
        return p1
    }).then(res1 => { console.log(res1); });
    console.log(333333)
} else if (arg === 4) {
    /**
     * 222222
     * 111111
     * 333333
     */
    (async () => {
        await p2.then(async res2 => {
            p1.then(res1 => { console.log(res1); });
            console.log(res2);
        })
        console.log(333333);
    })();
} else if (arg === 5) {
    (async () => {
        console.log('before');
        return await new Promise(resolve => {
            console.log("await 5s");
            setTimeout(() => {
                resolve("success")
            }, 5000);
        })
    })().then(result => {
        console.log(result);
    });
}
