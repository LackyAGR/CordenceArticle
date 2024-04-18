# Imports
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
from pymongo import MongoClient
from datetime import datetime
from utils import generate_uid, send_to_teams_webhook

def twynstragudde_Scrape_Function(url):
    all_articles = []
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        article_elements = soup.find_all('div', class_='element-item')
        for article_element in article_elements:
            link_element = article_element.find('a')
            if link_element:
                subtitle_element = article_element.find('span', class_='subtitle')
                title_element = article_element.find('h3')
                description_element = article_element.find('p')
                author_element = article_element.find('div', class_='fbox-footer')
                link_url = link_element['href']

                if subtitle_element and title_element and description_element and author_element:
                    subtitle = subtitle_element.text.strip()
                    title = title_element.text.strip()
                    description = description_element.text.strip()
                    author = author_element.text.strip()

                    # Adjusting the link URL
                    base_url = 'https://www.twynstragudde.nl'
                    if not link_url.startswith(base_url):
                        link_url = urljoin(base_url, link_url)

                    all_articles.append({
                        'type': subtitle,
                        'title': title,
                        'description': description,
                        'author': author,
                        'link_url': link_url
                    })
    else:
        print(f"Error: Failed to fetch URL {url}")

    return all_articles


#Store Twynstragudde Article in DB
def store_Twynstragudde_Articles_In_Db(twynstragudde_Scrape_Data, collection):
    count = 0
    mes_str = ""
    for article in twynstragudde_Scrape_Data:
        if(article['title'] == None or article['link_url'] == None ):
            pass
        # Extract required information
        uid = generate_uid(prefix="AR")
        org_name = "Twynstragudde"
        article_category = article['type']
        article_subcategory = ""
        article_title = article['title']
        article_tags = ""
        article_url = article['link_url']
        article_description = article['description']
        article_author = article['author']
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
                "article_tags": article_tags,
                "article_url": article_url,
                "article_description": article_description,
                "article_author": article_author,
                "article_language": article_language,
                "created_ts": created_ts,
                "last_checked": last_checked
            }
            collection.insert_one(article_data)
            count+=1
            # send_to_teams_webhook('Twynstragudde New Article: '+article_title+' added to the collection.')
            mes_str = mes_str + article_title + " || "

    print("All Twynstragudde Articles processed.")
    twynstragudde_MediaCenter_msg = "Twynstragudde Total New Articles Added:"+ str(count) + "\n" + mes_str
    # send_to_teams_webhook(twynstragudde_MediaCenter_msg)
    return "All Twynstragudde Articles processed."