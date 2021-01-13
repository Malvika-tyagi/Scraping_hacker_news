import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import time
from pymongo import MongoClient
import re

def get_image(html_soup):
    images = html_soup.find_all('img', {'src':re.compile('.jpg')})
    image_set = []
    for image in images:
        a = image['src']+'\n'
        if a.startswith("https://thehackernews.com"):
            if a in image_set:
                pass
            else:
                image_set.append(a)
    return image_set


def links_url(html_soup):
    anchors = html_soup.find_all('a', class_= 'story-link')
    all_links = set()
    for link in anchors:
        a = link['href']
        all_links.add(a)
    return all_links


def heading(html_soup):
    anchors = html_soup.find_all('h2', class_= 'home-title')
    all_heading = set()
    for link in anchors:
        all_heading.add(link.text)
    return all_heading


def description(html_soup):
    anchors = html_soup.find_all('div', class_= 'home-desc')
    description = set()
    for link in anchors:
        description.add(link.text)
    return description

if __name__ == '__main__':
    driver = webdriver.Chrome(executable_path=r'F:chromedriver')
    driver.get("https://thehackernews.com/")
    time.sleep(10)
    data = driver.page_source
    html_soup = BeautifulSoup(data, 'html.parser')
    descriptionn = description(html_soup)
    descriptionn = list(descriptionn)
    headingg = heading(html_soup)
    headingg = list(headingg)
    links_urll = links_url(html_soup)
    links_urll = list(links_urll)
    get_imagee = get_image(html_soup)
    get_imagee = get_imagee[:len(links_url)]
    dict_to_add = {"Description": descriptionn, "Heading": headingg, "Links_url": links_urll, "Images_url": get_imagee}
    client = MongoClient('localhost', 27017)
    db = client.scrapper_db
    collection = db.scraping_hacker
    result = collection.insert_one(dict_to_add)
    print("Data Appended to DB")