### Node.js
- 一个事件驱动 I/O 服务端 JavaScript 环境
- 基于 Google V8 引擎(速度快，性能好)

##### npm
- npm -h
    - 查看手册
- npm list [-g]
    - 查看所有已(全局)安装模块
- npm i/install [package[@num] [--save]] [-g]
    - 安装依赖包
        - 如果没有指定包名，则检查当前 `package.json` 的所有依赖
        - `@num` 指定包的版本
        - `--save` 自动加入 `package.json` 的　`dependencies`
        - `-g` 全局安装到 `$node/lib/node_modules`
- npm uninstall package [--save/-g]
    - 卸载
        - `--save` 依据 `package.json` 卸载
        - `-g` 全局卸载
- npm view package versions
    - 查看模块所有可用版本

##### npm vs bower
- npm，Node.js 包管理器
    - 支持嵌套依赖管理
    - js 通用的包管理工具
- bower，专门为前端表现设计的包管理器
    - 只能支持扁平的依赖（嵌套的依赖，由程序员自己解决）
    - 只解决了包和依赖的下载问题，但没解决加载顺序问题，开发者需要手动加载模块并调整顺序

##### package.json
- main
    + nodejs 环境入口
- browser
    + 浏览器环境入口
- dependencies
    + 正常运行该项目时所需的依赖包
        ```bash
        npm i --production
        ```
    + 模块:版本号
        * ^4.1.2
            - 主版本号不变，尽可能新
        * ~4.1.2
            - 主版本号和次版本号都不变(不超过4版本)
- devDependencies
    + 开发时所需的依赖包，像一些进行单元测试之类的包
        ```bash
        npm i --dev
        ```
- scripts
    + 命令脚本
        ```bash
        npm run ***
        ```

##### es7
```javascript
'use strict';
require("babel-core/register")({presets: ['stage-3','es2015']});
require("babel-polyfill");
require("./app.js");
```

##### es6 导入模块
```javascript
export { xxx, yyy }
import { xxx, yyy } from ...
// export default
export default xxx
import xxx from ...
// export from
export { xxx } from ...
import { xxx } from ...
// export default multi
export default { xxx, yyy } from ...
import module from ...
let xxx = module.xxx
let yyy = module.yyy

export default { xxx, yyy }
import module from ...
let xxx = module.xxx
let yyy = module.yyy
```

##### es5 modules
- module.exports
    + 导出代码
    + 初始值为{}
- exports
    + 指向module.exports的引用
- module.exports 指向新的对象时，exports 断开了与 module.exports 的引用
    + 重新引用exports = module.exports = somethings
- require
    + 加载载module.exports代码

##### 箭头函数
- ES6 新特性
- 不能用 new 来实例化(构造类对象)
- 没有arguments对象
- this不再善变
```javascript
// 省略 return
() => ***
arg => arg * arg
(arg1, arg2) => arg1 * arg2
// 返回对象(紧随箭头的 { 被解析为块的开始)
arg => ({})
// 执行其它函数
arg => {
    func1(arg);
}
```