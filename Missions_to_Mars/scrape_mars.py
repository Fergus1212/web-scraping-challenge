

from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup
import pandas as pd
import requests
from flask import Flask, render_template
import pymongo


def scrape():
    scrapped_mars_data = {}

    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    executable_path = {'executable_path': 'chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    news_titles_all = soup.find_all('div',class_ = 'content_title')

    ## Find the first headline and add it to the dictionary
    headlines = []

    for td in news_titles_all:
        if (td.a):
            if (td.a.text):
                headlines.append(td)

    news_title = headlines[1].text
    scrapped_mars_data['news_title'] = news_title

    # ## Nasa News Paragraph

    news_p_all = soup.find_all('div',class_ = 'rollover_description')

    paragraphs = []

    for td in news_p_all:
        if (td.div):
            if (td.div.text):
                paragraphs.append(td)

    news_p = paragraphs[1].text
    scrapped_mars_data['news_p'] = news_p

    ## Mars Featured Image
    url_image = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    response2 = requests.get(url_image)
    soup2 = BeautifulSoup(response2.text, 'html.parser')

    browser.visit(url_image)
    browser.click_link_by_partial_text('FULL IMAGE')

    images = soup2.find_all('a', class_="fancybox")

    pic_src = []
    for image in images:
        pic = image['data-fancybox-href']
        pic_src.append(pic)

    featured_image_url = 'https://www.jpl.nasa.gov' + pic

    scrapped_mars_data['featured_image_url'] = featured_image_url

    # ## Mars Weather

    url_weather = 'https://twitter.com/marswxreport?lang=en'
    response3 = requests.get(url_weather)
    soup3 = BeautifulSoup(response3.text, 'html.parser')

    tweets = soup3.find_all("div",class_="content")
    tweeters = []
    for td in tweets:
        first_tweet = td.find("div",class_ = "js-tweet-text-container").text
        tweeters.append(first_tweet)

    mars_weather = tweeters[2]
    scrapped_mars_data['mars_weather'] = mars_weather

    # ## Mars Facts

    url_facts = 'https://space-facts.com/mars/'


    tables = pd.read_html(url_facts)
    df=tables[0]
    df_t=df.transpose()
    df_t.columns = ['Equatorial Diameter:','Polar Diameter:','Mass:',"Moons:","Orbit Distance:","Orbit Period:","Surface Temperature:","First Record:", "Recorded By:"]
    df_t = df_t.drop([0])
    html_table = df_t.to_html()

    scrapped_mars_data['html_table'] = html_table

    # ## Mars Hemispheres

    ## First Hemisphere
    url_hemi_1 = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced'
    response_hemi_1 = requests.get(url_hemi_1)
    soup_hemi_1 = BeautifulSoup(response_hemi_1.text, 'html.parser')

    container = soup_hemi_1.find_all('div',{"class":'wide-image-wrapper'})

    hemi1_pic_src = []
    for a in soup_hemi_1.find_all('a', href=True):
        hemi1_pic_src.append(a['href'])

    hemi1_pic = hemi1_pic_src[4]


    ## Second Hemisphere
    url_hemi_2 = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced'
    response_hemi_2 = requests.get(url_hemi_2)
    soup_hemi_2 = BeautifulSoup(response_hemi_2.text, 'html.parser')

    container = soup_hemi_2.find_all('div',{"class":'wide-image-wrapper'})

    hemi2_pic_src = []
    for a in soup_hemi_2.find_all('a', href=True):
        hemi2_pic_src.append(a['href'])

    hemi2_pic = hemi2_pic_src[4]

    ## Third Hemisphere
    url_hemi_3 = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced'
    response_hemi_3 = requests.get(url_hemi_3)
    soup_hemi_3 = BeautifulSoup(response_hemi_3.text, 'html.parser')

    container = soup_hemi_3.find_all('div',{"class":'wide-image-wrapper'})

    hemi3_pic_src = []
    for a in soup_hemi_3.find_all('a', href=True):
        hemi3_pic_src.append(a['href'])

    hemi3_pic = hemi3_pic_src[4]

    ## Fourth Hemisphere
    url_hemi_4 = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced'
    response_hemi_4 = requests.get(url_hemi_4)
    soup_hemi_4 = BeautifulSoup(response_hemi_4.text, 'html.parser')

    container = soup_hemi_4.find_all('div',{"class":'wide-image-wrapper'})

    hemi4_pic_src = []
    for a in soup_hemi_4.find_all('a', href=True):
        hemi4_pic_src.append(a['href'])

    hemi4_pic = hemi4_pic_src[4]

    ## Hemisphere Dictionary

    hemisphere_image_urls = [
        {"title": "Valles Marineris Hemisphere",'img_url':hemi1_pic},
        {"title": "Cerberus Hemisphere",'img_url':hemi2_pic},
        {"title": "Schiaperelli Hemisphere",'img_url':hemi3_pic},
        {"title": "Syrtis Major Hemisphere",'img_url':hemi4_pic},
    ]

    scrapped_mars_data['hemisphere_image_urls'] = hemisphere_image_urls

    return scrapped_mars_data

