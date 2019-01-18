/*
* @Date:   2017-09-27 18:34:40
* @Last Modified time: 2017-09-27 18:34:41
*/
'use strict';
import { networkInterfaces } from "os";


let getIPAdress = () => {
    for (let devName in networkInterfaces()) {
        let iFace = networkInterfaces()[devName];
        for (let i = 0; i < iFace.length; i++) {
            let alias = iFace[i];
            if (alias.family === 'IPv4' && alias.address !== '127.0.0.1' && !alias.internal) {
                return alias.address;
            }
        }
    }
};


export {
    getIPAdress
}