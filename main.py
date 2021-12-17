from datetime import datetime
import getopt
import re
import os
import sys
import pandas as pd
import scrapy
from scrapy.crawler import CrawlerProcess
from scraper.spiders.switchboard import SwitchboardSpider

USAGE_HINT = 'Usage:\npipenv run python main.py -i <inputfile> -o <outputfile> -c <inputcolumn>'

def readArgs():
    datenow = datetime.now()
    inputfile = 'input.txt'
    outputfile = datenow.strftime('result.%Y-%m-%d.%H%M%S.csv')
    logfile = datenow.strftime('log.%Y-%m-%d.%H%M%S.txt')
    inputcolumn = 'Names'  # default column name to be read from csv files
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hi:o:', ['ifile=','ofile='])
    except getopt.GetoptError:
        print(USAGE_HINT)
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print(USAGE_HINT)
            sys.exit()
        elif opt in ('-i', '--ifile'):
            inputfile = arg
        elif opt in ('-o', '--ofile'):
            outputfile = arg
        elif opt in ('-c', '--column'):
            inputcolumn = arg
    print('Input file:', inputfile)
    print('Output file:', outputfile)
    print('Log file:', logfile)
    print('---------------------------------------------')
    return inputfile, outputfile, inputcolumn, logfile

if __name__ == '__main__':
    try:
        # Setup File
        inputfile, outputfile, inputcolumn, logfile = readArgs()
        if not os.path.isfile(inputfile):
            print('Input file not found, please check your command.')
            print(USAGE_HINT)
            sys.exit()

        print('GENERATING URLS FROM INPUT FILE...')
        scientific_names = []
        if('.txt' in inputfile):
            with open(inputfile, 'r') as filehandle:
                scientific_names = [name.rstrip() for name in filehandle.readlines()]
        elif('.csv' in inputfile):
            scientific_names = pd.read_csv(inputfile)[inputcolumn].tolist()
        elif('.xlsx' in inputfile):
            scientific_names = pd.read_excel(inputfile)[inputcolumn].tolist()
        start_urls = []
        for name in scientific_names:
            name_to_search = re.sub(r'[^\w]', ' ', name).strip().replace(' ', '%20')
            start_urls.append(f'http://apps.worldagroforestry.org/products/switchboard/index.php/species_search/{name_to_search}')
        SwitchboardSpider.start_urls = start_urls

        print('RUNNING CRAWLER...')
        print('It may take a while, please wait...')
        process = CrawlerProcess(settings={
            'FEEDS': {
                outputfile: {
                    'format': 'csv',
                    'fields': [
                        'Query',
                        'Species Name',
                        'Scientific Name',
                        'Note',
                        'Switchboard',
                        'African Wood Density Database',
                        'Agroforestree Database',
                        'Genetic Resources Unit Database',
                        'RELMA-ICRAF Useful Trees',
                        'Tree Functional Attributes and Ecological Database',
                        'Tree Seed Suppliers Directory',
                        'Useful Tree Species for Africa Map',
                        'vegetationmap4africa'
                    ]
                },
            },
            'LOG_FILE': logfile,
        })
        process.crawl(SwitchboardSpider)
        process.start()
        print('Done!')
    except KeyboardInterrupt:
        print('Stopped!')
        sys.exit(0)
