# Imports
from pymongo import MongoClient
from datetime import datetime
from scrapper.cordence_scrapper import cordence_scrape_function, store_articles_in_db_insights, store_articles_in_db_latest
from scrapper.north_highland_scrapper import north_highland_scrapper_function, store_north_highland_articles_in_db
from scrapper.state_of_matter_scrapper import state_Of_Matter_Scrapper_Function, store_State_Of_Matter_Articles_In_Db
from scrapper.key_to_way_scrapper import key_To_Way_Scrapper_Function, store_Key_To_Way_Articles_In_Db
from scrapper.avalon_consulting_scrapper import avalon_Consulting_Scrapper_Function, store_Avalon_Consulting_Articles_In_Db
from utils import send_to_teams_webhook

if __name__ == "__main__":
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['cordence_article_db']  
    collection = db['articles']  
    time = datetime.now()
    send_to_teams_webhook("Started at " + str(time))

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
    
    # State Of Matter Scrapper For Case Studies
    url_CaseStudies = "https://www.sofm.com.au/case-studies/"
    state_Of_Matter_Scrape_Data = state_Of_Matter_Scrapper_Function(url_CaseStudies)
    res_State_Of_Matter = store_State_Of_Matter_Articles_In_Db(state_Of_Matter_Scrape_Data, collection)
    send_to_teams_webhook(res_State_Of_Matter)
    
    # Key to Way Scrapper For Case Studies
    url_CaseStudies = "https://keytoway.kr/en/cases"
    key_To_Way_Scrape_Data = key_To_Way_Scrapper_Function(url_CaseStudies)
    res_Key_To_Way = store_Key_To_Way_Articles_In_Db(key_To_Way_Scrape_Data, collection)
    send_to_teams_webhook(res_Key_To_Way)
    
    # Avalon Consulting Scrapper For Case Studies
    url_CaseStudies = ["https://www.consultavalon.com/category/insights/","https://www.consultavalon.com/category/our-blog/","https://www.consultavalon.com/category/press-room/", "https://www.consultavalon.com/category/events/", "https://www.consultavalon.com/category/callout/", "https://www.consultavalon.com/category/webinars/", "https://www.consultavalon.com/category/the-avalon-edge-series/", "https://www.consultavalon.com/category/alumni-spotlight/"]
    avalon_Consulting_Scrape_Data = avalon_Consulting_Scrapper_Function(url_CaseStudies)
    res_Avalon_Consulting = store_Avalon_Consulting_Articles_In_Db(avalon_Consulting_Scrape_Data, collection)
    send_to_teams_webhook(res_Avalon_Consulting)


