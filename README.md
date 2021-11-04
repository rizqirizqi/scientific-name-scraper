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

<details>
   <summary>Detailed Guide for Windows</summary>

   1. Download python from https://www.python.org/downloads/
   2. Install python, follow the instruction
   3. Press Win button (something like window icon on keyboard), search "env", then open `Edit the system environment variables`
   4. Click Environment Variables
   5. On `System Variables` section, edit the `Path` key
   6. Add these paths using the `New` button:
      ```
      # Please replace the username with your windows username, you can see it in C:\Users folder
      # Please replace the python version with your installed python version
      C:\Users\<YOUR_USERNAME>\AppData\Local\Programs\Python\Python310
      C:\Users\<YOUR_USERNAME>\AppData\Local\Programs\Python\Python310\Scripts
      C:\Users\<YOUR_USERNAME>\AppData\Roaming\Python\Python310\Scripts
      ```
   7. Click OK, then OK
   8. Open cmd, then type `python --version`, then it should respond with the python version.
   9. Type `pip3 install --user pipenv`, then it should install pipenv, make sure it's successfully installed.
   10. Type `pipenv --version`, then it should respond with the pipenv version.
   11. Done! You can continue follow the guide in the "How to run" section.
</details>


## How to run
1. Clone
   ```sh
   git clone git@github.com:rizqirizqi/species-switchboard-scraper.git
   cd species-switchboard-scraper
   ```
2. Install dependencies
   ```sh
   pipenv --python 3
   pipenv install
   ```
3. Fill your input in `input.csv`, please look at `samples/input.csv` for example. You can also use txt or xlsx if you want.
4. Run
   ```sh
   pipenv run python main.py -i input.csv
   ```
5. The result will be placed in a file named `result.*.csv`

### Help
```sh
pipenv run python main.py --help
```

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
