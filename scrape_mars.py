# Declare Dependencies 
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import os
import time
import requests
import warnings
warnings.filterwarnings('ignore')

def init_browser():
    # @NOTE: Path to my chromedriver
    executable_path = {'executable_path': '../Web-Scraping-and-Document-Databases/chromedriver_win32/chromedriver'}
    return Browser("chrome", **executable_path, headless=False)

# Create Mission to Mars global dictionary that can be imported into Mongo
mars_info = {}

# NASA MARS NEWS
def scrape_mars_news():

        # Initialize browser 
        browser = init_browser()

        #browser.is_element_present_by_css("div.content_title", wait_time=1)

        # Visit Nasa news url through splinter module
        url = 'https://mars.nasa.gov/news/'
        browser.visit(url)
        time.sleep(5)

        # HTML Object
        html = browser.html

        # Parse HTML with Beautiful Soup
        soup = bs(html, 'html.parser')

        # Retrieve the latest element that contains news title and news_paragraph
        
        date= soup.find('div', {'class' : "list_date"})
        
        if date is not None:
                news_date = date.text
        else:
                news_date = None

        title= soup.find('div', {'class' : "bottom_gradient"}, {'class': 'content_title'})

        if title is not None:
                news_title = title.text
        else:
                news_title = None


        para =soup.find('div', {'class' :'article_teaser_body'})
        
        if title is not None:
                news_p = para.text
        else:
                news_p = None


        # Dictionary entry from MARS NEWS
        mars_info['news_date'] = news_date
        mars_info['news_title'] = news_title
        mars_info['news_paragraph'] = news_p

        
        browser.quit()
        
        return mars_info

        

       

# FEATURED IMAGE
def scrape_mars_image():

        # Initialize browser 
        browser = init_browser()

        #browser.is_element_present_by_css("img.jpg", wait_time=1)

        # Visit Mars Space Images through splinter module
        featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(featured_image_url)# Visit Mars Space Images through splinter module
        time.sleep(5)

        # HTML Object 
        html_image = browser.html

        # Parse HTML with Beautiful Soup
        soup = bs(html_image, 'html.parser')

        # Retrieve background-image url from style tag 
        image_url  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

        # Website Url 
        main_url = 'https://www.jpl.nasa.gov'

        # Concatenate website url with scrapped route
        image_url = main_url + image_url

        # Display full link to featured image
        image_url 

        # Dictionary entry from FEATURED IMAGE
        mars_info['image_url'] = image_url

        browser.quit()  
       

        return mars_info

        

        

# Mars Weather 
def scrape_mars_weather():

        # Initialize browser 
        browser = init_browser()

        #browser.is_element_present_by_css("div", wait_time=1)

        # Visit Mars Weather Twitter through splinter module
        weather_url = 'https://twitter.com/marswxreport?lang=en'
        browser.visit(weather_url)
        time.sleep(5)

        # HTML Object 
        html_weather = browser.html

        # Parse HTML with Beautiful Soup
        soup = bs(html_weather, 'html.parser')

        # Find the latest tweet

        dt = soup.find({'time':'datetime'})

        if dt is not None:
                date_time = dt.text
                
        else:
                date_time = None

        weather =soup.find('div', class_= 'css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0')

        if weather is not None:
                mars_weather = weather.text
        else:
                mars_weather = None

        
        
         # Dictionary entry from WEATHER TWEET
        mars_info['date_time'] = date_time
        mars_info['mars_weather'] = mars_weather

        browser.quit()
        
        return mars_info
        
        
# Mars Facts
def scrape_mars_facts():

        # Initialize browser 
        browser = init_browser()

         # Visit Mars facts url 
        url = 'http://space-facts.com/mars/'
        browser.visit(url)
        time.sleep(5)

        # Use Pandas to "read_html" to parse the URL
        tables = pd.read_html(url)
        #Find Mars Facts DataFrame in the lists of DataFrames
        df = tables[1]
        #Assign the columns
        html_table = df.to_html(table_id="html_tbl_css",justify='left',index=False)

        # Dictionary entry from Mars Facts

        mars_info['tables'] = html_table
        
        browser.quit()

        return mars_info
        

# Mars Hemisphere

def scrape_mars_hemispheres():

        # Initialize browser 
        browser = init_browser()

        # Visit hemispheres website through splinter module 
        hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(hemispheres_url)
        time.sleep(25)

        # HTML Object
        html_hemispheres = browser.html

        # Parse HTML with Beautiful Soup
        soup = bs(html_hemispheres, 'html.parser')

        # Retreive all items that contain mars hemispheres information
        items = soup.find_all('div', class_='item')

        # Create empty list for hemisphere urls 
        hiu = []

        # Store the main_ul 
        hemispheres_main_url = 'https://astrogeology.usgs.gov' 

        # Loop through the items previously stored
        for i in items: 
            # Store title
            title = i.find('h3').text
            time.sleep(5)
            # Store link that leads to full image website
            partial_img_url = i.find('a', class_='itemLink product-item')['href']
            
            # Visit the link that contains the full image website 
            browser.visit(hemispheres_main_url + partial_img_url)
            
            # HTML Object of individual hemisphere information website 
            partial_img_html = browser.html
            
            # Parse HTML with Beautiful Soup for every individual hemisphere information website 
            soup = bs( partial_img_html, 'html.parser')
            
            # Retrieve full image source 
            img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
            
            # Append the retreived information into a list of dictionaries 
            hiu.append({"title" : title, "img_url" : img_url})

        mars_info['hiu'] = hiu
       
        
        browser.quit()
       
       

        # Return mars_data dictionary 

        return mars_info