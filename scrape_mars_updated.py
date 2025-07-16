import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import time

def scrape_all():
    mars_data = {}

    # ========== NASA Mars News ========== #
    news_url = 'https://science.nasa.gov/mars/stories/'
    try:
        response = requests.get(news_url)
        soup = bs(response.text, "html.parser")

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
    except Exception as e:
        print("Failed to load NASA Mars News:", e)

    # ========== Curiosity Rover Update ========== #
    try:
        rover_url = "https://science.nasa.gov/mission/msl-curiosity/science-updates/"
        response = requests.get(rover_url)
        soup = bs(response.text, "html.parser")

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
    except Exception as e:
        print("Failed to load Curiosity Rover update:", e)

    # ========== Mars Facts Table ========== #
    try:
        facts_url = "https://space-facts.com/mars/"
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

    # ========== Mars Gallery Images ========== #
    try:
        gallery_url = "https://science.nasa.gov/gallery/mars/"
        base_url = "https://science.nasa.gov"
        response = requests.get(gallery_url)
        response.raise_for_status()
        soup = bs(response.text, "html.parser")

        gallery_data = []
        items = soup.find_all("div", class_="hds-gallery-item-single hds-gallery-image")

        for item in items[:10]:  # Limit for performance
            a_tag = item.find("a", class_="hds-gallery-item-link hds-gallery-image-link")
            detail_url = a_tag["href"]
            caption = item.find("div", class_="hds-gallery-item-caption hds-gallery-image-caption").get_text(strip=True)
            thumb_url = a_tag.find("img")["src"]

            if not detail_url.startswith("http"):
                detail_url = base_url + detail_url

            # Visit the detail page to get high-res image
            full_img_url = None
            try:
                detail_response = requests.get(detail_url)
                detail_response.raise_for_status()
                detail_soup = bs(detail_response.text, "html.parser")

                download_section = detail_soup.find("div", class_="hds-attachment-single__buttons")
                download_link_tag = download_section.find("a", class_="hds-button-download") if download_section else None

                if download_link_tag and download_link_tag.get("href"):
                    full_img_url = download_link_tag["href"]
            except Exception as e:
                print(f"Failed to get full image from {detail_url}: {e}")

            gallery_data.append({
                "title": caption,
                "thumb_url": thumb_url,
                "full_img_url": full_img_url or thumb_url  # fallback
            })
            time.sleep(0.5)

        mars_data["mars_gallery"] = gallery_data
    except Exception as e:
        print("Failed to scrape Mars Gallery:", e)
        mars_data["mars_gallery"] = []

    return mars_data
