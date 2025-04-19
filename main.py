# main.py
import json
import os
import random
from datetime import datetime, timedelta

from browser_utils import setup_browser, login
from database import DatabaseManager
from scraper import InstagramScraper
from config import COOKIES_FILE, DATABASE_FILE, DAYS_TO_LOOK_BACK, DEFAULT_HANDLES


def main():
    # Initialize database
    db_manager = DatabaseManager(DATABASE_FILE)
    db_manager.setup_tables()

    # Get handles and last scrape date from database
    handles, last_scrape_date = db_manager.get_scrape_metadata()
    if not handles:
        handles = DEFAULT_HANDLES
    random.shuffle(handles)

    # Determine minimum date for scraping (DAYS_TO_LOOK_BACK days ago or last scrape date, whichever is earlier)
    days_ago = datetime.now() - timedelta(days=DAYS_TO_LOOK_BACK)
    min_date = min(last_scrape_date, days_ago) if last_scrape_date else days_ago

    # Setup browser and login
    driver = setup_browser()
    login(driver, COOKIES_FILE)

    # Initialize scraper and collect posts
    scraper = InstagramScraper(driver)
    posts = scraper.scrape_posts(min_date, handles)

    # Create a summary and save data to database
    summary_text = "# Example Summary\nWill be created with ai."
    scraped_at = datetime.now().isoformat()

    # Save data to database
    db_manager.save_summary(summary_text, scraped_at, posts)

    # Update last scrape metadata
    db_manager.update_scrape_metadata(scraped_at)

    # Close database connection and browser
    db_manager.close()
    driver.quit()


if __name__ == "__main__":
    main()