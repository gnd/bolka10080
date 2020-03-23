# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import scrapy
import functions
import unicodedata

#curl -H "X-Requested-With: XMLHttpRequest" \
#--data "page=1&category=&type=vtipy&sort=najnovsie" \
#"https://www.rehot.sk/ajax/1"

class RehotSkSpider(scrapy.Spider):
    name = 'rehot_sk'
    domain = 'rehot.sk'
    curr_page = 1
    start_url = ''

    def __init__(self, maxpages=0, start_url='', delay=1.0, *args, **kwargs):
        super(RehotSkSpider, self).__init__(*args, **kwargs)
        self.start_url = start_url
        self.maxpages = int(maxpages)

    def start_requests(self):
        # 1 - 1078
        for i in range(1, self.maxpages):
            form_data = {'page': "%d" % i, 'category': '', 'type': 'vtipy', 'sort': 'najnovsie',}
            print "------ SCRAPING: %s page %d" % (self.start_url, i)
            yield scrapy.FormRequest(self.start_url, formdata=form_data, callback=self.parse)

    def parse(self, response):
        jokes = response.xpath('//div[@class="joke-content"]').extract()

        for i in range(len(jokes)):
            joke = jokes[i].encode('utf8').replace('<div class="joke-content">','').replace('</div>','')
            joke = functions.strip_accents(joke)
            joke = functions.clean_text(joke)

            # add to db
            yield {
                'domain': self.domain,
                'url': self.start_url,
                'joke': joke
            }
