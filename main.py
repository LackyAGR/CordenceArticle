# Imports
from pymongo import MongoClient
from datetime import datetime
from scrapper.cordence_scrapper import cordence_scrape_function, store_articles_in_db_insights, store_articles_in_db_latest
from scrapper.north_highland_scrapper import north_highland_scrapper_function, store_north_highland_articles_in_db


if __name__ == "__main__":
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['cordence_article_db']  
    collection = db['articles']  

    # Cordence Scrapper Insights
    # url_insights = "https://cordence.com/insights/"
    # cordence_insight_scrape_data = cordence_scrape_function(url_insights)
    # store_articles_in_db_insights(cordence_insight_scrape_data, collection)

    # url_insights = "https://cordence.com/latest/"
    # cordence_insight_scrape_data = cordence_scrape_function(url_insights)
    # store_articles_in_db_latest(cordence_insight_scrape_data, collection)

    # North Highland Scrapper For All Category
    url_insights = "https://www.northhighland.com/insights"
    north_highland_insight_scrape_data = north_highland_scrapper_function(url_insights)
    store_north_highland_articles_in_db(north_highland_insight_scrape_data, collection)


    
    

    



