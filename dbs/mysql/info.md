```sql
-- 常用信息
SELECT VERSION();     -- 查看版本
SELECT CURRENT_DATE;  -- 查看当前日期
SELECT NOW();         -- 查看时间
SELECT USER();        -- 查看当前用户
SELECT VERSION(),CURRENT_DATE,NOW(),USER();
-- 库信息
SHOW DATABASES;                        -- 显示所有数据库
DROP DATABASE IF EXISTS `test`;        -- 删除数据库
CREATE DATABASE `test` IF NOT EXISTS;  -- 创建数据库
USE `test`;                            -- 选择数据库
SELECT DATABASE();                     -- 查询当前数据库
-- 表信息
DROP TABLE IF EXISTS `test`;              -- 删除表
-- 创建临时表(连接 MySQL 期间存在)
CREATE TEMPORARY TABLE IF NOT EXISTS test(id INT);
SHOW TABLES;                              -- 显示所有表
SHOW CREATE TABLE `test`;                 -- 显示建表 sql
SHOW COLUMNS FROM `test`;                 -- 显示所有的列属性
DESCRIBE `test`;
DESC `test`;
-- 修改表结构
ALTER TABLE test RENAME tb;                             -- 重命名表
ALTER TABLE tb ADD col CHAR(10);                        -- 增加列
ALTER TABLE tb MODIFY col CHAR(10) NOT NULL;            -- 修改列类型
ALTER TABLE tb CHANGE col col1 INT unsigned;            -- 修改列名和属性
ALTER TABLE tb ALTER col1 SET DEFAULT 0;                -- 修改列的默认值
ALTER TABLE tb ALTER col1 DROP DEFAULT;                 -- 删除列的默认值
ALTER TABLE tb DROP COLUMN col1;                        -- 删除列
ALTER TABLE tb DROP PRIMARY KEY;                        -- 删除主键
ALTER TABLE tb ADD PRIMARY KEY PK_depart_pos (col1,id); -- 增加主键
```