# scraper.p
from datetime import datetime
from urllib.parse import urlparse

from selenium.common import ElementNotInteractableException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from browser_utils import sleep_for_random_seconds
from models import InstagramPost


class InstagramScraper:
    def __init__(self, driver):
        self.driver = driver

    def go_to_profile(self, handle):
        """Navigate to an Instagram profile by handle"""
        self.driver.get(f"https://www.instagram.com/{handle}/")
        sleep_for_random_seconds(6, 7)

    def go_to_first_post(self, handle):
        """
        Opens the first post on an Instagram profile.

        Returns:
            bool: True if the post was found and opened, False otherwise.
        """
        try:
            self.driver.find_element(By.XPATH,
                                     f"//a[starts-with(@href, '/{handle}/p/') or starts-with(@href, '/{handle}/reel/')]").click()
            sleep_for_random_seconds(1, 2)
            return True
        except NoSuchElementException:
            print(f"No posts found for {handle}")
            return False

    def scrape_post(self, handle=None):
        """
        Scrapes the caption and timestamp of the currently opened post.

        Args:
            handle (str, optional): The Instagram handle associated with this post

        Returns:
            InstagramPost or None: An InstagramPost object if scraping was successful, None otherwise
        """
        post_caption_containers = self.driver.find_elements(By.XPATH, "//h1[@dir='auto']")
        url = self.driver.current_url
        post_id = urlparse(url).path.strip("/").split("/")[1]

        try:
            # time_elements = self.driver.find_elements(
            #     By.XPATH,
            #     "//time[contains(text(), 'minutes ago') or contains(text(), 'hours ago') or contains(text(), 'days ago') or contains(text(), 'day ago') or contains(text(), 'hour ago') or contains(text(), 'minute ago')]"
            # )
            time_elements = self.driver.find_elements(By.XPATH, f"//a[contains(@href, '/p/{post_id}') or contains(@href, '/reel/{post_id}')]//time")

            if time_elements:
                time_element = time_elements[-1]
            else:
                return None
        except NoSuchElementException:
            return None

        if post_caption_containers:
            caption = post_caption_containers[-1].get_attribute("innerHTML")
        else:
            return None

        date_str = time_element.get_attribute("datetime")
        date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")

        return InstagramPost(post_id, caption, date, url, handle)

    def click_next_post(self):
        """
        Clicks on the "Next" button to go to the next post if available.

        Returns:
            bool: True if the next button was found and clicked, False otherwise.
        """
        try:
            next_buttons = self.driver.find_elements(By.XPATH, "//button[.//span[contains(@style, 'rotate')]]")
            if next_buttons:
                next_button = next_buttons[-1]
                next_button.click()
                sleep_for_random_seconds(3, 4)
                return True
            else:
                return False
        except ElementNotInteractableException:
            print("Could not click on 'Next' button.")
            return False
        except NoSuchElementException:
            print("No more posts to scrape")
            return False

    def scrape_posts(self, min_date, handles):
        """
        Scrapes posts from multiple Instagram handles.

        Args:
            min_date (datetime): Minimum date for posts to be included
            handles (list): List of Instagram handles to scrape

        Returns:
            list: List of InstagramPost objects
        """
        posts = []

        for handle in handles:
            print(f"Scraping {handle}...")
            self.go_to_profile(handle)

            try:
                pinned_posts = self.driver.find_elements(By.CSS_SELECTOR, "svg[aria-label='Pinned post icon']")
                pinned_posts_count = len(pinned_posts)
            except NoSuchElementException:
                pinned_posts_count = 0

            pinned_clicked = 0

            if self.go_to_first_post(handle):
                post = self.scrape_post(handle)

                if post:
                    if post.date >= min_date:
                        posts.append(post)
                        print(f"Scraped {post}")
                    else:
                        pinned_clicked += 1
                        if pinned_clicked > pinned_posts_count:
                            continue
                else:
                    print("No posts found for this handle. Skipping...")
                    continue

                # Continue to next posts
                while self.click_next_post():
                    post = self.scrape_post(handle)

                    if post:
                        if post.date >= min_date:
                            posts.append(post)
                            print(f"Scraped {post}")
                        else:
                            pinned_clicked += 1
                            if pinned_clicked > pinned_posts_count:
                                break
                    else:
                        break

        return posts