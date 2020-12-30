from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import pymongo

def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    Browser = Browser('chrome', **executable_path, headless=False)

def scrape():
    Browser = init_browser()
    mars_dict ={}


news_url='https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
Browser.visit(news_url)

html = Browser.html
news_soup = bs(html,'html.parser')

#Nasa Mars News
news_title = news_soup.find_all("div", class_="content_title")[0].text
print (news_title)
news_paragraph = news_soup.body.find("div", class_="article_teaser_body").text
print(news_paragraph)

#mars image
base_url = 'https://www.jpl.nasa.gov'
images_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

Browser.visit(images_url)
html = Browser.html
images_soup = bs(html, 'html.parser')

relative_image_path = images_soup.find_all('img')[3]["src"]
featured_images_url = base_url + relative_image_path
print(featured_images_url)
    
#Mars Facts
Facts_url = 'https://space-facts.com/mars/'
Browser.visit(Facts_url)
time.sleep(2)

html = Browser.html

table = pd.read_html(html)

facts_df = table[0]
facts_df.columns = ['Description', 'Value']
facts_df

facts_df.to_html('marsfacts.html', index=False)

#mars hemisphere
usgs_url='https://astrogeology.usgs.gov'

hem_images_url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

Browser.visit(hem_images_url)

hem_html = Browser.html

hem_soup = bs(hem_html, 'html.parser')

all_mars_hem = hem_soup.find('div', class_ = 'collapsible results')
mars_hem = all_mars_hem.find_all('div', class_='item')

hem_url = []

for i in mars_hem:
    hemisphere = i.find('div', class_="description")
    title = hemisphere.h3.text
    
    hem_link = hemisphere.a["href"]
    Browser.visit(usgs_url + hem_link)
    
    image_html = Browser.html
    image_soup=bs(image_html,'html.parser')
    
    image_link = image_soup.find('div',class_='downloads')
    image_url = image_link.find('li').a['href']
    
    
    image_dict={}
    image_dict['title']=title
    image_dict['img_url']=image_url
    
    hem_url.append(image_dict)

print(hem_url)

mars_dict = {
    "news_title": news_title,
    "news_paragraph": news_paragraph,
    "featured_images_url":featured_images_url,
    "facts_df":str(table),
    "hemisphere_images":hem_url
    
}

