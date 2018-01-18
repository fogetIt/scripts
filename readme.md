##### knowledge
```
主线程全局变量，被所有子线程共享。
子线程全局变量，在每个子线程中各自独立。

SimpleSpider 单线程爬虫
    顺序地请求 url

ThreadSpider 多线程爬虫
    通过 类的实例 来创建线程， 类变量 是共享的， 实例变量 互不影响。
    I/O 密集型任务下， cpu 定时切换到其他线程，节省网络 I/O 等待时间。

GeventSpider
    gevent.monkey.patch_socket()
        在等待网络IO操作时，gevent 自动切换
    gevent.sleep()
        交出控制权，让 greenlet 交替运行（手动切换）

sp.main(sp)
    在类中使用装饰器，调用函数时，需要传递实例对象作为参数
```
