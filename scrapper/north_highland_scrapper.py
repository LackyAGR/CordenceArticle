# Imports
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
from pymongo import MongoClient
from datetime import datetime
from utils import generate_uid, send_to_teams_webhook

# Working for NorthHighland
def north_highland_scrapper_function(url):
    data = []

    while url:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            content_elements = soup.find_all('div', class_='insight--card')

            for content_element in content_elements:
                title_element = content_element.find('div', class_='insight--card--text').find('h3', class_='h4')
                title = title_element.text.strip() if title_element else None

                category_element = content_element.find('div', class_='insight--card--category')
                category = category_element.text.strip() if category_element else None

                link_element = content_element.find('div', class_='insight--card--link').find('a')
                link_url = urljoin(url, link_element['href']) if link_element else None

                data.append({
                    'title': title,
                    'category': category,
                    'url': link_url
                })
            next_page_element = soup.find('li', class_='pager__item--next')

            if next_page_element:
                next_page_url_fragment = next_page_element.find('a')['href']
                next_page_url = urljoin(url, next_page_url_fragment)
                url = next_page_url
            else:
                url = None
        else:
            print(f"Error: Failed to fetch URL {url}")
            return None

    # print(data)
    return data

#Store North Highland Article in DB
def store_north_highland_articles_in_db(north_highland_insight_scrape_data, collection):
    count = 0
    mes_str = ""
    for article in north_highland_insight_scrape_data:
        if(article['title'] == None or article['url'] == None ):
            pass
        # Extract required information
        uid = generate_uid(prefix="AR")
        org_name = "North Highland"
        article_category = article['category']
        article_subcategory = ""
        article_title = article['title']
        article_url = article['url']
        article_content = ""
        article_language = "English"
        created_ts = datetime.now()
        last_checked = datetime.now()

        # Check if article exists based on URL
        existing_article = collection.find_one({"article_url": article_url})
        if existing_article:
            # Update last_checked field
            collection.update_one({"_id": existing_article["_id"]}, {"$set": {"last_checked": last_checked}})
            # print(f"Article '{article_title}' already exists. Last checked updated.")
        else:
            # Insert new article
            article_data = {
                "_uid": uid,
                "org_name": org_name,
                "article_category": article_category,
                "article_subcategory": article_subcategory,
                "article_title": article_title,
                "article_url": article_url,
                "article_content": article_content,
                "article_language": article_language,
                "created_ts": created_ts,
                "last_checked": last_checked
            }
            collection.insert_one(article_data)
            count+=1
            # send_to_teams_webhook('North Highland New Article: '+article_title+' added to the collection.')
            mes_str = mes_str + article_title + " || "

    print("All North Highland Articles processed.")
    north_highland_msg = "North Highland Total New Articles Added: "+ str(count) + "\n" + mes_str
    # send_to_teams_webhook(north_highland_msg)
    return "All North Highland Articles processed."
