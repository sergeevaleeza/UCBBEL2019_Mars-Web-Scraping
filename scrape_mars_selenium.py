#!/usr/bin/env python
# coding: utf-8

from selenium import webdriver
from .webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as bs
import pandas as pd


def launch_driver(headless=True):
    chrome_options = Options()
    chrome_options.binary_location = "/usr/bin/google-chrome"
    if headless:
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)


def scrape_all():
    driver = launch_driver()
    mars_data = {}

    try:
        # ========== NASA Mars News ========== #
        news_url = 'https://science.nasa.gov/mars/stories/'
        driver.get(news_url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'hds-a11y-heading-22')))
        soup = bs(driver.page_source, "html.parser")

        article = soup.find("a", class_="hds-content-item-heading")
        if article:
            title = article.find("div", class_="hds-a11y-heading-22")
            paragraph = article.find_next("p", class_="margin-top-0 margin-bottom-1")
            date = article.find_next("div", class_="label margin-y-1")
            link = article['href']

            mars_data["news_title"] = title.get_text(strip=True) if title else "No title"
            mars_data["news_paragraph"] = paragraph.get_text(strip=True) if paragraph else "No summary available."
            mars_data["news_date"] = date.get_text(strip=True) if date else "No date"
            mars_data["news_link"] = link if link.startswith("http") else f"https://science.nasa.gov{link}"

        # ========== Featured Image ========== #
        driver.get("https://www.jpl.nasa.gov/images?search=&category=Mars")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "BaseImage")))
        soup = bs(driver.page_source, "html.parser")
        image_tag = soup.find("img", class_="BaseImage")
        mars_data["featured_image_url"] = image_tag["src"] if image_tag else None

        # ========== Curiosity Rover Update ========== #
        driver.get("https://science.nasa.gov/mission/msl-curiosity/science-updates/")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "hds-content-item-heading")))
        soup = bs(driver.page_source, "html.parser")

        blog = soup.find("a", class_="hds-content-item-heading")
        if blog:
            title = blog.find("div", class_="hds-a11y-heading-22")
            date = blog.find_next("div", class_="label margin-y-1")
            summary = blog.find_next("p", class_="margin-top-0 margin-bottom-1")
            link = blog["href"]

            mars_data["curiosity_title"] = title.get_text(strip=True) if title else "No title"
            mars_data["curiosity_date"] = date.get_text(strip=True) if date else "No date"
            mars_data["curiosity_summary"] = summary.get_text(strip=True) if summary else "No summary"
            mars_data["curiosity_link"] = link if link.startswith("http") else f"https://science.nasa.gov{link}"

        # ========== Mars Facts Table ========== #
        facts_url = "https://space-facts.com/mars/"
        try:
            tables = pd.read_html(facts_url)
            df = tables[0]
            df.columns = ['Description', 'Mars']
            df.set_index('Description', inplace=True)
            mars_data["mars_facts"] = df.to_html(classes="table table-striped", border=0, justify="left")
        except Exception as e:
            print("Failed to load Mars facts table:", e)
            mars_data["mars_facts"] = None

        # ========== Hemisphere Map Embed ========== #
        mars_data["hemisphere_viewer_embed"] = (
            '<iframe src="https://usgs.maps.arcgis.com/apps/webappviewer/index.html?id=f693b580b2464e6989f32e4266199552" '
            'width="100%" height="1000" style="border:none;" allowfullscreen loading="lazy"></iframe>'
        )

    except Exception as e:
        print("Error during scraping:", e)

    finally:
        driver.quit()

    return mars_data
