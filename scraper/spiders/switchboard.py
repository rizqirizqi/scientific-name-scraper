import scrapy

class SwitchboardSpider(scrapy.Spider):
    name = 'switchboard'
    allowed_domains = ['http://apps.worldagroforestry.org/']
    start_urls = []

    def log_note(self, species_dict, note):
        if not species_dict.get('Note'): species_dict['Note'] = note

    def parse(self, response):
        name_to_search = response.request.url.split('/')[-1].replace('%20', ' ')
        print('Looking up:', name_to_search)
        species_dict = { 'Scientific Name': name_to_search }

        # Parse species name
        species_name = response.css('body > main > div:nth-child(2) > table tr:nth-child(2) td::text').get()
        if not species_name:
            self.log_note(species_dict, 'species_not_found')
            return species_dict
        species_dict['Found Species Name'] = species_name
        species_dict['Switchboard'] = response.request.url

        # Parse search result
        search_result = response.css('#linksWrapper > div')
        if len(search_result) <= 0:
            self.log_note(species_dict, 'similar_species_found')
            return species_dict

        # Parse ICRAF Databases table
        icraflinks = search_result[0].css('h3::text')[0].get()
        if icraflinks != 'ICRAF Databases':
            self.log_note(species_dict, 'icraf_database_not_found')
            return species_dict
        tables = search_result[0].css('div > div')[0].css('table')
        if len(tables) <= 0:
            self.log_note(species_dict, 'icraf_database_not_found')
            return species_dict
        
        # Parse links
        for table in tables:
            links = table.css('a')
            for link in links:
                if species_name in link.css('::text').get():
                    db_name = " ".join(table.css('th::text').get().strip().split())
                    species_dict[db_name] = link.css('::attr(href)').get()

        return species_dict