##### 操作数据
```sql
-- 插入整行
INSERT INTO 表名 VALUES(值1,值2,...),...;
-- 插入指定列
INSERT INTO (列1,列2,...)　表名 VALUES(值1,值2,...),...;

-- 删除匹配行
DELETE FROM 表名 WHERE 条件;

-- 更新匹配行
--      LOW_PRIORITY
--          低优先级(确保读的速度)
--      IGNORE
--          更新语句不因异常中止(冲突行不更新)
UPDATE 表名 SET 列1=值1 WHERE 条件 LOW_PRIORITY IGNORE;
-- 将列增大 2 倍，再加 1
UPDATE 表名 SET 列1=列1*2,列1=列1+1 WHERE 条件;
-- 多表 UPDATE(不可以使用 ORDER BY/LIMIT)
UPDATE 表1,表2 SET 表１.列1=表2.列2 WHERE 条件;


UPDATE
    `pb_house` ph
SET
    create_id         =(SELECT create_id FROM `house` h WHERE h.Id=ph.house_id),
    create_name       =(SELECT create_name FROM `house` h WHERE h.Id=ph.house_id),
    investigator_id   =(SELECT investigator_accendant_id FROM `house` h WHERE h.Id=ph.house_id),
    investigator_name =(SELECT investigator_accendant_name FROM `house` h WHERE h.Id=ph.house_id);
-- 每 set 一次都有 select 整个 house ，效率低下
-- INNER JOIN...ON，在表间做关联更新和删除操作
UPDATE pb_house p
INNER JOIN (
    SELECT
        h.id,
        h.`investigator`,
        h.`investigator_name`,
        h.`create_id`,
        h.`create_name`
    FROM house h
    WHERE h.`Id`IN
    (
        SELECT p.`house_id` FROM pb_house p
    )
) h
ON p.`house_id` = h.id
SET
    p.create_id         = h.create_id,
    p.create_name       = h.create_name,
    p.investigator_id   = h.investigator_accendant_id,
    p.investigator_name = h.investigator_accendant_name;
```