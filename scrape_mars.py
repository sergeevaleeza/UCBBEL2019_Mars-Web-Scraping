#!/usr/bin/env python
# coding: utf-8

# # Scraping. Part 2.
# Start by converting your Jupyter notebook into a Python script called scrape_mars.py 
# with a function called scrape that will execute all of your scraping code from above 
# and return one Python dictionary containing all of the scraped data.


from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd

# Function to initiate browser
def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)



def scrape_info():
    # initialize browser 
    browser = init_browser()
    mars_data = {}


    # ## NASA Mars News
    # * Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text. 
    # * Assign the text to variables that you can reference later.
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Get the title and paragraph
    news_title = soup.find("div",class_="content_title").text
    news_paragraph = soup.find("div", class_="article_teaser_body").text


    # ## JPL Mars Space Images - Featured Image
    # * Visit the url for JPL Featured Space Image at https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars.
    # * Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called 'featured_image_url'.
    # * Make sure to find the image url to the full size .jpg image.
    # * Make sure to save a complete url string for this image.

    # assign url and open browser
    featured_image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(featured_image_url)

    # Scrape page into Soup
    jpl_html = browser.html
    jpl_soup = bs(jpl_html, "lxml")

    featured = jpl_soup.find('div', class_='default floating_text_area ms-layer')
    featured_image = featured.find('footer')
    featured_image_url = 'https://www.jpl.nasa.gov'+ featured_image.find('a')['data-fancybox-href']
    

    # ## Mars Weather
    # * Visit the Mars Weather twitter account at https://twitter.com/marswxreport?lang=en
    # * Scrape the latest Mars weather tweet from the page. 
    # * Save the tweet text for the weather report as a variable called 'mars_weather'.

    # get mars weather's latest tweet from the website
    weather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(weather_url)

    # Scrape page into Soup
    weather_html = browser.html
    weather_soup = bs(weather_html, 'html.parser')

    #Retrieve latest tweet
    mars_weather = weather_soup.find('p', 'TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text


    # ## Mars Facts
    # * Visit the Mars Facts webpage at https://space-facts.com/mars/
    # * Use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    # * Use Pandas to convert the data to a HTML table string.

    # get mars weather's latest tweet from the website
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)

    # convert facts/table to DataFrame
    table = pd.read_html(facts_url)
    df = table[0]
    mars_df = df.drop('Earth', axis=1) 
    mars_df.columns = ['Description', 'Mars']
    mars_df = mars_df.set_index(['Description'], drop=True)
    mars_df

    # convert df to HTML string
    mars_df_html = mars_df.to_html()
    mars_df_html = mars_df_html.replace("\n", "")
    mars_df_html

    # convert df to HTML and export it as HTML page
    # mars_df.to_html('mars_facts.html')



    # ## Mars Hemispheres
    # * Visit the USGS Astrogeology site at https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars to obtain high resolution images for each of Mar's hemispheres.
    # * You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
    # * Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name. Use a Python dictionary to store the data using the keys 'img_url' and 'title'.
    # * Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.  

    # get url loaded
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)  

    # Scrape page into Soup
    hemispheres_html = browser.html
    hemispheres_soup = bs(hemispheres_html, 'html.parser')  

    # scrape all information from the page
    items = hemispheres_soup.find("div", class_="collapsible results")
    all_items = items.find_all("div", class_="item")
    hemisphere_image_urls = []  

    for item in all_items:
        title = item.find('h3').text
        browser.click_link_by_partial_text(title)

        # refresh browser page to image page
        html = browser.html
        soup = bs(html, 'html.parser')

        # get url address for full picture
        img_url = soup.find("div", class_="downloads").find("ul").find("li").a.get("href")

        #append dictionary to list
        hemisphere_image_urls.append({"title":title, "img_url":img_url })
        browser.back()

    mars_data["news_title"] = news_title
    mars_data["news_paragraph"] = news_paragraph
    mars_data["featured_image_url"] = featured_image_url
    mars_data["mars_weather"] = mars_weather
    mars_data["mars_facts"] = mars_df_html
    mars_data["hemisphere_image_urls"] = hemisphere_image_urls

#        "news_title": news_title,
#        "news_paragraph": news_paragraph,
#        "featured_image_url": str(featured_image_url),
#        "mars_weather": mars_weather,
#        "mars_facts": mars_df_html,
#        "hemispheres": hemisphere_image_urls, 
#        }

    
    return mars_data


