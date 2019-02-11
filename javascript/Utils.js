/*
* @Date:   2017-09-27 18:34:40
* @Last Modified time: 2017-09-27 18:34:41
*/
'use strict';
import path from "path";
import { networkInterfaces } from "os";

const getIPAdress = () => {
    for (let devName in networkInterfaces()) {
        const iFace = networkInterfaces()[devName];
        for (let i = 0; i < iFace.length; i++) {
            const alias = iFace[i];
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

/**
 * 获取客户端ip：req.ip/本机ip
 */
const clientHttpAddress = req => {
    const clientIP = req.ip.match(ipReg) ? req.ip.match(ipReg)[0]: getIPAdress();
    const clientPort = 8080;
    return `http://${clientIP}:${clientPort}`;
};
const getWebClientAddress = req => {
    const webClient = req.query.webClient || req.body.webClient;
    return debug ? webClient: clientHttpAddress(req);
};

/*
lib dir path === __dirname
@type {string|*}
 */
const rootDirPath = path.resolve(__dirname, '..');
const viewsDirPath = path.join(__dirname, "views");
const publicDirPath = path.join(__dirname, "public");
const uploadDirPath = path.join(__dirname, "public/images");
const faviconPath = path.join(__dirname, "public", "images", "favicon.ico");

export {
    ipReg,
    emailReg,
    passwordReg,
    nicknameReg,
    getIPAdress,
    getWebClientAddress
}