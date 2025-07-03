from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

from scraper_utils import login_to_fxc

import os
import importlib
from countries import __path__ as countries_path
# from tts_analysis import __path__ as tts_analysis_path


# Get all scraper files in the countries/ folder
country_modules = []
for filename in os.listdir(countries_path[0]):
    if filename.endswith("_scraper.py"):
        module_name = filename[:-3]  # remove .py
        pretty_name = module_name.replace("_scraper", "").replace("_", " ").title()
        full_module = f"countries.{module_name}"
        module = importlib.import_module(full_module)
        country_modules.append((module, pretty_name))


# sending_countries = ['United States']
sending_countries = ['United States' ,'United Kingdom', 'France',  'Canada', 'Australia' ]
time_period = 0

def run_scraper(country_module, country_name):

    download_dir = f"/Users/ryanwh/Documents/pricing_data/tts_tracker_20250612/{country_name}"
    os.makedirs(download_dir, exist_ok=True)

    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }

    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument("--headless=new")



    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 20)

    login_to_fxc(driver, wait)  # shared login logic

    country_module.run(driver, wait, sending_countries, time_period)

    driver.quit()
    print(f"Done scraping {country_name}")


if __name__ == "__main__":
    for module, name in country_modules:
        print(f" Running scraper for {name}")
        run_scraper(module, name)

# if __name__ == "__main__":
    # for module, name in country_modules:
    #     print(f" Running scraper for {name}")
    #     run_scraper(india_scraper, 'India')
    # run_scraper(zimbabwe_scraper, 'Zimbabwe')
