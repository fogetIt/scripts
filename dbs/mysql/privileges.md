### 查看权限
```sql
-- 查看当前用户权限
SHOW GRANTS;

-- 查看其他用户权限
SHOW GRANTS FOR 用户名@登录主机;
```

### 授权/解除授权
##### 直接授权/解除授权
```sql
-- 权限
--      SELECT/INSERT/DELETE/FILE/...
--      多个权限使用 , 分割
--      ALL PRIVILEGES/ALL 表示全部权限
-- 库.表
--      * 代表所有库或表
-- 登录主机
--      localhost/ip/hostname/域名
--      % 表示从任何地址连接
-- 密码
--      \"\"代表没有密码
-- WITH GRANT OPTION
--      被授权的用户，也可以将这些权限授给其他用户
GRANT 权限 ON 库.表 TO '用户名'@'登录主机' IDENTIFIED BY '密码' WITH GRANT OPTION;
-- 解除授权
RECOKE 权限 ON 表.库 FROM '用户名'@'登录主机';

FLUSH PRIVILEGES;
```

##### 修改 user 表
```sql
USE mysql;
UPDATE user SET host='登录主机' WHERE user='用户名';
DELETE FROM user WHERE user='用户名' and host='登录主机';

FLUSH PRIVILEGES;
```