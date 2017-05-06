# -*- coding: utf-8 -*-
import re
from datetime import datetime

from scrapy import Spider, Request

from kylx.items import KylxItem


class HuakeSpider(Spider):
    name = "huake"
    allowed_domains = ["job.hust.edu.cn"]
    start_urls = ['http://job.hust.edu.cn/']

    pre_url = 'https://job.hust.edu.cn/searchJob_'
    suf_url = '.jspx?type=2&fbsj='
    root_url = "https://job.hust.edu.cn"
    max_page = 25

    relative_url_pattern = re.compile(r'/.{7}/\d{4,6}\.htm')
    title_pattern = re.compile(r'<a href="/.{7}/\d{4,6}\.htm" .*?>(.*?)</a>')
    time_pattern = re.compile(r'\d{4}-\d{1,2}-\d{1,2}')

    def start_requests(self):
        for i in range(1, self.max_page):
            url = ''.join([self.pre_url, str(i), self.suf_url])
            yield Request(url, callback=self.parse)

    def parse(self, response):
        if response.text is not None:
            relative_urls = re.findall(self.relative_url_pattern, response.text)
            titles = re.findall(self.title_pattern, response.text)
            times_ = re.findall(self.time_pattern, response.text)
            for j in range(len(times_)):
                title = titles[j]
                sub_url = ''.join([self.root_url, relative_urls[j]])
                time_ = times_[j]
                yield Request(sub_url, callback=self.parse_page,
                              meta={'url': sub_url, 'title': title, 'time': time_})

    def parse_page(self, response):
        kylxitem = KylxItem()
        content = response.xpath('//div[@class="Content"]').extract()[0]
        kylxitem['content'] = content
        kylxitem['url'] = response.meta['url']
        kylxitem['title'] = response.meta['title']
        _time = response.meta['time']
        kylxitem['start_date'] = datetime.strptime(_time, '%Y-%m-%d')
        kylxitem['start_milli'] = kylxitem['start_date'].timestamp()
        yield kylxitem
