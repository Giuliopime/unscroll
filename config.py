"""
Configuration settings for the Instagram scraper
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Instagram login credentials from environment variables
INSTAGRAM_USERNAME = os.environ.get("INSTAGRAM_USERNAME")
INSTAGRAM_PASSWORD = os.environ.get("INSTAGRAM_PASSWORD")

# Default Instagram handles to scrape
DEFAULT_HANDLES = [
    "ilmuretto_official",
    # "after_caposile",
    # "cusnautico",
    # "suoniuniversitari",
    # "unitinpovo",
    # "unidea_tn",
    # "trentino.eventi",
    # "dolcevitaeventi",
    # "basemen.tn"
]

# Browser settings
COOKIES_FILE = os.path.join("data", "cookies.pkl")

# Database settings
DATABASE_FILE = os.path.join("data", "instagram_scraper.db")

# Scraping settings
DAYS_TO_LOOK_BACK = 2

# Model settings
MODEL_NAME = "mistral:7b-instruct"