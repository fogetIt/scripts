/*
* @Date:   2017-02-16 15:20:48
* @Last Modified time: 2018-01-08 16:54:15
*/
select * from(
    (
    SELECT
        oc.id AS openCustomerId,
        oc.`customer_name`,
        oc.city_id,
        oc.city_name,
        oc.`district_id`,
        oc.`district_name`,
        oc.`circle_id`,
        oc.`circle_name`,
        oc.`order_area_begin`,
        oc.`order_area_end`,
        oc.`order_price_begin`,
        oc.`order_price_end`,
        '' AS tag,
        '未接单' AS isAccept,
        oc.create_at,
        ocs.end_at
    FROM `open_customer_send` ocs
    LEFT JOIN `open_customer` oc ON ocs.`customer_id`=oc.`id`
    where ocs.user_id = 666753
    )
    UNION
    (
    select
        oc.id AS openCustomerId,
        oc.`customer_name`,
        oc.city_id,
        oc.city_name,
        oc.`district_id`,
        oc.`district_name`,
        oc.`circle_id`,
        oc.`circle_name`,
        oc.`order_area_begin`,
        oc.`order_area_end`,
        oc.`order_price_begin`,
        oc.`order_price_end`,
        ouc.tag,
        case ouc.`systemresource` when 0 then '接单' when 1 then '私客' else '' end AS isAccept,
        oc.create_at,
        0 AS end_at
    from `open_user_customer` ouc
    left join `open_customer` oc on ouc.`open_customer_id`=oc.`id`
    where ouc.user_id = 666753
    order by oc.create_at DESC
    )
)
AS temp
-- group by写在最外层才能生效
group by temp.end_at desc, temp.create_at desc;