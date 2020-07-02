import scrapy
import json
import codecs
import datetime


def writeToFile(filename, text):
    with codecs.open(filename, 'w', 'utf-8') as outfile:
        outfile.write(text)

class MediumPost(scrapy.Spider):
    name = 'medium_scrapper'
    handle_httpstatus_list = [401, 400]

    autothrottle_enabled = True
    def start_requests(self):
        start_urls = ['https://www.medium.com/search/posts?q='+ self.searchString]

        cookie = cookie
        header = header

        for url in start_urls:
            yield scrapy.Request(url, headers = header, cookies = cookie, method='GET', callback = self.parse)

    def parse(self, response):
        response_data = response.text
        response_split = response_data.split("while(1);</x>")

        response_data = response_split[1]
        filename = 'medium.json'

        writeToFile(filename, response_data)

        with codecs.open(filename, 'r', 'uts-8') as infile:
            data = json.load(infile)

        if 'paging' in data['payload']:
            data = data['payload']['paging']

            if 'next' in data:
                print("In paging, Next Loop")
                data = data['next'] 

                formdata = {
                    'ignoredIds':data['ignoredIds'],
                    'page' : data['page'],
                    'pageSize' : data['pageSize']
                } 

                cookie = cookie
                header = header  
                yield scrapy.Request('https://www.medium.com/search/posts?q=' + self.seachString,method='GET',
                                        body=json.dumps(formdata), headers = header, cookies = cookie,
                                        callback=self.parse)

