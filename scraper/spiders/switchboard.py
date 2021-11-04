import scrapy

class SwitchboardSpider(scrapy.Spider):
    name = 'switchboard'
    allowed_domains = ['http://apps.worldagroforestry.org/']
    start_urls = []

    def parse(self, response):
        name_to_search = response.request.url.split('/')[-1].replace('%20', ' ')
        print('Looking up:', name_to_search)
        species_name = response.css('body > main > div:nth-child(2) > table tr:nth-child(2) td::text').get()
        species_dict = { 'Scientific Name': name_to_search }
        if species_name:
            species_dict['Found Species Name'] = species_name
            species_dict['Switchboard'] = response.request.url
        else:
            species_dict['Note'] = 'species_not_found'
        search_result = response.css('#linksWrapper > div')
        if len(search_result) > 0:
            icraflinks = search_result[0].css('h3::text')[0].get()
            if icraflinks == 'ICRAF Databases':
                tables = search_result[0].css('div > div')[0].css('table')
                for table in tables:
                    links = table.css('a')
                    for link in links:
                        if species_name in link.css('::text').get():
                            db_name = " ".join(table.css('th::text').get().strip().split())
                            species_dict[db_name] = link.css('::attr(href)').get()
            else:
                species_dict['Note'] = 'icraf_database_not_found'
        else:
            species_dict['Note'] = 'similar_species_found'
        return species_dict