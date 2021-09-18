from selectorlib import Extractor
import requests 
import json 
from time import sleep
import csv
from dateutil import parser as dateparser

# Create an Extractor by reading from the YAML file


def scrape(url):    
    e = Extractor.from_yaml_file('selectors.yml')
    r = requests.get(url)
    print("scrapping the data")
    print(e.extract(r.text))
    return e.extract(r.text)

# content  = scrape(url)
# print(content)