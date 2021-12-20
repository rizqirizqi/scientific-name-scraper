import scrapy
from urllib.parse import urlparse, parse_qs

class WfoSpider(scrapy.Spider):
    name = "wfo"
    allowed_domains = ["www.worldfloraonline.org/"]
    start_urls = []

    def log_note(self, species_dict, note):
        if not species_dict.get("Note"):
            species_dict["Note"] = note

    def parse(self, response):
        query = parse_qs(urlparse(response.request.url).query)["query"][0]
        name_to_search = query.replace("+", " ")
        print("Looking up:", name_to_search)

        # Parse species name
        results = response.css("#results > table tr")
        for result in results:
            species_dict = {
                "Query": name_to_search,
                "Source": "WFO",
                "Source Key": "NA",
                "Status": "NA",
                "Rank": "NA",
                "Accepted Name": "NA",
                "Scientific Name": "NA",
                "Canonical Name": "NA",
                "Authorship": "NA",
                "Kingdom": "PLANTAE",
                "Phylum": "",
                "Class": "",
                "Order": "NA",
                "Family": "NA",
                "Genus": "NA",
                "Species": "NA",
                "Threat Status": "",
                "URL": "NA",
                "Search URL": "NA",
            }
            data_col = result.css("td:nth-child(2)")
            species_url_path = data_col.css("a::attr(href)").get().split(";")[0]
            species_dict["Source Key"] = species_url_path.split("/")[2]
            species_dict["Status"] = data_col.css("#entryStatus::text").get().strip().split()[0].upper()
            species_dict["Rank"] = data_col.css("#entryRank::text").get().strip().split()[0].upper()
            species_name = data_col.css("h4 em::text").get().strip()
            author = data_col.css("h4 strong::text").get()
            if not author:
                author = data_col.css("h4::text").get()
            author = author.strip()
            scientific_name = f"{species_name} {author}".strip()
            if species_dict["Status"] == "ACCEPTED":
                species_dict["Accepted Name"] = scientific_name
            elif species_dict["Status"] == "SYNONYM":
                accepted_species = data_col.css("div a em::text").get().strip()
                accepted_author = data_col.css("div a em::text").get().strip()
                accepted_name = f"{accepted_species} {accepted_author}".strip()
                species_dict["Accepted Name"] = accepted_name
            species_dict["Scientific Name"] = scientific_name
            species_dict["Canonical Name"] = species_name
            species_dict["Authorship"] = author
            info = data_col.css('div::text')
            species_dict["Family"] = data_col.css('div::text')[0].get().strip()
            if len(info) > 1:
                species_dict["Order"] = data_col.css('div::text')[1].get().strip()
            species_dict["Genus"] = species_name.split()[0]
            species_dict["Species"] = species_name
            species_dict["URL"] = f"http://www.worldfloraonline.org/taxon/{species_url_path}"
            species_dict["Search URL"] = response.request.url
            yield species_dict
