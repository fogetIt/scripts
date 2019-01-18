/*
* @Date:   2017-09-27 10:30:20
* @Last Modified time: 2017-09-27 10:30:21
*/
'use strict';

const ipReg = /\d+\.\d+\.\d+\.\d+/;
const passwordReg = /^[0-9a-zA-Z@!.,]{8,16}$/;
// /^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/
const emailReg = /^[_.0-9a-z-]+@[0-9a-z]+.+[a-z]{2,3}$/;
const nicknameReg = /^([\u4E00-\uFA29]|[\uE7C7-\uE7F3]|[a-zA-Z0-9_]){1,10}$/;

export {
    ipReg,
    emailReg,
    passwordReg,
    nicknameReg
}