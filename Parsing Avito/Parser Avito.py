import requests
from bs4 import BeautifulSoup
import re


def get_html(url):
    response = requests.get(url)
    return response.text


def get_count_pages(html):
    soup = BeautifulSoup(html, "lxml")
    pages = soup.find("div", class_="pagination-pages clearfix").find_all("a", class_="pagination-page")[-1].get("href")
    return int(re.search("[\d]+", pages).group())   # количество страниц


def get_page_data(html):
    soup = BeautifulSoup(html, "lxml")
    info_phone = soup.find("div", class_="js-catalog_serp").find_all_next("div", class_="item__line")
    with open("info_phone.csv", "w") as file:
        for data in info_phone:
            name = data.find("a", class_="snippet-link").text.strip()
            price = data.find("div", class_="snippet-price-row").text.strip()
            address = data.find("span", class_="item-address-georeferences-item__content").text.strip()
            time_published = data.find("div", class_="snippet-date-info").text.strip()
            file.write(f"{name},{price},{address},{time_published}\n")


start_url = "https://www.avito.ru/moskva/telefony?q=Iphone"

for num in range(1, 2): #get_count_pages(get_html(start_url)) + 1):
    url_gen = start_url + f"&p={num}"
    get_page_data(get_html(url_gen))
