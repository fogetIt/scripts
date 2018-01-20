##### flow
```
login: 客户端运行程序时自动与服务器建立连接。
logout: 客户端关闭时自动关闭与服务器的连接。
online: 服务器监听客户端的登录/退出，保存 {user_name: client_ip}, {client_ip: tcp_socket}，并广播在线用户列表。
transmit: 服务端监听用户发送的 json 数据，再进行广播/转发。
```

##### p2p flow(not safety)
```
服务器只保存用户名、客户端ip，客户端之间需要通话时，由服务器发送对方ip，帮助双方建立连接。
```

##### run
```shell
# run server
python server.py

# run client
sudo python client.pyw
```

##### wxPython 并发问题
```
wxPython
    wx.App.MainLoop() 用一个死循环来维持 GUI 界面
    GUI 操作必须发生在 主线程 或者 wx.App.MainLoop() 所在的线程
    所以，无法通过共用 class object 来更新 GUI
python threading
    只能利用到一个计算机核（只能同时干一件事）
    所以，如果线程工作时间过长，容易造成 GUI 界面卡死
python multiprocessing
    非 GUI 进程，无法更新 GUI

corrent way
    wx.CallAfter
        非 GUI 线程调用 GUI 线程
    wx.lib.pubsub.pub
        subscribe(callback, topicName)    发布订阅事件
        sendMessage(topicName, **kwargs)  发送全局消息，启动事件
```