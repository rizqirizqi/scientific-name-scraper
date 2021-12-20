from datetime import datetime
import getopt
import re
import os
import sys
import pandas as pd
from scrapy.crawler import CrawlerProcess
from scraper.spiders.switchboard import SwitchboardSpider
from scraper.spiders.wfo import WfoSpider

USAGE_HINT = "\
USAGE:\n\
pipenv run python -m sciscraper <OPTIONS>\n\
\n\
OPTIONS:\n\
    -s <source>                 | Set data source. Available source: SWITCHBOARD, WFO\n\
    -i <inputfile>              | Set input file\n\
    -o <outputfile>             | Set output file\n\
    -c <inputcolumn>            | Set name column from input csv/xlsx\n\
\n\
EXAMPLES:\n\
    Normal usage:           pipenv run python -m sciscraper -i samples/input.csv -o output.csv\n\
    Set data source:        pipenv run python -m sciscraper -i samples/input.csv -o output.csv -s WFO\n\
    Set id and name column: pipenv run python -m sciscraper -i samples/input.csv -o output.csv -c ScientificName\n\
    Show help message:      pipenv run python -m sciscraper -h\n\
"


def readArgs():
    datenow = datetime.now()
    inputfile = "input.txt"
    outputfile = datenow.strftime("result.%Y-%m-%d.%H%M%S.csv")
    source = "ALL"
    logfile = datenow.strftime("log.%Y-%m-%d.%H%M%S.txt")
    inputcolumn = "Names"  # default column name to be read from csv files
    try:
        opts, args = getopt.getopt(
            sys.argv[1:], "hi:o:s:c:", ["ifile=", "ofile=", "source=", "column="]
        )
    except getopt.GetoptError:
        print(USAGE_HINT)
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(USAGE_HINT)
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-s", "--source"):
            source = arg.upper()
        elif opt in ("-c", "--column"):
            inputcolumn = arg
    print("Input file:", inputfile)
    print("Output file:", outputfile)
    if source != "ALL":
        print(f"Source: {source}")
    if inputcolumn:
        print(f"Name Column: {inputcolumn}")
    print("Log file:", logfile)
    print("---------------------------------------------")
    return inputfile, outputfile, source, inputcolumn, logfile


def run_crawlers(spiders, scientific_names):
    for spider in spiders:
        if not spider["enabled"]:
            continue
        start_urls = []
        for name in scientific_names:
            name_to_search = re.sub(r"[^\w]", " ", name).strip().replace(" ", "%20")
            start_urls.append(spider["url"].format(name_to_search))
        spider["class"].start_urls = start_urls
        process = CrawlerProcess(
            settings={
                "FEEDS": {
                    outputfile: {"format": "csv", "fields": spider["fields"]},
                },
                "LOG_FILE": logfile,
            }
        )
        process.crawl(spider["class"])
        process.start()


if __name__ == "__main__":
    try:
        # Setup File
        inputfile, outputfile, source, inputcolumn, logfile = readArgs()
        if not os.path.isfile(inputfile):
            print("Input file not found, please check your command.")
            print(USAGE_HINT)
            sys.exit()
        if source not in ["SWITCHBOARD", "WFO"]:
            print("[Error] Available sources: SWITCHBOARD, WFO")
            sys.exit(2)

        print("GENERATING URLS FROM INPUT FILE...")
        scientific_names = []
        if ".txt" in inputfile:
            with open(inputfile, "r") as filehandle:
                scientific_names = [name.rstrip() for name in filehandle.readlines()]
        elif ".csv" in inputfile:
            scientific_names = pd.read_csv(inputfile)[inputcolumn].tolist()
        elif ".xlsx" in inputfile:
            scientific_names = pd.read_excel(inputfile)[inputcolumn].tolist()

        print("RUNNING CRAWLERS...")
        print("It may take a while, please wait...")
        spiders = [
            {
                "class": SwitchboardSpider,
                "url": "http://apps.worldagroforestry.org/products/switchboard/index.php/species_search/{}",
                "fields": [
                    "Query",
                    "Species Name",
                    "Scientific Name",
                    "Note",
                    "Switchboard",
                    "African Wood Density Database",
                    "Agroforestree Database",
                    "Genetic Resources Unit Database",
                    "RELMA-ICRAF Useful Trees",
                    "Tree Functional Attributes and Ecological Database",
                    "Tree Seed Suppliers Directory",
                    "Useful Tree Species for Africa Map",
                    "vegetationmap4africa",
                ],
                "enabled": source in ["ALL", "SWITCHBOARD"],
            },
            {
                "class": WfoSpider,
                "url": "http://www.worldfloraonline.org/search?query={}&view=&limit=5&start=0&sort=",
                "fields": [
                    "Query",
                    "Source",
                    "Source Key",
                    "Status",
                    "Rank",
                    "Accepted Name",
                    "Scientific Name",
                    "Canonical Name",
                    "Authorship",
                    "Kingdom",
                    "Phylum",
                    "Class",
                    "Order",
                    "Family",
                    "Genus",
                    "Species",
                    "Threat Status",
                    "URL",
                    "Search URL",
                ],
                "enabled": source in ["ALL", "WFO"],
            },
        ]
        run_crawlers(spiders, scientific_names)
        print("Done!")
    except KeyboardInterrupt:
        print("Stopped!")
        sys.exit(0)
