# Agroforestry Species Switchboard 2.0 Scraper

[![contributions welcome][contrib-badge]][contrib-url]
[![MIT License][license-badge]][license-url]

[![Watch on GitHub][github-watch-badge]][github-watch]
[![Star on GitHub][github-star-badge]][github-star]
[![Tweet][twitter-badge]][twitter]

Scrape plants scientific name information from [Species Switchboard 2.0](http://apps.worldagroforestry.org/products/switchboard).

## Requirements
- [python >= 3.10](https://www.python.org/downloads/) (you can use [pyenv](https://github.com/pyenv/pyenv) for easier python version management)
- [pipenv](https://github.com/pypa/pipenv)

## How to run
1. Install dependencies
   ```python
   cp env.sample .env
   pipenv --python 3
   pipenv install
   ```
3. Run
   ```sh
   pipenv run python main.py
   ```
4. The result will be placed in a file named `result.*.csv`

### Test Shell
```sh
pipenv run scrapy shell 'http://apps.worldagroforestry.org/products/switchboard/index.php/species_search/Acacia%20abyssinica'
```

### Cleanup All Outputs
```sh
rm result.* && rm log.*
```

### Special Cases
| Case | Link | Note |
|---|---|---|
| ICRAF Databases Not Found | [Engelhardia spicata](http://apps.worldagroforestry.org/products/switchboard/index.php/species_search/Engelhardia%20spicata) |
| Genus Found | [Forficula](http://apps.worldagroforestry.org/products/switchboard/index.php/species_search/Forficula) | What to do next? |
| Multiple Species Found | [Alstonia spectabilis](http://apps.worldagroforestry.org/products/switchboard/index.php/species_search/Alstonia%20spectabilis) | Get the matched species right? |
| Species Variant Found | [Engelhardtia spicata](http://apps.worldagroforestry.org/products/switchboard/index.php/species_search/Engelhardtia%20spicata) | Need human to check |
| Similar Species Found | [Costus speciosus](http://apps.worldagroforestry.org/products/switchboard/index.php/species_search/Costus%20speciosus) | Need human to check |

## Contributing
1. Fork this repo
2. Develop
3. Create pull request
4. Tag [@rizqirizqi](https://github.com/rizqirizqi) for review
5. Merge~~

## License

GPL-3.0

[contrib-badge]: https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat-square
[contrib-url]: https://github.com/rizqirizqi/species-switchboard-scraper/issues
[license-badge]: https://img.shields.io/npm/l/webpconvert.svg?style=flat-square
[license-url]: https://github.com/rizqirizqi/webpconvert/blob/master/LICENSE

[github-watch-badge]: https://img.shields.io/github/watchers/rizqirizqi/species-switchboard-scraper.svg?style=social
[github-watch]: https://github.com/rizqirizqi/species-switchboard-scraper/watchers
[github-star-badge]: https://img.shields.io/github/stars/rizqirizqi/species-switchboard-scraper.svg?style=social
[github-star]: https://github.com/rizqirizqi/species-switchboard-scraper/stargazers
[twitter]: https://twitter.com/intent/tweet?text=Scrape%20plants%20scientific%20name%20information%20from%20Agroforestry%20Species%20Switchboard%202.0.%20https%3A%2F%2Fgithub.com%2Frizqirizqi%2Fspecies-switchboard-scraper
[twitter-badge]: https://img.shields.io/twitter/url/https/github.com/rizqirizqi/species-switchboard-scraper.svg?style=social
