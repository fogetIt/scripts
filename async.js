/*
 * @Date:   2018-03-16 18:57:28
 * @Last Modified time: 2018-03-17 22:00:46
 */
'use strict';

// async function -> Promise
let promise0 = async () => {
    console.log('before');
    // await Promise
    let result = await new Promise(resolve => {
        setTimeout(
            () => {
                console.log("await 5s");
                resolve("success")
            }, 5000
        );
    })
    // throw new Error();
    return result;
};


let promise1 = async () => {
    console.log('before1');
    let result = await promise0();
    // throw new Error();
    return result;
};


// promise0().then(result => {
//     console.log(result);
// }).catch(err => {
//     console.log(err);
// })

promise1().then(result => {
    console.log(result);
})