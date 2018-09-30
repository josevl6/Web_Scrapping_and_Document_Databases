# Importing dependencies

from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time

# scrape all
def scrape_all():
    executable_path = {"executable_path": "chromedriver"}
    browser = Browser("chrome", **executable_path, headless=False)

    news_header, news_text = mars_news(browser)

    mars_data = {
        "news_header": news_header,
        "news_text": news_text,
        "mars_image": mars_img(browser),
        "mars_weather": mars_weather(browser),
        "mars_facts": mars_facts(browser),
        "mars_hem": mars_hem(browser) 
    }
    
    return mars_data
    
# scrape_all

#---------------------------------------
def mars_news(browser):

    #Visit the NASA website
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(1)
# Scrape page into soup
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
# print(html)

# Collect the latest News Title and Paragraph Text
    news = soup.find("ul", class_="item_list")
    current_news = news.find("li", class_="slide")

    news_header = current_news.find("div", class_="content_title").text
    news_text = current_news.find("div", class_="article_teaser_body").text

    return news_header, news_text

# mars_news()
# ----------------------------------------------------------------------------

def mars_img(browser):

    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    time.sleep(1)
    find_image_id = browser.find_by_id("full_image")
    find_image_id.click()

    # expand = browser.find_by_css('a.fancybox-expand')
    # expand.click()
    # time.sleep(1)

    browser.is_element_present_by_text("more info", wait_time=1)
    find_moreInfo_button = browser.find_link_by_partial_text("more info")
    find_moreInfo_button.click()

    image_html = browser.html
    img_soup = BeautifulSoup(image_html, "html.parser")


    # img = img_soup.find("img", class_="fancybox-image").get("src")
    # featured_image_url = f"https://www.jpl.nasa.gov{img}"

    img = img_soup.select_one("figure.lede a img").get("src")
    featured_image_url = f"https://www.jpl.nasa.gov{img}"

    return featured_image_url

#print(mars_img())

#---------------------------------------------------------

# Mars Weather
def mars_weather(browser):

    mars_weather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(mars_weather_url)
    time.sleep(1)

    # Scrape page into soup
    mars_weather_html = browser.html
    mars_weather_soup = BeautifulSoup(mars_weather_html, "html.parser")

    # Get first Nasa Tweet 
    mars_weather = mars_weather_soup.find(
        "div", class_="js-tweet-text-container").text

    return mars_weather

# print(mars_weather()) 
#-------------------------------------------------------------
def mars_facts(browser):

    url = 'http://space-facts.com/mars/'
    table = pd.read_html(url)
    
    df = table[0]
    df.columns = ["Description", "Value"]
    df = df.set_index("Description")

    html_table = df.to_html()

    return html_table

# print(mars_facts())
#------------------------------------------------------------------
def mars_hem(browser):
    # executable_path = {"executable_path": "chromedriver"}
    # browser = Browser("chrome", **executable_path, headless=False)

    # scrape images of Mars' hemispheres from the USGS site
    mars_hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(mars_hemisphere_url)
    
    hemi_dicts = []

    links = browser.find_by_css("a.product-item h3")

    for i in range(len(links)):    
        
        hemisphere_dict = {}

        browser.find_by_css("a.product-item h3")[i].click()

        element = browser.find_link_by_text("Sample").first
        hemisphere_dict["img_url"] = element["href"]

        title = browser.find_by_css("h2.title").text # 
        hemisphere_dict["img_title"] = title

        hemi_dicts.append(hemisphere_dict)

        browser.back()


    return hemi_dicts
# print(mars_hem())
# print(scrape_all())
# print("scrape succesful!")



