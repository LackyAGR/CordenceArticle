# Imports
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
from pymongo import MongoClient
from datetime import datetime
from utils import generate_uid, send_to_teams_webhook

def elogroup_Scrape_Function(url):
    data = []
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        content_elements = soup.find_all('div', class_='elementor-column elementor-col-100 elementor-inner-column elementor-element elementor-element-720e7b1')
        
        for content_element in content_elements:
            title_element = content_element.find('h2', class_='elementor-heading-title elementor-size-default').find('a', class_='')
            title = title_element.text.strip() if title_element else None

            link_element = content_element.find('h2', class_='elementor-heading-title elementor-size-default').find('a')
            link_url = urljoin(url, link_element['href']) if link_element else None

            # Extracting content of tags
            tags = []
            tag_elements = content_element.find_all('span', class_='elementor-post-info__terms-list-item')
            for tag_element in tag_elements:
                tags.append(tag_element.text.strip())

            data.append({
                'title': title,
                'link_url': link_url,
                'tags': tags
            })

    else:
        print(f"Error: Failed to fetch URL {url}")
        return None
    
    return data


#Store Elogroup Article in DB
def store_Elogroup_Articles_In_Db(elogroup_Scrape_Data, collection):
    count = 0
    mes_str = ""
    for article in elogroup_Scrape_Data:
        if(article['title'] == None or article['link_url'] == None ):
            pass
        # Extract required information
        uid = generate_uid(prefix="AR")
        org_name = "Elogroup"
        article_category = ""
        article_subcategory = ""
        article_title = article['title']
        article_tags = article['tags']
        article_url = article['link_url']
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
                "article_tags": article_tags,
                "article_url": article_url,
                "article_content": article_content,
                "article_language": article_language,
                "created_ts": created_ts,
                "last_checked": last_checked
            }
            collection.insert_one(article_data)
            count+=1
            # send_to_teams_webhook('Elogroup New Article: '+article_title+' added to the collection.')
            mes_str = mes_str + article_title + " || "

    print("All Elogroup Articles processed.")
    elogroup_msg = "Elogroup Total New Articles Added:"+ str(count) + "\n" + mes_str
    # send_to_teams_webhook(elogroup_msg)
    return "All Elogroup Articles processed."