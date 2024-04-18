# Imports
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
from pymongo import MongoClient
from datetime import datetime
from utils import generate_uid, send_to_teams_webhook

# Working code for State of matter
def state_Of_Matter_Scrapper_Function(url):
    data = []

    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        articles = soup.find_all('li', class_='case-study-archive__Li-n3mjjm-0')

        for article in articles:
            link_element = article.find('a', class_='typography__IsolatedLink-wvc8x7-11 jGoQyz')
            article_url = urljoin(url, link_element['href']) if link_element else None

            title = link_element.text.strip() if link_element else None

            response_article = requests.get(article_url)
            if response_article.status_code == 200:
                soup_article = BeautifulSoup(response_article.content, 'html.parser')
                tags_element = soup_article.find('div', class_='tags')
                tags = [tag.text.strip() for tag in tags_element.find_all('span', class_='typography__Metadata-wvc8x7-12 gqrLQe tag')] if tags_element else None

                content_elements = soup_article.find_all('p', class_='typography__BodyText-wvc8x7-7 hJJAGI')
                content = '\n'.join([content_element.text.strip() for content_element in content_elements]) if content_elements else None

                data.append({
                    'title': title,
                    'tags': tags,
                    'link': article_url,
                    'content': content
                })
            else:
                print(f"Error: Failed to fetch article URL {article_url}")

    else:
        print(f"Error: Failed to fetch URL {url}")
        return None

    return data


#Store State Of Matter Article in DB
def store_State_Of_Matter_Articles_In_Db(state_Of_Matter_Scrape_Data, collection):
    count = 0
    mes_str = ""
    for article in state_Of_Matter_Scrape_Data:
        if(article['title'] == None or article['link'] == None ):
            pass
        # Extract required information
        uid = generate_uid(prefix="AR")
        org_name = "State Of Matter"
        article_category = ""
        article_subcategory = ""
        article_title = article['title']
        article_tags = article['tags']
        article_url = article['link']
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
                "article_tags": article_tags,
                "article_url": article_url,
                "article_content": article_content,
                "article_language": article_language,
                "created_ts": created_ts,
                "last_checked": last_checked
            }
            collection.insert_one(article_data)
            count+=1
            # send_to_teams_webhook('State Of Matter New Article: '+article_title+' added to the collection.')
            mes_str = mes_str + article_title + " || "

    print("All State Of Matter Articles processed.")
    state_of_matter_msg = "State Of Matter Total New Articles Added: "+ str(count) + "\n" + mes_str
    # send_to_teams_webhook(state_of_matter_msg)
    return "All State of Matter Articles processed."