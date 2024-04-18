# Imports
from pymongo import MongoClient
from datetime import datetime
from scrapper.cordence_scrapper import cordence_scrape_function, store_articles_in_db_insights, store_articles_in_db_latest
from scrapper.north_highland_scrapper import north_highland_scrapper_function, store_north_highland_articles_in_db
from scrapper.state_of_matter_scrapper import state_Of_Matter_Scrapper_Function, store_State_Of_Matter_Articles_In_Db
from scrapper.key_to_way_scrapper import key_To_Way_Scrapper_Function, store_Key_To_Way_Articles_In_Db
from scrapper.avalon_consulting_scrapper import avalon_Consulting_Scrapper_Function, store_Avalon_Consulting_Articles_In_Db
from scrapper.oresys_scrapper import oresys_Scraper_Function, oresys_CaseStudies_Scrapper_Function, store_Oresys_Articles_In_Db, store_Oresys_CaseStudies_Articles_In_Db
from scrapper.elogroup_scrapper import elogroup_Scrape_Function, store_Elogroup_Articles_In_Db
from scrapper.horvath_scrapper import horvath_MediaCenter_Scrape_Function, store_Horvath_MediaCenter_Articles_In_Db, horvath_Press_Scrape_Function, store_Horvath_Press_Articles_In_Db
from scrapper.twynstragudde_scrapper import twynstragudde_Scrape_Function, store_Twynstragudde_Articles_In_Db
from utils import send_to_teams_webhook

if __name__ == "__main__":
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['cordence_article_db']  
    collection = db['articles']  
    time = datetime.now()
    # send_to_teams_webhook("Started at " + str(time))

    # ** Cordence Scrapper Insights
    url_insights = "https://cordence.com/insights/"
    cordence_insight_scrape_data = cordence_scrape_function(url_insights)
    res_insight = store_articles_in_db_insights(cordence_insight_scrape_data, collection)
    # send_to_teams_webhook(res_insight)

    url_insights = "https://cordence.com/latest/"
    cordence_latest_scrape_data = cordence_scrape_function(url_insights)
    res_latest = store_articles_in_db_latest(cordence_latest_scrape_data, collection)
    # send_to_teams_webhook(res_latest)

    #** North Highland Scrapper For All Category
    url_insights = "https://www.northhighland.com/insights"
    north_highland_insight_scrape_data = north_highland_scrapper_function(url_insights)
    res_north_highland = store_north_highland_articles_in_db(north_highland_insight_scrape_data, collection)
    # send_to_teams_webhook(res_north_highland)
    
    #** State Of Matter Scrapper For Case Studies
    url_CaseStudies = "https://www.sofm.com.au/case-studies/"
    state_Of_Matter_Scrape_Data = state_Of_Matter_Scrapper_Function(url_CaseStudies)
    res_State_Of_Matter = store_State_Of_Matter_Articles_In_Db(state_Of_Matter_Scrape_Data, collection)
    # send_to_teams_webhook(res_State_Of_Matter)
    
    #** Key to Way Scrapper For Case Studies
    url_CaseStudies = "https://keytoway.kr/en/cases"
    key_To_Way_Scrape_Data = key_To_Way_Scrapper_Function(url_CaseStudies)
    res_Key_To_Way = store_Key_To_Way_Articles_In_Db(key_To_Way_Scrape_Data, collection)
    # send_to_teams_webhook(res_Key_To_Way)
    
    #** Avalon Consulting Scrapper For Case Studies
    url_CaseStudies = ["https://www.consultavalon.com/category/insights/","https://www.consultavalon.com/category/our-blog/","https://www.consultavalon.com/category/press-room/", "https://www.consultavalon.com/category/events/", "https://www.consultavalon.com/category/callout/", "https://www.consultavalon.com/category/webinars/", "https://www.consultavalon.com/category/the-avalon-edge-series/", "https://www.consultavalon.com/category/alumni-spotlight/"]
    avalon_Consulting_Scrape_Data = avalon_Consulting_Scrapper_Function(url_CaseStudies)
    res_Avalon_Consulting = store_Avalon_Consulting_Articles_In_Db(avalon_Consulting_Scrape_Data, collection)
    # send_to_teams_webhook(res_Avalon_Consulting)
    
    #** Oresys Scrapper for white papers and Webinars
    urls = ["https://www.oresys.eu/category/livres-blancs/", "https://www.oresys.eu/category/evenement/replay/"]
    oresys_Scrape_Data = oresys_Scraper_Function(urls)
    res_Oresys = store_Oresys_Articles_In_Db(oresys_Scrape_Data, collection)
    # send_to_teams_webhook(res_Oresys)
    
    url_Oresys_CaseStudies = "https://www.oresys.eu/category/cas-client/"
    oresys_CaseStudies_Scrape_Data = oresys_CaseStudies_Scrapper_Function(url_Oresys_CaseStudies)
    res_Oresys_CaseStudies = store_Oresys_CaseStudies_Articles_In_Db(oresys_CaseStudies_Scrape_Data, collection)
    # send_to_teams_webhook(res_Oresys_CaseStudies)
    
    #** Elogroup Scraper for Insights
    url_Elogroup = "https://elogroup.com/en/insight/"
    elogorup_Scrape_Data = elogroup_Scrape_Function(url_Elogroup)
    res_Elogroup = store_Elogroup_Articles_In_Db(elogorup_Scrape_Data, collection)
    # send_to_teams_webhook(res_Elogroup)
    
    #** Horvath Scraper For all articles
    url_Horvath_MediaCenter = ["https://www.horvath-partners.com/en/media-center/studies", "https://www.horvath-partners.com/en/media-center/featured-articles", "https://www.horvath-partners.com/en/media-center/books", "https://www.horvath-partners.com/en/media-center/white-paper"]
    horvath_MediaCenter_Scrape_Data = horvath_MediaCenter_Scrape_Function(url_Horvath_MediaCenter)
    res_Horvath_MediaCenter = store_Horvath_MediaCenter_Articles_In_Db(horvath_MediaCenter_Scrape_Data, collection)
    # send_to_teams_webhook(res_Horvath_MediaCenter)
    
    url_Horvath_Press = "https://www.horvath-partners.com/en/press"
    horvath_Press_Scrape_Data = horvath_Press_Scrape_Function(url_Horvath_Press)
    res_Horvath_Press = store_Horvath_Press_Articles_In_Db(horvath_Press_Scrape_Data, collection)
    # send_to_teams_webhook(res_Horvath_Press)
    
    #** Twynstragudde Scraper For all articles
    url_Twynstragudde = "https://www.twynstragudde.nl/inzichten"
    twynstragudde_Scrape_Data = twynstragudde_Scrape_Function(url_Twynstragudde)
    res_Twynstragudde = store_Twynstragudde_Articles_In_Db(twynstragudde_Scrape_Data, collection)
    # send_to_teams_webhook(res_Twynstragudde)
    