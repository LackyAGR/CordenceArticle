# Imports
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
from pymongo import MongoClient
from datetime import datetime
from utils import generate_uid, send_to_teams_webhook
import time

def oresys_Scraper_Function(urls):
    data = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

    for url in urls:
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                articles = soup.find_all('article', class_='preview-post')

                for article in articles:
                    link_element = article.find('a', href=True)
                    article_url = link_element['href'] if link_element else None

                    title_element = article.find('h3', class_='post-title')
                    title = title_element.text.strip() if title_element else None

                    tags_element = article.find('ul', class_='tags')
                    tags = [tag.text.strip() for tag in tags_element.find_all('a')] if tags_element else None

                    data.append({
                        'title': title,
                        'tags': tags,
                        'link': article_url
                    })

                    # Adding a delay between requests to avoid triggering rate limits
                    time.sleep(1)
            else:
                print(f"Error: Failed to fetch URL {url}")
        except Exception as e:
            print("Error:", e)

    return data


#Store Oresys Article in DB
def store_Oresys_Articles_In_Db(oresys_Scrape_Data, collection):
    count = 0
    mes_str = ""
    for article in oresys_Scrape_Data:
        if(article['title'] == None or article['link'] == None ):
            pass
        # Extract required information
        uid = generate_uid(prefix="AR")
        org_name = "Oresys"
        article_category = ""
        article_subcategory = ""
        article_title = article['title']
        article_tags = article['tags']
        article_url = article['link']
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
            # send_to_teams_webhook('Oresys New Article: '+article_title+' added to the collection.')
            mes_str = mes_str + article_title + " || "

    print("All Oresys Articles processed.")
    oresys_msg = "Oresys Total New Articles Added:"+ str(count) + "\n" + mes_str
    # send_to_teams_webhook(oresys_msg)
    return "All Oresys Articles processed."


#** Oresys CaseStudies scraper function and db store function

def oresys_CaseStudies_Scrapper_Function(url):
    data = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    session = requests.Session()

    try:
        response = session.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            articles = soup.find_all('article', class_='preview-post-case')

            for article in articles:
                title_element = article.find('h3', class_='post-title')
                title = title_element.text.strip() if title_element else None

                tags_element = article.find('ul', class_='tags')
                tags = [tag.text.strip() for tag in tags_element.find_all('a')] if tags_element else None

                description_element = article.find('div', class_='preview-description')
                description = description_element.text.strip() if description_element else None

                data.append({
                    'title': title,
                    'tags': tags,
                    'description': description
                })

                # Adding a delay between requests to avoid triggering rate limits
                time.sleep(1)
        else:
            print(f"Error: Failed to fetch URL {url}")
            return None
    except Exception as e:
        print("Error:", e)
        return None

    return data


#Store Oresys CaseStudies Article in DB
def store_Oresys_CaseStudies_Articles_In_Db(oresys_CaseStudies_Scrape_Data, collection):
    count = 0
    mes_str = ""
    for article in oresys_CaseStudies_Scrape_Data:
        if(article['title'] == None):
            pass
        # Extract required information
        uid = generate_uid(prefix="AR")
        org_name = "Oresys CaseStudies"
        article_category = ""
        article_subcategory = ""
        article_title = article['title']
        article_tags = article['tags']
        article_url = ""
        article_content = article['description']
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
            # send_to_teams_webhook('Oresys New Article: '+article_title+' added to the collection.')
            mes_str = mes_str + article_title + " || "

    print("All Oresys CaseStudies Articles processed.")
    oresys_CaseStudies_msg = "Oresys CaseStudies Total New Articles Added:"+ str(count) + "\n" + mes_str
    # send_to_teams_webhook(oresys_CaseStudies_msg)
    return "All Oresys CaseStudies Articles processed."