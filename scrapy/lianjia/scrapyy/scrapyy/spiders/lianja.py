from scrapy import Spider, Request
from ..items import LianjiaItem
import json
from urllib.parse import quote


class LianjaSpider(Spider):
    name = 'lianjia'
    # allowed_domains = ['bj.lianjia.com']

    regions = {#'dongcheng': '东城'
               # 'xicheng': '西城'
               # 'chaoyang': '朝阳',
               # 'haidian': '海淀',
               # 'fangtai': '丰台',
               # 'shijingshan': '石景山',
               # 'tongzhou': '通州',
               'changping': '昌平'
               # 'daxing': '大兴',
               # 'yizhuangkaifaqu': '亦庄开发区',
               # 'shunyi': '顺义',
               # 'fangshan': '房山',
               # 'mentougou': '门头沟',
               # 'pinggu': '平谷',
               # 'huairou': '怀柔',
               # 'miyun': '密云',
               # 'yanqing': '延庆'
               }

    def start_requests(self):
        """以行政区为区分获取小区

        返回response: 行政区域下小区列表
        """
        for region in list(self.regions.keys()):
            url = "https://bj.lianjia.com/xiaoqu/" + region + "/"
            yield Request(url=url, callback=self.parse, meta={'region': region})

    def parse(self, response):
        """
        行政区域的小区页面有多个,但是无法通过获取下一页的链接进行递归获取
        只能获取该行政区域下展示小区的总页数,循环请求获取每一页
        :param response:
        :return:
        """
        region = response.meta['region']
        pages_to_parse = response.xpath('//div[@class="page-box house-lst-page-box"]/@page-data').get()
        pages = json.loads(pages_to_parse)
        total_pages = pages['totalPage']
        for i in range(int(total_pages)):
            url_page = "https://bj.lianjia.com/xiaoqu/{}/pg{}".format(region, str(i + 1))
            yield Request(url=url_page, callback=self.parse_xiaoqu, meta={'region': region})

    def parse_xiaoqu(self, response):
        """
        获取小区的专有id及名字
        :return:
        """
        ids = response.xpath('//li[@class="clear xiaoquListItem"]/@data-id').getall()
        names = response.xpath('//li[@class="clear xiaoquListItem"]/@data-id').getall()
        for cells in zip(ids, names):
            url = 'https://bj.lianjia.com/chengjiao/c{}/'.format(cells[0])
            xiaoqu_name = cells[1]
            yield Request(url=url,
                          callback=self.parse_chengjiao,
                          meta={'region': response.meta['region'], 'xiaoqu': xiaoqu_name, 'id': cells[0]})

    def parse_chengjiao(self, response):
        chengjiao_to_parse = response.xpath('//div[@class="page-box house-lst-page-box"]/@page-data').get()
        chengjiao_pages_json = json.loads(chengjiao_to_parse)
        chengjiao_total_pages = chengjiao_pages_json['totalPage']
        region = response.meta['region']
        xq_name = response.meta['xiaoqu']
        xq_id = response.meta['id']
        for i in range(int(chengjiao_total_pages)):
            url_page = "https://bj.lianjia.com/chengjiao/pg{}c{}/".format(str(i + 1), str(xq_id))
            yield Request(url=url_page, callback=self.parse_content, meta={'region': region, 'xq': xq_name})

    def parse_content(self, response):
        cj_list = response.xpath("//ul[@class='listContent']/li")
        for cj in cj_list:
            item = LianjiaItem()
            item['region'] = self.regions.get(response.meta['region'])
            href = cj.xpath('./a/@href')
            if not len(href):
                continue
            item['href'] = href[0].get()

            content = cj.xpath('.//div[@class="title"]/a/text()').get()
            if content:
                content_s = content.split()  # 按照空格分割成一个列表
                item['name'] = content_s[0]
                item['style'] = content_s[1]
                item['area'] = content_s[2]

            content_t = cj.xpath('.//div[@class="houseInfo"]/text()').get()
            if content_t:
                content = content_t.split('|')
                item['orientation'] = content[0]
                item['decoration'] = content[1]
                if len(content) == 3:
                    item['elevator'] = content[2]
                else:
                    item['elevator'] = '无'

            content_u = cj.xpath('.//div[@class="positionInfo"]/text()').get()
            if content_u:
                content = content_u.split()
                item['floor'] = content[0]
                if len(content) == 2:
                    item['build_year'] = content[1]
                else:
                    item['build_year'] = '无'

            content_v = cj.xpath('.//div[@class="dealDate"]/text()').get()
            if content_v:
                item['sign_time'] = content_v

            content = cj.xpath('.//div[@class="totalPrice"]/span/text()').get()
            if content:
                item['total_price'] = content

            content = cj.xpath('.//div[@class="unitPrice"]/span/text()').get()
            if content:
                item['unit_price'] = content

            content = cj.xpath('.//span[@class="dealHouseTxt"]/span/text()').get()  # 返回的是一个字符串列表
            if content:
                item['fangchan_class'] = content

            yield item













