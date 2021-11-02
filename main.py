from datetime import datetime
from pathlib import Path
import scrapy
from scrapy.crawler import CrawlerProcess
from scraper.spiders.switchboard import SwitchboardSpider

if __name__ == "__main__":
    datenow = datetime.now()
    logfile = datenow.strftime('log.%Y-%m-%d.%H%M%S.txt')
    outputfile = datenow.strftime('result.%Y-%m-%d.%H%M%S.csv')
    print('Log File', logfile)
    print('Output File', outputfile)

    print('GENERATING URLS FROM CSV...')
    # TODO: import csv
    SwitchboardSpider.start_urls = [
        'http://apps.worldagroforestry.org/products/switchboard/index.php/species_search/Acacia%20abyssinica',
        'http://apps.worldagroforestry.org/products/switchboard/index.php/species_search/Parkia%20speciosa',
        'http://apps.worldagroforestry.org/products/switchboard/index.php/species_search/Animalia Asdasd'
    ]

    print('RUNNING CRAWLER...')
    print('It may take a while, please wait...')
    process = CrawlerProcess(settings={
        "FEEDS": {
            outputfile: {"format": "csv"},
        },
        "LOG_FILE": logfile,
    })
    process.crawl(SwitchboardSpider)
    process.start()
    print('Done!')