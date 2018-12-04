##### HTTP(HyperText Transfer Protocal)
- 超文本传输协议，基于 TCP 协议，从 Web 服务器传输超文本到本地浏览器的传送协议
- 从 1990 年开始在 WWW 上广泛应用，是现今在 WWW 上应用最多的协议
- 应用层协议，基于 Request/Response 模式的、无状态的协议
    - 客户端发送一个请求给服务器，服务器接收到请求后生成一个响应返回给客户端
    - 同一个客户端的这次请求和上次请求是没有对应关系
    - 对服务器来说，它并不知道这两个请求来自同一个客户端
        - 为了解决这个问题， Web 程序引入了 Cookie 机制来维护状态

##### Request
- 格式
    + request line
        * Method
            - 请求方法(POST/GET)当使用 GET 方法时， body 是为空的
        * Path-to-resoure
            - 请求的资源
        * Http/version-number
            - HTTP 协议的版本号
    + request header
        * 在 HTTP/1.1 中，除 Host 外，所有的请求头都是可选的
    + **header和body之间有个空行**
    + body
        - 可选的消息体
    - 请求行和标题必须以 <CR><LF> 作为结尾(回车然后换行)，空行内必须只有 <CR><LF> 而无其他空格

##### Response
- 格式
    + response line
        * Http/version-number
        * status-code
            - 状态码，告诉客户端服务器是否产生了预期的 Response
        * message
    + response header
    + **header和body之间有个空行**
    + body
        - 可选的消息体

##### URL(Uniform Resource Locator)
- 统一资源定位符——用于描述一个网络上的资源
- 基本格式：`schema://host[:port]/path/[?query-string][#anchor]`
    - scheme
        - 指定低层协议(http/https/ftp)
    - host
        - 服务器的 IP 地址或者域名(www.baidu.com)
    - port
        - 服务器的端口，默认是80
    - path
        - 访问资源的路径(/sj/test/test.aspx/)
    - query-string
        - 发送给服务器的数据(name=sviergn&x=true)
    - anchor
        - 锚(stuff)
- 例子：`http://www.mywebsite.com/sj/test/test.aspx?name=sviergn&x=true#stuff`

##### 缓存机制
- 缓存的目的
    - 在很多情况下减少发送请求
        - 用“过期(expiration)”机制来减少网络回路的数量
    - 在许多情况下可以不需要发送完整响应
        - 用“验证(validation)”机制来减少网络应用的带宽

##### 基于 HTTP 的应用
1. HTTP 代理
2. 多线程下载
    - 下载工具开启多个发出 HTTP 请求的线程
    - 每个 http 请求只请求资源文件的一部分：Content-Range: bytes 20000-40000/47000
    - 合并每个线程下载的文件