##### HTTP 协议访问 URL
- GET/POST/PUT/DELETE，对应着资源的查、改、增、删操作
- 对资源的增、删、改、查操作，都可以通过 GET/POST 完成，不需要用到 PUT/DELETE
- HTTP 协议对 GET/POST 请求数据没有长度限制
- HEAD
    - 告诉服务器只要得到信息头，页面内容不要
- GET
    - 缺省
    - 告诉服务器只要得到页面上的信息
    - 自动添加 HEAD ，确保 HEAD 按照 HTTP RFC 的要求来处理
    - 参数放在 URL 之后，以 ? 分割 URL 和参数，参数之间以 & 相连
        - 例：`EditPosts.aspx?name=test1&id=123456`
            - 如果数据是英文字母、数字，原样发送
            - 如果数据是空格，转换为 +
            - 如果数据是中文或其他字符，用 base64 加密
        - 通过地址栏来传值，提交的数据大小有限制(浏览器对 URL 的长度有限制)
            - IE：2083字节
            - Netscape/FireFox：长度取决于操作系统
        - 安全问题
            - 数据附着在 URL 上，可以从浏览器缓存的历史记录获取到
            - Cross-site request forgery 攻击
    - 用于获取、查询资源
        - 安全要求：不应产生副作用(用于获取而非修改信息，不会影响资源状态)
        - 幂等要求：对同一 URL 的多个请求应该返回同样的结果
            - 例：新闻站点的头版不断更新。虽然第二次请求会返回不同的一批新闻，该操作仍然被认为是安全的和幂等的，因为它总是返回当前的新闻。
            - 当用户打开一个链接时，他可以确信从自身的角度来看没有改变资源即可。
- POST
    - 参数放在 HTTP 包的 Body 中
        - 通过提交表单来传值，限制数据长度的是服务器处理程序的处理能力
    - 用于创建、更新资源(非幂等)
        - 服务器必须确保数据被保存好且只保存了一次
- PUT
    - 用于创建、更新资源(幂等)
        - 服务器可能触发多次储存过程而把旧的值覆盖掉
- DELETE
    - 用于删除给定位置的资源
- 在 HTML4 和 XHTML1 中，表单只能使用 GET 和 POST 方法
- 在 JavaScript 和未来的 HTML 标准中可以使用其他的方法