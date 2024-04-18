# Imports
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
from pymongo import MongoClient
from datetime import datetime
from utils import generate_uid, send_to_teams_webhook

def key_To_Way_Scrapper_Function(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        articles = soup.find_all('div', class_='sqs-block-content')
        data = []

        for article in articles:
            title_elements = article.find_all(['p', 'div'], class_='sqs-dynamic-text')
            title = ' '.join([elem.text.strip() for elem in title_elements]) if title_elements else None

            url_elem = article.find('a', class_='image-inset')
            if url_elem:
                article_url = urljoin(url, url_elem['href'])
            else:
                article_url = None

            data.append({
                'title': title,
                'url': article_url
            })

        return data
    else:
        print(f"Error: Failed to fetch URL {url}")
        return None


#Store State Of Matter Article in DB
def store_Key_To_Way_Articles_In_Db(key_To_Way_Scrape_Data, collection):
    count = 0
    mes_str = ""
    for article in key_To_Way_Scrape_Data:
        if(article['title'] == None or article['url'] == None ):
            pass
        # Extract required information
        uid = generate_uid(prefix="AR")
        org_name = "Key To Way"
        article_category = ""
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
            # send_to_teams_webhook('Key To Way New Article: '+article_title+' added to the collection.')
            mes_str = mes_str + article_title + " || "

    print("All Key To Way Articles processed.")
    key_To_Way_msg = "Key To Way Total New Articles Added: "+ str(count) + "\n" + mes_str
    # send_to_teams_webhook(key_To_Way_msg)
    return "All Key To Way Articles processed."