"""Script for testing schedule module."""
import time

import schedule

from scraper import scrape_books 

schedule.every().day.at("16:39").do(scrape_books, is_save=True, books_count=5)

while True:
    schedule.run_pending()
    time.sleep(1)