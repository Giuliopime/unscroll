import random
import signal
import subprocess
from datetime import datetime, timedelta

from browser_utils import setup_browser, login, sleep_for_random_seconds
from cli_utils import prompt_for_goal
from database import DatabaseManager
from file_utls import create_summary_output_file, create_output_file_name, create_pdf
from scraper import InstagramScraper
from config import COOKIES_FILE, DATABASE_FILE, DAYS_TO_LOOK_BACK, DEFAULT_HANDLES, MODEL_NAME
from summarizer import ContentSummarizer


def main():
    # Start ollama
    print("Starting ollama")
    ollama_sh = subprocess.Popen(["ollama", "run", MODEL_NAME])
    sleep_for_random_seconds(5, 5)

    # Ask for goal
    goal = prompt_for_goal()

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

    # Close browser once done
    sleep_for_random_seconds(1, 1)
    driver.quit()

    # Create a summary and save data to database
    summarizer = ContentSummarizer(model=MODEL_NAME)
    summary = summarizer.create_unified_summary_per_single_post(posts, goal)

    # Close ollama
    ollama_sh.send_signal(signal.SIGINT)
    subprocess.Popen(["osascript", "-e", 'tell app "Ollama" to quit'])

    # Save data to database
    scraped_at = datetime.now().isoformat()
    db_manager.save_summary(summary, scraped_at, posts)
    # Update last scrape metadata
    db_manager.update_scrape_metadata(scraped_at)

    # Close database connection
    db_manager.close()

    # Create pdf
    file_name = create_output_file_name(goal=goal)
    output_file = create_summary_output_file(goal=goal)
    create_pdf(summary, file_name, output_file)

    # Open PDF
    subprocess.run(["open", output_file])

if __name__ == "__main__":
    main()