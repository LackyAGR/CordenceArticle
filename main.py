# Imports
from pymongo import MongoClient
from datetime import datetime
from scrapper.cordence_scrapper import cordence_scrape_function, store_articles_in_db_insights, store_articles_in_db_latest
from scrapper.north_highland_scrapper import north_highland_scrapper_function, store_north_highland_articles_in_db
from utils import send_to_teams_webhook

if __name__ == "__main__":
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['cordence_article_db']  
    collection = db['articles']  

    # Cordence Scrapper Insights
    url_insights = "https://cordence.com/insights/"
    cordence_insight_scrape_data = cordence_scrape_function(url_insights)
    res_insight = store_articles_in_db_insights(cordence_insight_scrape_data, collection)
    send_to_teams_webhook(res_insight)

    url_insights = "https://cordence.com/latest/"
    cordence_latest_scrape_data = cordence_scrape_function(url_insights)
    res_latest = store_articles_in_db_latest(cordence_latest_scrape_data, collection)
    send_to_teams_webhook(res_latest)

    # North Highland Scrapper For All Category
    url_insights = "https://www.northhighland.com/insights"
    north_highland_insight_scrape_data = north_highland_scrapper_function(url_insights)
    res_north_highland = store_north_highland_articles_in_db(north_highland_insight_scrape_data, collection)
    send_to_teams_webhook(res_north_highland)


    
    

    



