import scrapy
from example.items import DouBanItem
from scrapy.linkextractors import LinkExtractor

class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['book.douban.com']
    #start_urls = ['https://book.douban.com/tag/%E5%B0%8F%E8%AF%B4']
    start_urls = ['https://book.douban.com/tag/%E7%BC%96%E7%A8%8B']

    def parse(self, response):
        item = DouBanItem()
        booklist = response.css('ul.subject-list') 
        bookinfos = booklist.css('div.info')
        for bookinfo in bookinfos:
            item['name'] = bookinfo.css('a::text').get().strip() 
            item['auth'] = bookinfo.css('div.pub::text').get().strip().split('/')[0]
            try:
                item['translator'] = bookinfo.css('div.pub::text').get().strip().split('/')[1] 
            except:
                item['translator'] = ""
            try:
                item['publisher'] = bookinfo.css('div.pub::text').get().strip().split('/')[-3]
            except:
                item['publisher'] = ""
            try:
                item['date'] = bookinfo.css('div.pub::text').get().strip().split('/')[-2]
            except:
                item['date'] = ""
            try:
                item['price'] = bookinfo.css('div.pub::text').get().strip().split('/')[-1]
            except:
                item['price'] = ""
            try:
                item['rating'] = bookinfo.css('span.rating_nums::text').get(default='not-found').strip() 
            except:
                item['rating'] = "none"
            try:
                item['hot'] = bookinfo.css('span.pl::text').re('\d+') 
            except:
                item['hot'] = ""
            try:
                item['url'] = bookinfo.css('a::attr(href)').get(default='not-found').strip() 
            except:
                item['url'] = ""
            yield item

        le = LinkExtractor(restrict_css='span.next')
        links = le.extract_links(response)
        if links[0].url:
            yield scrapy.Request(links[0].url, callback=self.parse)
