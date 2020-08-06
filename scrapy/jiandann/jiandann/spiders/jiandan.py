import scrapy
from jiandann.items import JiandanItem

class jiandanSpider(scrapy.Spider):
    name = 'jiandan'
    start_urls = ["http://jandan.net/ooxx"]

    def parse(self, response):

        item = JiandanItem()
        item['image_urls'] = response.xpath('//a[@class="view_img_link"]/@href').re('\/\/(.*)')
        yield item
       
        url = "http://" + response.css('a.previous-comment-page::attr(href)').re('\/\/(.*)')[0]
        if url:
            yield scrapy.Request(url, callback=self.parse)
