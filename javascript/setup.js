/*
* @Date:   2017-09-21 16:56:01
* @Last Modified time: 2017-09-21 16:56:02
*/
'use strict';
import logger from "morgan";
import express from "express";
import favicon from "serve-favicon";
import bodyParser from "body-parser";
import cookieParser from "cookie-parser";
import { viewsDirPath, publicDirPath, faviconPath } from "../config";


export default app => {
    /*
    view engine
     */
    app.set('views', viewsDirPath);
    app.set('view engine', 'jade');
    /*
    网页logo
     */
    // app.use(favicon(faviconPath));
    app.use(logger('dev'));
    app.use(bodyParser.json());
    app.use(bodyParser.urlencoded({ extended: false }));
    app.use(cookieParser());
    app.use(express.static(publicDirPath));
    /*
    跨域访问
     */
    app.all('*', (req, res, next) => {
        res.header("Access-Control-Allow-Origin", "*");
        res.header("Access-Control-Allow-Headers", "X-Requested-With");
        res.header("Access-Control-Allow-Methods","PUT,POST,GET,DELETE,OPTIONS");
        res.header("X-Powered-By",' 3.2.1');
        res.header("Content-Type", "application/json;charset=utf-8");
        next();
    });
}