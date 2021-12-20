import scrapy


class SwitchboardSpider(scrapy.Spider):
    name = "switchboard"
    allowed_domains = ["apps.worldagroforestry.org/"]
    start_urls = []
    replace_link_with_apps = [
        "African Wood Density Database",
        "Agroforestree Database",
        "RELMA-ICRAF Useful Trees",
    ]

    def log_note(self, species_dict, note):
        if not species_dict.get("Note"):
            species_dict["Note"] = note

    def parse(self, response):
        query = response.request.url.split("/")[-1]
        name_to_search = query.replace("%20", " ")
        print("Looking up:", name_to_search)
        species_dict = {
            "Query": name_to_search,
            "Switchboard": "NA",
            "African Wood Density Database": "NA",
            "Agroforestree Database": "NA",
            "Genetic Resources Unit Database": "NA",
            "RELMA-ICRAF Useful Trees": "NA",
            "Tree Functional Attributes and Ecological Database": "NA",
            "Tree Seed Suppliers Directory": "NA",
            "Useful Tree Species for Africa Map": "NA",
            "vegetationmap4africa": "NA",
        }

        # Parse species name
        matched_species = response.css(
            "body > main > div:nth-child(2) > table tr:nth-child(2) td:nth-child(2)"
        )
        species_name = matched_species.css("a::text").get().strip()
        author = matched_species.xpath("text()").get().strip()
        scientific_name = f"{species_name} {author}".strip()
        if not species_name:
            self.log_note(species_dict, "species_not_found")
            return species_dict
        species_dict["Species Name"] = species_name
        species_dict["Scientific Name"] = scientific_name
        species_dict["Switchboard"] = response.request.url
        if len(name_to_search.split()) == 1:
            self.log_note(species_dict, "genus_found")
            return species_dict
        if name_to_search != species_name:
            self.log_note(species_dict, "similar_species_found")

        # Parse search result
        search_result = response.css("#linksWrapper > div")
        if len(search_result) <= 0:
            name_like_page = f"http://apps.worldagroforestry.org/products/switchboard/index.php/name_like/{query}"
            return scrapy.Request(name_like_page, callback=self.parse, dont_filter=True)

        # Parse ICRAF Databases table
        icraflinks = search_result[0].css("h3::text")[0].get()
        if icraflinks != "ICRAF Databases":
            self.log_note(species_dict, "icraf_database_not_found")
            return species_dict
        tables = search_result[0].css("div > div")[0].css("table")
        if len(tables) <= 0:
            self.log_note(species_dict, "icraf_database_not_found")
            return species_dict

        # Parse links
        for table in tables:
            links = table.css("a")
            is_link_found = False
            for link in links:
                if species_name in link.css("::text").get():
                    db_name = " ".join(table.css("th::text").get().strip().split())
                    species_dict[db_name] = link.css("::attr(href)").get()
                    if db_name in self.replace_link_with_apps:
                        species_dict[db_name] = (
                            link.css("::attr(href)").get().replace("www.", "apps.")
                        )
                    if is_link_found:
                        self.log_note(species_dict, "duplicate_link_found")
                    is_link_found = True

        return species_dict
