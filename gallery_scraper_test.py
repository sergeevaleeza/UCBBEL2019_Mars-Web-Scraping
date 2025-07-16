import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import time


def scrape_mars_gallery():
    from bs4 import BeautifulSoup as bs
    import requests
    import time

    gallery_url = "https://science.nasa.gov/gallery/mars/"
    base_url = "https://science.nasa.gov"

    try:
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

            try:
                detail_res = requests.get(detail_url)
                detail_res.raise_for_status()
                detail_soup = bs(detail_res.text, "html.parser")

                download_section = detail_soup.find("div", class_="hds-attachment-single__buttons margin-bottom-6")
                full_img_url = download_section.find("a", class_="usa-button hds-button hds-button-download margin-right-2")["href"]
            except:
                full_img_url = None

            gallery_data.append({
                "title": caption,
                "thumb_url": thumb_url,
                "full_img_url": full_img_url if full_img_url else thumb_url
            })

            time.sleep(0.5)

        return gallery_data
    except Exception as e:
        print("Scraping failed:", e)
        return []

# To test:
print(scrape_mars_gallery())
