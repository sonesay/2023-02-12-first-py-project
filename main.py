import sys
from helpers.api_request import APIRequest
from helpers.web_scrapper import WebScraper

if __name__ == '__main__':
    api_key = 'TB7AST8FPLI9N1EA0AJCBHVOC694343Kmf6XiFTdlDld2XZBO7vikH0Mm4d4QHPLtMRASY08'
    api_request = APIRequest(api_key)

    scraper = WebScraper()
    # scraper.process_english_categories()
    scraper.scrape_full_article_page()
