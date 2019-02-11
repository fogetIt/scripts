##### 连接
```python
# coding: utf-8
import redis


pool = redis.ConnectionPool()
"""
管理对一个 redis server 的所有连接，避免每次建立、释放连接的开销
多个 Redis 实例共享一个连接池，线程安全
参数
    connection_class=Connection
    max_connections=None
    **connection_kwargs
"""


r = redis.StrictRedis()
"""
class StrictRedis(object) # 实现大部分官方命令，并使用官方的语法和命令
class Redis(StrictRedis)  # 用于向后兼容旧版本的 redis-py
参数
    connection_pool=None
    host='localhost'
    port=6379
    db=0
    password=None,
    socket_timeout=None
    socket_connect_timeout=None
    retry_on_timeout=False
    socket_keepalive=None
    socket_keepalive_options=None
    encoding='utf-8'
    encoding_errors='strict'
    charset=None
    decode_responses=False
    ssl=False
    ssl_keyfile=None
    ssl_certfile=None
    ssl_cert_reqs=None
    ssl_ca_certs=None,
    unix_socket_path=None
    max_connections=None
    errors=None
"""


# String API
# 将键值对存入 redis ，不存在则创建，存在则修改
"""
r.set(
    name,
    value,
    ex=None,   # 过期时间/秒
    px=None,   # 过期时间/毫秒
    nx=False,  # True， name 不存在时，才执行
    xx=False   # True， name 存在时，才执行
)
r.get(name)                     # -> value/None
r.getset(name, value)           # 设置新值并获取原来的值
r.setnx(name, value)            # 更新， name 不存在时，才执行
r.setex(name, value, time)      # 设置过期时间/秒
r.psetex(name, time_ms, value)  # 设置过期时间/毫秒
r.mset(*args, **kwargs)
r.mget(keys, *args)
r.getrange(key, start, end)     # 获取子序列(根据字节获取，非字符)
r.setrange(name, offset, value) # 修改字符串，从指定索引开始向后替换(新值太长时，向后添加)
"""


#  List API
"""
r.lpop(name)            # 移除左侧第一个元素并返回
r.rpop(name)
r.lpush(name, *values)  # 在最左边添加元素
r.rpush(name, *values)
"""


# Set API
"""
r.sismember(name, value)  # 检查 value 是否 name 集合成员
r.sadd(name, *values)
"""


#  hash Map API
"""
r.hset(name, key, value)  # 单个增加或修改 hash
"""
```

##### [参考](http://www.cnblogs.com/wangtp/p/5636872.html)
##### [参考](http://www.cnblogs.com/xiaoming279/p/6293583.htm)