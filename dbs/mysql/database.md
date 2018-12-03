##### 删除数据库
```bash
mysqladmin drop database 库名
```

##### 补全插件
```bash
sudo pip install mycli
mycli -u root -p
```


##### 执行 sql 脚本
```bash
mysql -h localhost -u root -p'xxx' < xx/xx.sql
```
```sql
# sql 脚本可以通过 source 互相调用
source xx/xx.sql
```

##### 备份/恢复
```bash
# 备份数据库
mysqldump -u root -p'xxx' 库名 > xxx/backup.sql
: <<'COMMIT'
-d, --no-data    　　　　 只导出表结构
-t, --no-create-info     只导出数据
--databases     　　　　  导出表结构和数据
-w, --where=条件         根据条件导出
COMMIT

# 恢复数据库
mysqladmin -u root -p'xxx' CREATE 库名
mysql -u root -p 库名 < xxx/backup.sql
# 或者登录 mysql 之后 source xxx/backup.sql;
```

##### 从文本向数据库导入数据
```bash
# 将文件导入到和同名的表里
mysqlimport -u root -p'xxx' 库名 'xx/xx.txt' --columns='列1,列2,...' --local
: << 'COMMIT'
-d, --delete        新数据导入之前删除数据表中的所有信息
-f, --force         不管是否遇到错误，强制继续插入数据
-i, --ignore        跳过或者忽略那些有相同唯一关键字的行
-l, -lock-tables    数据被插入之前锁住表，防止了在更新数据库时，用户的查询和更新受到影响
-r, -replace        与 -i 选项的作用相反，覆盖表中有相同唯一关键字的行
-v　　　　　　　　　　　显示版本
-p　　　　　　　　　　　提示输入密码
--fields-enclosed-by=name      指定数据以什么符号被括起，很多情况下数据以双引号括起。默认没有被括起
--fields-terminated-by=name    指定字段之间的分隔符，在句号分隔的文件中，分隔符是句号。默认为 Tab 。
--lines-terminated-by=name     指定行之间的分隔符。默认为换行符。
COMMIT
```
```sql
LOAD DATA INFILE 文件名 INTO 表名(列1,列2,...);
```