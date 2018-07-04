# -*- coding: utf-8 -*-
import scrapy
import sys
from demo02.items import Demo02Item

reload(sys)
sys.setdefaultencoding('utf-8')

class LwcsspiderSpider(scrapy.Spider):
    name = 'demo02'
    # 允许爬虫的域名列表
    allowed_domains = ['www.bxwx3.org']

    # 爬虫启示页
    start_urls = ['http://www.bxwx3.org/txt/217331/1122576.htm']

    url = 'http://www.bxwx3.org/txt/217331/1122576.htm'

    def parse(self, response):
        item = Demo02Item()

        selector = scrapy.Selector(response)

        mainArticle = selector.xpath('//div[@id="neirongDiv"]')[0]

        titles = mainArticle.xpath('div[@class="bookname"]/h1/text()').extract()

        contents = mainArticle.xpath('div[@id="zjneirong"]/p/text() | div[@id="zjneirong"]/font/font/text() | div[@id="zjneirong"]/text()').extract()

        titles_text = []

        contents_text = []

        for title in titles:
            # print(title)
            temp_title = str(title).replace('\r\n', '')
            temp_title = temp_title.replace(' ', '')
            temp_title = temp_title.replace('　', '')
            
            if temp_title.isspace():
                continue
            if len(temp_title) == 0:
                continue
            titles_text.append(temp_title)

        for content in contents:
            # print(content)
            temp_content = str(content).replace('\r\n', '')
            temp_content = temp_content.replace(' ', '')
            temp_content = temp_content.replace('　', '')

            if temp_content.find('天才壹秒記住，為您提供精彩小說閱讀') != -1:
                continue
            if temp_content.isspace():
                continue
            if len(temp_content) == 0:
                continue

            contents_text.append(temp_content)

        item['title'] = titles_text

        item['content'] = contents_text

        item['href'] = self.url

        print('%s ==> %s' %(titles_text[0], self.url))

        yield item

        next_link = mainArticle.xpath('div[@class="bottem2"]/a[@id="xiaye"]/@href').extract()[0]

        next_link_atr = str(next_link)

        if next_link_atr and next_link_atr.endswith('.htm'):
            # print str(next_link)
            yield  scrapy.http.Request(str(next_link),callback=self.parse)  #递归调用并提交数据
