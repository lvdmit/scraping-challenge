import os
from bs4 import BeautifulSoup as bs
from splinter import Browser
import requests
import pandas as pd
import time

def scrape():
    
    
    #-------------------
    ## NASA Mars News
    #-------------------

    #set up url
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

    #set up splinter brouser
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    #visit url
    browser.visit(url)

    #pull html + needed info 
    html = browser.html
    soup = bs(html, 'html.parser')

    news_title = soup.find('div', class_="content_title").text
    news_p = soup.find('div', class_='article_teaser_body').text

    #----------------------------------------
    ## JPL Mars Space Images - Featured Image
    #----------------------------------------

    #set up url
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    #set up browser and visit url
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(jpl_url )

    #navigate to the required html-page
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(5)
    browser.click_link_by_partial_text('more info')

    #pull html + needed info from the web-page
    jpl_html = browser.html
    soup = bs(jpl_html, 'html.parser')

    result = soup.find('figure', class_='lede')
    featured_image_path = result.a['href']
    featured_image_url = f'https://www.jpl.nasa.gov/{featured_image_path}'

    #----------------
    ## Mars Weather
    #----------------

    #set up  + visit url
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(weather_url )

    #pull html + needed info from the web-page
    for x in range(1, 6):

        weather_html = browser.html
        soup = bs(weather_html, 'html.parser')
        results = soup.find_all('div', class_='js-tweet-text-container')
    
    #get tweets that consist of only weather info
        tweets = []
        errors = []
        for result in results:
            try:
                mars_weather = result.find('p', {'data-aria-label-part':'0'}).text
                if 'daylight' in mars_weather:
    
                    tweets.append(mars_weather)
        
            except AttributeError as e:
                errors.append(e)
    
    #get the latest tweets 
    mars_weather = tweets[0]

    #----------------
    ## Mars Facts
    #----------------

    #set up  + visit url
    facts_url = 'https://space-facts.com/mars/'
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(facts_url)

    #pull html + needed info from the web-page
    facts_html = browser.html
    soup = bs(facts_html, 'html.parser')
    data = soup.find('table', class_='tablepress tablepress-id-mars')
    
    #get only table rows
    table_data = data.find_all('tr')

    #extract needed info from the table
    keys=[]
    values=[]
    
    for x in table_data:
        col_1 = x.find('td', class_="column-1").text
        col_2 = x.find('td', class_="column-2").text
        keys.append(col_1)
        values.append(col_2)
    
    #create a dictionary from keys and values
    dictionary = dict(zip(keys, values))

    #create a dataframe from the dictionary
    mars_df = pd.DataFrame.from_dict(dictionary, orient='index', columns=['Values'])

    #convert dataframe into html
    mars_html = mars_df.to_html()

    #--------------------
    ## Mars Hemispheres
    #--------------------

    #set up and visit url
    hem_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(hem_url)

    #pull html + get all the links that hold img urls
    hem_html = browser.html
    soup = bs(hem_html, 'html.parser')
    hem_results = soup.find('div', class_="collapsible results")
    hemispheres = hem_results.find_all('a')

    #get all the titles + img urls
    hem_links=[]
    hem_titles=[]
    for a in hemispheres:
        hem_link=a['href']
        hem_title = a.text
    
        hem_links.append(f'https://astrogeology.usgs.gov{hem_link}')
        hem_titles.append(hem_title)

    #get only unique values for titles and img urls
    titles=list(set(hem_titles))
    titles.pop(0)
    titles.sort()
    links=list(set(hem_links))
    links.sort()

    #get large size img urls
    img_results = []
    for a in links:
        browser.visit(a)
        time.sleep(5)
        img_html = browser.html
        soup = bs(img_html, 'html.parser') 
        img_result = soup.find('div', class_="downloads").find('li').a['href']
        img_results.append(img_result)

    #create a list of dictionaries of titles and img_results
    hemisphere_image_urls=[]
    hemisphere_image_urls.append({"title": titles[0], "img_url": img_results[0]})
    hemisphere_image_urls.append({"title": titles[1], "img_url": img_results[1]})
    hemisphere_image_urls.append({"title": titles[2], "img_url": img_results[2]})
    hemisphere_image_urls.append({"title": titles[3], "img_url": img_results[3]})
    

    mars_dict = {
        "id": 1,
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "mars_html": mars_html,
        "hemisphere_images": hemisphere_image_urls
    }

    return mars_dict

    

