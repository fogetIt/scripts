##### 查询
```sql
-- 列
--      多列
--          列1,列2,...
--      所有列
--          *
--      别名(AS 可以省略)
--          列1 AS 别名
--      或运算(存在数值类型返回 1)
--          列1 || 列2
--          列1 || num
--      DISTINCT
--          单独使用时，必须放在开头(列去重）
--          与其他函数使用时，没有位置限制(字段去重)
--      ABS(SUM(IF(表名.col=5, 表名.num, 0)))
--      FROM_UNIXTIME(表名.create_at, '%Y-%m-%d %H:%M:%S')
--          第一个参数是时间戳或者 DATE/DATETIME
--      UNIX_TIMESTAMP(NOW())
--          参数类型
--              一个 DATE/DATETIME 字符串
--              一个 DATE/DATETIME
--              一个 YYMMDD/YYYMMDD/YYYYMMDD 格式的数字
--      截取字符串
--          LEFT(表名.col,4)
--              截取左边指定长度字符
--          RIGHT(表名.col,4)
--              截取右边指定长度字符
--          SUBSTRING(表名.col,5,2)
--              截取特定位置指定长度字符
--              最后一个参数可以省略，截取到最后一个字符
--          字符串为 NULL ，返回 NULL
--          长度为 0 或 负，返回空
--          长度为 NULL ，返回 NULL
--      CONCAT(col1,col2,...)
--          连接字符串
--              任何一个参数为 NULL ，则返回 NULL
--              数字参数被变换为等价的字符串形式
--      GROUP_CONCAT(col)
--          连接一列字符串
--      CASE 语句
--          CASE 表名.col
--              WHEN 1 THEN 'xxx'
--              WHEN 2 THEN 'xxx'
--          ELSE '' END AS new_col
-- 条件语句
--      条件语句之间以 AND/OR/NOT 连接，优先级：NOT>AND>OR
--      限制范围(<> 在任何 SQL 中都起作用， != 在某些软件中是语法错误)
--          列名 =/!=/>/</>=/<= 值
--          列名 BETWEEN 值1 AND 值2
--          列名 IN (值1,值2,...)
--      正则匹配
--          列名 LIKE '_s%'         第二个字母是 s
--          列名 NOT LIKE '%张%'    不包含
--      空值检索
--          列名 IS NULL
-- 表名(AS 别名)
--      左(外)联查询以左表为主，表关系用 ON 建立
--          FROM `表1` b LEFT JOIN `表2` c ON 条件 WHERE 条件
--          FROM `表1` b LEFT OUUTER JOIN `表2` c ON 条件 WHERE 条件
--      右联(外)查询以右表为主，表关系用 ON 建立
--          FROM `表1` b RIGHT JOIN `表2` c ON 条件 WHERE 条件
--          FROM `表1` b RIGHT OUTER JOIN `表2` c ON 条件 WHERE 条件
--      全(内)联结联结查询，表名用逗号割开，表关系在 WHERE 中建立
--          FROM `表1` b,`表2` c WHERE 条件
--          FROM `表1` b INNER JOIN `表2` c WHERE 条件
-- 分组(可选)
--      GROUP BY 列1,列2,...
-- 排序(可选)
--      ORDER BY 列1 DESC,列2 ASC,...
-- 限定(可选)
--      给定一个参数：指定返回的最大行数
--          LIMIT num
--      给定两个参数：第一个参数指定第一行的偏移量，第二个参数指定返回的最大行数
--          LIMIT num1,num2
--      当确认查询条数时(如核对用户名密码)，加上 LIMIT ，避免全表扫描，提高查询效率
--      使用 limit 来查询，并且偏移量特别大时，会降低查询效率
SELECT 列 WHERE 条件语句 FROM 表名 分组 排序 限定;
```

#####　子查询，相当于左联

##### 变量
```sql
-- 声明
set @变量名=值;
-- 或者
set @变量名:=值;

-- 使用
SELECT * FROM 表名 WHERE 列名=@变量名;
SELECT @变量名:=列名 FROM `表名`;
```

##### 权重
```sql
SELECT
    *
FROM (
    SELECT
        h.id AS id_quan_zhong,
        o.name,
        CASE
            WHEN h.area >= 8.0 THEN 1
            ELSE 0
        END AS area_quanzhong,
    FROM house h JOIN office o ON h.office_id=o.id
    WHERE 条件
    ORDER BY id_quan_zhong+area_quanzhong DESC
)
AS house limit 0,20
```