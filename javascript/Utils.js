/*
* @Date:   2017-09-27 18:34:40
* @Last Modified time: 2017-09-27 18:34:41
*/
'use strict';
import { networkInterfaces } from "os";

const getIPAdress = () => {
    for (let devName in networkInterfaces()) {
        const iFace = networkInterfaces()[devName];
        for (let i = 0; i < iFace.length; i++) {
            let alias = iFace[i];
            if (alias.family === 'IPv4' && alias.address !== '127.0.0.1' && !alias.internal) {
                return alias.address;
            }
        }
    }
};

const ipReg = /\d+\.\d+\.\d+\.\d+/;
const passwordReg = /^[0-9a-zA-Z@!.,]{8,16}$/;
// /^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/
const emailReg = /^[_.0-9a-z-]+@[0-9a-z]+.+[a-z]{2,3}$/;
const nicknameReg = /^([\u4E00-\uFA29]|[\uE7C7-\uE7F3]|[a-zA-Z0-9_]){1,10}$/;

export {
    ipReg,
    emailReg,
    passwordReg,
    nicknameReg,
    getIPAdress
}