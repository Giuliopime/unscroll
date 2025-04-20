import os
import pickle
import time
import random

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from config import INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD


def get_random_seconds(from_seconds, to_seconds):
    """
    Returns a random float number of seconds between two values.
    """
    assert from_seconds <= to_seconds, "from_seconds must be less than or equal to to_seconds"
    return random.uniform(from_seconds, to_seconds)


def sleep_for_random_seconds(from_seconds, to_seconds):
    """
    Sleeps for a random amount of time between from_seconds and to_seconds.
    """
    time.sleep(get_random_seconds(from_seconds, to_seconds))


def setup_browser():
    """
    Initializes and returns a new Chrome WebDriver instance with basic options.
    """
    print("Starting browser...")
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)


def load_cookies(driver, cookies_file):
    """
    Loads saved cookies from a file and adds them to the WebDriver.
    """
    if not os.path.exists(cookies_file):
        print(f"Cookies file not found: {cookies_file}")
        return False

    try:
        with open(cookies_file, "rb") as cookies:
            cookies_list = pickle.load(cookies)
            for cookie in cookies_list:
                driver.add_cookie(cookie)
        print("Cookies loaded")
        return True
    except Exception as e:
        print(f"Error loading cookies: {e}")
        return False


def login(driver, cookies_file):
    """
    Logs into Instagram using saved cookies if available, or enters credentials manually.
    Saves cookies to file after login.
    """
    driver.get("https://www.instagram.com/")
    sleep_for_random_seconds(2, 3)

    # Ensure data directory exists
    os.makedirs(os.path.dirname(cookies_file), exist_ok=True)

    if os.path.exists(cookies_file):
        print("Loading cookies...")
        cookies_loaded = load_cookies(driver, cookies_file)
        if cookies_loaded:
            driver.get("https://www.instagram.com/")  # Refresh after loading cookies
            sleep_for_random_seconds(2, 3)
            return

    # Check if credentials are available
    if not INSTAGRAM_USERNAME or not INSTAGRAM_PASSWORD:
        raise ValueError("Instagram credentials not found in environment variables. "
                         "Please set INSTAGRAM_USERNAME and INSTAGRAM_PASSWORD.")

    try:
        accept_cookies_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Allow all cookies')]")
        accept_cookies_button.click()
        print("Accepted cookies")
    except NoSuchElementException:
        print("Cookies already accepted")

    sleep_for_random_seconds(4, 5)

    username_input = driver.find_element(By.CSS_SELECTOR, "input[name='username']")
    password_input = driver.find_element(By.CSS_SELECTOR, "input[name='password']")

    username_input.send_keys(INSTAGRAM_USERNAME)
    sleep_for_random_seconds(1, 2)
    password_input.send_keys(INSTAGRAM_PASSWORD)
    sleep_for_random_seconds(1, 2)

    login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    login_button.click()
    print("Logged in")
    sleep_for_random_seconds(7, 8)

    try:
        driver.find_element(By.XPATH, "//button[text()='Save info']").click()
    except NoSuchElementException:
        print("No 'Save info' button found")

    sleep_for_random_seconds(7, 8)
    pickle.dump(driver.get_cookies(), open(cookies_file, "wb"))
    print("Stored login cookies")