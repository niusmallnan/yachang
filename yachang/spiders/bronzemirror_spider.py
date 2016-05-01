# -*- coding: utf-8 -*-
# Copyright 2016 Neunn, Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
import scrapy

from yachang.items import BronzeMirrorItem


class BronzeMirrorSpider(scrapy.Spider):

    name = "bronzemirror"
    allowed_domains = ["artron.net"]
    base_url = 'http://artso.artron.net/auction/search_auction.php?keyword=%E9%95%9C&Status=0&ClassCode=021301000000&page='
    cookies = {
        '_at_pt_0_': '1845312',
        '_at_pt_1_': 'QQ%E7%BD%91%E5%8F%8B1845312',
        '_at_pt_2_': '4d0667018a17dd3332a004437cf53c2a',
    }

    pattern1 = {
        u'尺寸': 'size',
        u'创作年代': 'create_age',
        u'拍卖时间': 'auction_date',
    }

    pattern2 = {
        u'专场': 'auction_session',
        u'拍卖公司': 'auction_company',
        u'拍卖会': 'auction_meet',
    }
    total_page = 282

    def __init__(self, *args, **kwargs):
        super(BronzeMirrorSpider, self).__init__(*args, **kwargs)
        for page in range(1, self.total_page+1):
            self.start_urls.append(self.base_url+str(page))

    def parse(self, response):
        for sel in response.xpath('//div[@class="listImg"]//div[@class="imgWrap"]//a/@href'):
            detail_link = sel.extract()
            yield scrapy.Request(response.urljoin(detail_link),
                                 cookies=self.cookies,
                                 callback=self.parse_detail)

    def parse_detail(self, response):
        item = BronzeMirrorItem()
        name = response.xpath('//h1/text()').extract_first()
        lot = name.split()[0]
        item['name'] = '-'.join(name.split())
        item['url'] = response.url
        item['id'] = response.url.split('-')[-1].replace('/', '')

        info_th_sel = response.xpath('//div[@class="worksInfo"]//th/text()')
        info_td_sel = response.xpath('//div[@class="worksInfo"]//td')
        for th_sel, td_sel in zip(info_th_sel, info_td_sel):
            key =  th_sel.extract()

            if key in self.pattern1.keys():
                item[self.pattern1[key]] = td_sel.xpath('.//text()').extract_first()

            if key in self.pattern2:
                item[self.pattern2[key]] = td_sel.xpath('.//a//text()').extract_first()

            if key == u'估价':
                _temp = td_sel.xpath('.//em/text()').extract_first().replace('\t',
                                                                        '').replace('\n',
                                                                        '').strip().split()
                item['valuation'] = ':'.join(_temp)

            if key == u'成交价':
                _vau_temp = [_t.strip() for _t in  td_sel.xpath('.//li/text()').extract()]
                item['deal'] = ':'.join('||'.join(_vau_temp).split())

            if key == u'说明':
                item['desc'] = ';'.join(td_sel.xpath('./text()').extract()).replace('\t', '').replace('\n', '').strip()

        year = item['auction_date'].split('-')[0]
        if int(year) <= 2008:
            year = 'old'
        path = item['id'].replace(lot, '')
        item['file_urls'] = 'http://img1.artron.net/auction/%s/%s/d/%s.jpg' % (year, path, item['id'])

        yield item

