# -*- coding: utf-8 -*-
# @Date:   2017-08-08 14:19:14
# @Last Modified time: 2017-08-13 19:45:09
__author__ = 'zdd'

# 起始url
start_urls = [
    {
        "url": "http://data.10jqka.com.cn/rank/cxd/",
        "code": "gbk"
    }
]
cxd_type = "4"
xd_type = "月"


# 多级爬取规则
def parser(p):
    if p.is_default_level():
        xpath = p.html_selector().xpath

        pages = xpath("//div[@class='m-page J-ajax-page']/a/@page").text_all()
        for i in pages:
            if i.isdigit():
                _url = start_urls[0].get("url")
                url = _url + "board/%s/field/stockcode/order/asc/page/%s/ajax/1/" % (cxd_type, i)
                p.add_req(url, code="gbk", ext_data={"xd_type": xd_type})

        trs = xpath("//tbody/tr").text_all()
        for i in trs:
            xpath = p.html_selector(text=i).xpath
            stock_num = xpath("//td[2]/a/text()").text().strip()
            stock_name = xpath("//td[3]/a/text()").text().strip()
            zhang_die_fu = xpath("//td[4]/text()").text().strip()
            huan_shou_lv = xpath("//td[5]/text()").text().strip()
            zui_xin_jia = xpath("//td[6]/text()").text().strip()
            qian_qi_di_dian = xpath("//td[7]/text()").text().strip()
            qian_qi_di_dian_ri_qi = xpath("//td[8]/text()").text().strip()
            if stock_num:
                p.put({
                    "key_id": stock_num,
                    "xd_type": xd_type,
                    "stock_num": stock_num,
                    "stock_name": stock_name,
                    "zhang_die_fu": zhang_die_fu,
                    "huan_shou_lv": huan_shou_lv,
                    "zui_xin_jia": zui_xin_jia,
                    "qian_qi_di_dian": qian_qi_di_dian,
                    "qian_qi_di_dian_ri_qi": qian_qi_di_dian_ri_qi
                })
                url = xpath("//td[2]/a/@href").text().strip()
                p.add_req(
                    url,
                    level="detail",
                    code="utf-8",
                    ext_data={"key_id": stock_num}
                )

    elif p.is_level("detail"):
        xpath = p.html_selector().xpath
        company_details_dict = {}
        company_details = xpath("//dl[@class='company_details']").text()
        dts = p.html_selector(text=company_details).xpath(
            "//dd/preceding-sibling::*[1]/text()").text_all()
        dds = p.html_selector(text=company_details).xpath(
            "//dt/following-sibling::*[1]/text()|//dt/following-sibling::*[1]/a/text()").text_all()
        for i, dt in enumerate(dts):
            # print dt.strip("： "), dds[i].strip()
            company_details_dict.update({
                dt.strip("： "): dds[i].strip()
            })

        news_list = xpath("//ul[@class='news_list stat']").text_all()
        if news_list:
            company_news = p.html_selector(text=news_list[0]) \
                .xpath("//li/span[1]/a/text()").text_all()
            company_news_list = [i.strip() for i in company_news]

            company_notice = p.html_selector(text=news_list[1]) \
                .xpath("//li/span[1]/a/text()").text_all()
            company_notice_list = [i.strip() for i in company_notice]

            industry_info = p.html_selector(text=news_list[2]) \
                .xpath("//li/span[1]/a/text()").text_all()
            industry_info_list = [i.strip() for i in industry_info]

            research_report = p.html_selector(text=news_list[3]) \
                .xpath("//li/span[1]/a/text()").text_all()
            research_report_list = [i.strip() for i in research_report]
            p.put({
                "key_id": p.get_ext("key_id"),
                "company_details_dict": company_details_dict,
                "company_news_list": company_news_list,
                "company_notice_list": company_notice_list,
                "industry_info_list": industry_info_list,
                "research_report_list": research_report_list,
            })
