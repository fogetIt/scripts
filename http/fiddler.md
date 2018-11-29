##### 简介：
- Edit
	- 复制信息
	- 移除捕获(Del、Ctrl+X)
	- 标识颜色
	- 解除编辑锁定(F2)
	- 查找会话
- Rules
	- 隐藏捕获
	- 为所有 Request/Response 加断点
	- 编辑规则(CustomRules.js)，取消编码
- Tool
	- 设置，清缓存，编码工具(TextWizard)
- View
	- 界面视图切换
- 监听开关——左下角 capturing (表示捕捉状态，F12)
	- 监听类型
		- 监听所有请求(All Processes)
		- 监听浏览器请求(Web Brosers)
		- 监听非浏览器请求(Nob-Broser)
		- 全部隐藏(Hide All)
- 命令行——监听开关上方
	- help
	- cls
		- Ctrl+X/清屏
	- select
		- 选择会话
	- ?.js
		- 选择js文件
	- bpu www.xxx/xxx
		- 暂停指定的 request(无参数时取消断点)
	- bpafter www.xxx/xxx
		- 暂停指定的 response (无参数时取消断点)
- 请求列表——左边栏
	- 结果/Result
	- 协议/Protocol
	- 主机名/Host
	- 网址/URL
	- 内容大小/Body
	- 缓存/Caching
	- 响应内容类型/Content-Type
	- 请求所运行的程序/Process
	- 注释/Comments
	- 自定义/Custom
- 请求数据流相关信息——右边
	- Statistics
		- 统计选中的一个或多个请求相关数据大小、耗时
	- Inspectors
		- Request/Response 的详细消息
	- AutoResponder
		- 自动回复器，设置一些规则将符合规则的请求指向本地
	- Composer
		- 创建发送 HTTP 请求
			- Parsed ---> POST:http://www.xxx/xxx
			- Parsed ---> GET:http://www.xxx/xxx
	- log
		- 日志信息
	- Filters
		- 设置会话过滤规则
	- Timeline
		- 网络请求时间轴



##### http header
- User-Agent: Fiddler
- 非 json
    + Content-Type:application/x-www-form-urlencoded;charset=utf-8
    + RequestBody(POST)
        * buildingname=外滩金融中心&coOSTct=lidaqing测试1232&contactphone=1223334444&houseprice=10&lvdiid=25&buildingno=25&floorno=25&houseno=255&key=ca9618f9882449e77b05f931a48898a0&begintime=2016-01-12 14:32:21
- json
    + Content-Type:application/json;charset=utf-8
    + RequestBody(POST)
        * {
            "buildingname":"嘉亭大厦",
            "contact":"mkk",
            "contactphone":12345678910,
            "houseprice":15,
            "lvdiid":"12",
            "buildingno":12,
            "floorno":12,
            "houseno":121,
            "key":"61c867242ba0bdda1339c2b4472af942"
        }
- Host: www.example.com————自动计算得出
- Content-Length: 163————由Options--->Fix Content-Length header自动计算得出
- Cookie: ***

### GET
- 获取cookie————打开网页，Inspectors -> Raw
- 在http头里追加cookie
- 在Parsed地址后面追加?parmas=***

application/xml ：在 XML RPC，如 RESTful/SOAP 调用时使用。
