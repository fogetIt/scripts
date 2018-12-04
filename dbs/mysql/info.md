```sql
-- 常用信息
SELECT VERSION();     -- 查看版本
SELECT CURRENT_DATE;  -- 查看当前日期
SELECT NOW();         -- 查看时间
SELECT USER();        -- 查看当前用户
SELECT VERSION(),CURRENT_DATE,NOW(),USER();
-- 库信息
SHOW DATABASES;                       -- 显示所有数据库
DROP DATABASE IF EXISTS `库名`;        -- 删除数据库
CREATE DATABASE `库名` IF NOT EXISTS;  -- 创建数据库
USE `库名`;                            -- 选择数据库
SELECT DATABASE();                    -- 查询当前数据库
-- 表信息
DROP TABLE IF EXISTS `表名`;     -- 删除表
CREATE TEMPORARY TABLE          -- 创建临时表(连接 MySQL 期间存在)
    IF NOT EXISTS 表名(id INT);
SHOW TABLES;                    -- 显示所有表
SHOW CREATE TABLE `表名`;        -- 显示建表 sql
SHOW COLUMNS FROM `表名`;        -- 显示所有的列属性
DESCRIBE `表名`;
DESC `表名`;
-- 修改表结构
ALTER TABLE 表名 RENAME 表名;                    -- 重命名表
ALTER TABLE 表名 ADD 列名 CHAR(10);              -- 增加列
ALTER TABLE 表名 DROP COLUMN 列名;               -- 删除列
ALTER TABLE 表名 MODIFY 列名 CHAR(10) NOT NULL;  -- 修改列类型
ALTER TABLE 表名 CHANGE 列1 列2 INT unsigned;    -- 修改列名和属性
ALTER TABLE 表名 ALTER 列名 SET DEFAULT 0;       -- 修改列的默认值
ALTER TABLE 表名 ALTER 列名 DROP DEFAULT;        -- 删除列的默认值

CREATE UNIQUE INDEX 索引名 ON 表名 (列名);  -- 创建唯一性索引
ALTER TABLE 表名 ADD UNIQUE(列名,...);     -- 增加唯一性索引(NULL/可重复)

ALTER TABLE 表名 ADD FULLTEXT 索引名 (列名);  -- 增加全文索引

CREATE INDEX 索引名 ON 表名 (列名,...);        -- 创建索引
ALTER TABLE 表名 ADD INDEX 索引名 (列名,...);  -- 增加索引
ALTER TABLE 表名 DROP INDEX 索引名;           -- 删除索引
DROP INDEX 索引名 ON 表名;

ALTER TABLE 表名 ADD PRIMARY KEY (列名);  -- 增加主键(NOT NULL/唯一)
ALTER TABLE 表名 DROP PRIMARY KEY;        -- 删除主键

ALTER TABLE 表名 ADD PRIMARY KEY PK_depart_pos (列名,...);  -- 增加复合主键
ALTER TABLE 表名 ADD CONSTRAINT 约束名 PRIMARY KEY(列名,...);  -- 增加复合约束
```