# Imports
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
from pymongo import MongoClient
from datetime import datetime
from utils import generate_uid, send_to_teams_webhook

# working for all pages of Avlon cunsulting
def avalon_Consulting_Scrapper_Function(urls):
    data = []

    for url in urls:
        while url:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                content_elements = soup.find_all('div', class_='inner-wrap')

                for content_element in content_elements:
                    title_element = content_element.find('h3', class_='title')
                    title = title_element.text.strip() if title_element else None

                    category_element = content_element.find('span', class_='meta-category')
                    category = category_element.text.strip() if category_element else None

                    link_element = content_element.find('a', class_='entire-meta-link')
                    link_url = link_element['href'] if link_element else None

                    data.append({
                        'title': title,
                        'category': category,
                        'link_url': link_url
                    })

                next_page_element = soup.find('a', class_='next')

                if next_page_element:
                    next_page_url_fragment = next_page_element['href']
                    next_page_url = urljoin(url, next_page_url_fragment)
                    url = next_page_url
                else:
                    url = None
            else:
                print(f"Error: Failed to fetch URL {url}")
                return None

    return data


#Store State Of Matter Article in DB
def store_Avalon_Consulting_Articles_In_Db(Avalon_Consulting_Scrape_Data, collection):
    count = 0
    mes_str = ""
    for article in Avalon_Consulting_Scrape_Data:
        if(article['title'] == None or article['url'] == None ):
            pass
        # Extract required information
        uid = generate_uid(prefix="AR")
        org_name = "Avalon Consulting"
        article_category = ""
        article_subcategory = ""
        article_title = article['title']
        article_tags = ""
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

    print("All Avalon Consulting Articles processed.")
    avalon_Consulting_msg = "Avalon Consulting Total New Articles Added:"+ str(count) + "\n" + mes_str
    # send_to_teams_webhook(avalon_Consulting_msg)
    return "All Avalon Consulting Articles processed."