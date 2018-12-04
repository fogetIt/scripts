##### 网址与 IP
每一个网站都有一个网址，每一个网址都对应着一个 IP 地址。访问一个网站，必须知道它的 IP 地址。

##### DNS 解析
通过 `DNS服务器（domain name server）` ，将网址还原成真实的 IP 地址，再通过 IP 地址去连接网站。

##### DNS 服务器有
- Google Public DNS
- OpenDNS

##### DNS 劫持和污染
以某种方式改变或者切断 `网址与IP地址` 的对应方式，就无法通过网址得到真实的 IP 访问网站。

##### hosts
- 优先使用 hosts 文件中记录的对应关系查询网址 IP
- 如果 hosts 没有要访问的网址，才去寻找 DNS 服务器
- DNS 劫持和污染，对 hosts 没有影响
- 文件位置
    - Windows: C:\Windows\System32\drivers\etc\hosts
    - Android: /system/etc/hosts
    - Mac/iOS: /etc/hosts
    - Linux: /etc/hosts
- 生效方法：插/拔网线、开/关飞行模式、重启网卡
