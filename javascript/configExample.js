/*
* @Date:   2017-09-27 18:12:59
* @Last Modified time: 2017-09-27 18:13:01
*/
'use strict';
/*
cp ./configExample.js ./config.js
修改config.js
 */
import path from "path";
import { ipReg } from "./utils/regRoles";
import { getIPAdress } from "./utils/envUtils"


const debug = true;
export {
    debug
}


/*
数据库地址、密码
 */
const dbHost = "gitlab.tianxi.com";
const dbPassword = "tianxiMySQL12315";
// const dbHost = "localhost";
// const dbPassword = "123zhang";
export {
    dbHost,
    dbPassword
}


/*
后台服务器、端口
 */
const serverIP = getIPAdress();
const serverPort = 3001;
const serverHttpAddress = "http://" + serverIP + ":" + serverPort;
let clientHttpAddress = req => {
    /*
    获取客户端ip：req.ip/本机ip
     */
    let clientIP = req.ip.match(ipReg) ? req.ip.match(ipReg)[0]: getIPAdress();
    let clientPort = 8080;
    return "http://" + clientIP + ":" + clientPort;
};
let getWebClientAddress = req => {
    let webClient = req.query.webClient || req.body.webClient;
    return debug ? webClient: clientHttpAddress(req);
};
export {
    serverIP,
    serverPort,
    serverHttpAddress,
    clientHttpAddress,
    getWebClientAddress
}


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
    viewsDirPath,
    publicDirPath,
    uploadDirPath,
    faviconPath
}