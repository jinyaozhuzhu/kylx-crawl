# -*- coding: utf-8 -*-
import json
import re
from datetime import datetime

from scrapy import Spider, Request
from scrapy.http import FormRequest

from kylx.items import KylxItem


class WudaSpider(Spider):
    name = "wuda"
    allowed_domains = ["xsjy.whu.edu.cn"]
    start_urls = ['http://xsjy.whu.edu.cn/']
    max_page = 5
    root_url = 'http://xsjy.whu.edu.cn/zftal-web/zfjy!' \
               'wzxx!whdx10486/dwzpxx_cxWzDwzpxxAdwNryEX.html?doType=query'
    sub_url = 'http://xsjy.whu.edu.cn/zftal-web/zfjy!wzxx/' \
              'dwzpxx_cxWzDwzpxxNry.html?dwxxid='
    pattern_content = re.compile(r'<h3 style="bordepr-bottom:.*?</div>', re.S)

    def start_requests(self):
        for num in range(1, self.max_page):
            form_data = self.get_form_data(str(num))
            yield FormRequest(self.root_url, callback=self.parse,
                              formdata=form_data)

    def parse(self, response):
        try:
            data = json.loads(response.text)
            items = data['items']
            for item in items:
                kylx = KylxItem()
                kylx['career_name'] = item['zwmc']
                end_date_str = item['tdjzrq']
                kylx['end_date'] = datetime.strptime(end_date_str, '%Y-%m-%d')
                kylx['end_milli'] = kylx['end_date'].timestamp()
                kylx['title'] = item['dwmc']
                dwxxid = item['dwxxid']
                yield Request(''.join([self.sub_url, dwxxid]), callback=self.page,
                              meta={'kylx': kylx})
        except Exception as e:
            print("json解析出错", e)

    def page(self, response):
        kylx = response.meta['kylx']
        kylx['url'] = response.url
        content = re.findall(self.pattern_content, response.text)[0]
        kylx['content'] = content
        yield kylx

    def get_form_data(self, page_num):
        form_data = {
            'zpxldm': '02',
            'queryModel.currentPage': page_num,
            'queryModel.showCount': '20',
            'queryModel.sortName': 'zdzt desc, fbsj',
            'queryModel.sortOrder': 'desc'
        }
        return form_data
