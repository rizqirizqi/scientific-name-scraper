import scrapy

class SwitchboardSpider(scrapy.Spider):
    name = 'switchboard'
    allowed_domains = ['http://apps.worldagroforestry.org/']
    start_urls = []

    def parse(self, response):
        name_to_search = response.request.url.split('/')[-1].replace('%20', ' ')
        print('Looking up:', name_to_search)
        species_name = response.css('body > main > div:nth-child(2) > table tr:nth-child(2) td::text').get()
        if not species_name:
            self.logger.info('Species not found!')
        species_dict = { 'Scientific Name': species_name or name_to_search, 'Switchboard': response.request.url }
        search_result = response.css('#linksWrapper > div')
        if search_result:
            icraflinks = search_result[0].css('h3::text')[0].get()
            if icraflinks == 'ICRAF Databases':
                tables = search_result[0].css('div > div')[0].css('table')
                for index, table in enumerate(tables):
                    species_dict[table.css('th::text').get()] = table.css('a::attr(href)').get()
            else:
                self.logger.info('ICRAF Database section not found!')
        yield species_dict