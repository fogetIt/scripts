-- 1
-- SET PASSWORD for 'root'@'localhost' = PASSWORD('mysql_12315_test');
-- 2
SET PASSWORD = PASSWORD('mysql_12315_test');
-- 3
-- UPDATE user SET PASSWORD=PASSWORD("mysql_12315_test") WHERE user='root';
ALTER USER 'root'@'localhost' PASSWORD EXPIRE NEVER;
CREATE DATABASE test;
-- CREATE USER 'test'@'%' IDENTIFIED BY 'mysql_12315_test';
GRANT ALL PRIVILEGES ON test.* TO 'test'@'%' IDENTIFIED BY 'mysql_12315_test';
FLUSH PRIVILEGES;