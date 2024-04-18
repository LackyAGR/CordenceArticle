# Imports
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
from pymongo import MongoClient
from datetime import datetime
from utils import generate_uid, send_to_teams_webhook

def horvath_MediaCenter_Scrape_Function(urls):
    all_articles = []
    for url in urls:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            article_elements = soup.find_all('div', class_='col-4')
            for article_element in article_elements:
                link_element = article_element.find('a')
                if link_element:
                    title_element = link_element.find('h4')
                    if title_element:
                        title = title_element.text.strip()
                        link_url = urljoin(url, link_element['href'])
                        all_articles.append({'title': title, 'link_url': link_url})
        else:
            print(f"Error: Failed to fetch URL {url}")

    return all_articles


#Store Horvath MediaCenter Article in DB
def store_Horvath_MediaCenter_Articles_In_Db(horvath_MediaCenter_Scrape_Data, collection):
    count = 0
    mes_str = ""
    for article in horvath_MediaCenter_Scrape_Data:
        if(article['title'] == None or article['link_url'] == None ):
            pass
        # Extract required information
        uid = generate_uid(prefix="AR")
        org_name = "Horvath MediaCenter"
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
                "article_tags": article_tags,
                "article_url": article_url,
                "article_content": article_content,
                "article_language": article_language,
                "created_ts": created_ts,
                "last_checked": last_checked
            }
            collection.insert_one(article_data)
            count+=1
            # send_to_teams_webhook('Horvath MediaCenter Article: '+article_title+' added to the collection.')
            mes_str = mes_str + article_title + " || "

    print("All Horvath MediaCenter Articles processed.")
    horvath_MediaCenter_msg = "Horvath MediaCenter Total New Articles Added:"+ str(count) + "\n" + mes_str
    # send_to_teams_webhook(horvath_MediaCenter_msg)
    return "All Horvath MediaCenter Articles processed."


# #? Horvath Press Articles scraping function and storing function

def horvath_Press_Scrape_Function(url):
    articles = []
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        article_elements = soup.find_all('div', class_='article')

        for article_element in article_elements:
            # Extracting date
            date_element = article_element.find('time', itemprop='datePublished')
            date = date_element.text.strip() if date_element else None

            # Extracting title
            title_element = article_element.find('span', itemprop='headline')
            title = title_element.text.strip() if title_element else None

            # Extracting description
            description_element = article_element.find('div', itemprop='description')
            description = description_element.text.strip() if description_element else None

            # Extracting link URL
            link_element = article_element.find('a', class_='more')
            link_url = urljoin(url, link_element['href']) if link_element else None

            articles.append({
                'date': date,
                'title': title,
                'description': description,
                'link_url': link_url
            })
    else:
        print(f"Error: Failed to fetch URL {url}")
        return None

    return articles


#Store Horvath Press Article in DB
def store_Horvath_Press_Articles_In_Db(horvath_Press_Scrape_Data, collection):
    count = 0
    mes_str = ""
    for article in horvath_Press_Scrape_Data:
        if(article['title'] == None or article['link_url'] == None ):
            pass
        # Extract required information
        uid = generate_uid(prefix="AR")
        org_name = "Horvath Press"
        article_category = ""
        article_subcategory = ""
        article_title = article['title']
        article_tags = ""
        article_url = article['link_url']
        article_description = article['description']
        article_publish_date = article['date']
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
                "article_publish_date": article_publish_date,
                "article_language": article_language,
                "created_ts": created_ts,
                "last_checked": last_checked
            }
            collection.insert_one(article_data)
            count+=1
            # send_to_teams_webhook('Horvath Press New Article: '+article_title+' added to the collection.')
            mes_str = mes_str + article_title + " || "

    print("All Horvath Press Articles processed.")
    horvath_Press_msg = "Horvath Press Total New Articles Added:"+ str(count) + "\n" + mes_str
    # send_to_teams_webhook(horvath_Press_msg)
    return "All Horvath Press Articles processed."
