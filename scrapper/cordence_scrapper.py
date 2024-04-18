# Imports
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
from pymongo import MongoClient
from datetime import datetime
from utils import generate_uid, send_to_teams_webhook

# Cordence Scrapper
def cordence_scrape_function(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        contents = soup.find_all('div', class_='latest__content')
        data = []

        for content in contents:
            title_elem = content.find('h2', class_='latest__heading')
            title = title_elem.text.strip() if title_elem else None

            url_elem = content.find('a', class_='latest__link')
            url = url_elem['href'] if url_elem else None

            content_elements = content.find_all(['p', 'div'], class_='latest__text')
            content = ' '.join([elem.text.strip() for elem in content_elements]) if content_elements else None


            data.append({
                'title': title,
                'url': url,
                'content': content
            })
        return data
    else:
        print(f"Error: Failed to fetch URL {url}")
        return None
    
#Store Insight Article in DB
def store_articles_in_db_insights(cordence_insight_scrape_data, collection):
    count = 0
    mes_str = ""
    for article in cordence_insight_scrape_data:
        # Extract required information
        uid = generate_uid(prefix="AR")
        org_name = "Cordence Worldwide"
        article_category = "Insights"
        article_subcategory = ""
        article_title = article['title']
        article_url = article['url']
        article_content = article['content']
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
            count += 1
            # send_to_teams_webhook('Cordence Insight New article: '+ article_title +' added to the collection.')
            # print(f"New article '{article_title}' added to the collection.")
            mes_str = mes_str + article_title + " || "

    print("All Cordence Insights Articles processed.")
    insight_msg = "Cordence Insights Total New Articles Added: "+ str(count) + "\n" + mes_str
    # send_to_teams_webhook(insight_msg)
    return "All Cordence Insights Articles processed."

#Store Latest Article in DB
def store_articles_in_db_latest(cordence_insight_scrape_data, collection):
    count = 0
    mes_str = ""
    for article in cordence_insight_scrape_data:
        if(article['title'] == None or article['url'] == None ):
            pass
        # Extract required information
        uid = generate_uid(prefix="AR")
        org_name = "Cordence Worldwide"
        article_category = "Latest"
        article_subcategory = ""
        article_title = article['title']
        article_url = article['url']
        article_content = article['content']
        article_language = "English"
        created_ts = datetime.now()
        last_checked = datetime.now()

        # Check if article exists based on URL
        existing_article = collection.find_one({"article_title": article_title})
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
            count += 1
            # send_to_teams_webhook('Cordence Latest New article: '+ article_title +'added to the collection.')
            # print(f"New article '{article_title}' added to the collection.")
            mes_str = mes_str + article_title + " || "

    print("All Cordence Latest Articles processed.")
    latest_msg = "Cordence Latest Total New Articles Added: "+ str(count) + "\n" + mes_str
    # send_to_teams_webhook(latest_msg)
    return "All Cordence Latest Articles processed."

