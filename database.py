import json
import sqlite3
from datetime import datetime

from models import InstagramPost


class DatabaseManager:
    def __init__(self, db_name):
        """Initialize database connection"""
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def setup_tables(self):
        """Create necessary database tables if they don't exist"""
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS summaries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            summary TEXT NOT NULL,
            scraped_at TIMESTAMP NOT NULL
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS post_summary (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            summary_id INTEGER NOT NULL,
            post_id TEXT NOT NULL,
            handle TEXT,
            reference_url TEXT NOT NULL,
            caption TEXT,
            post_date TIMESTAMP NOT NULL,
            FOREIGN KEY (summary_id) REFERENCES summaries(id)
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS last_scrape_metadata (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            last_scrape TIMESTAMP,
            handles TEXT -- JSON array of strings
        )
        """)

        self.conn.commit()

    def get_scrape_metadata(self):
        """Get handles and last scrape date from database"""
        # Get handles
        self.cursor.execute("SELECT handles FROM last_scrape_metadata WHERE id = 1")
        result = self.cursor.fetchone()

        handles = []
        if result and result[0]:
            try:
                handles = json.loads(result[0])
            except json.JSONDecodeError:
                handles = []

        # Get last scrape date
        self.cursor.execute("SELECT last_scrape FROM last_scrape_metadata WHERE id = 1")
        result = self.cursor.fetchone()

        last_scrape_date = None
        if result and result[0]:
            try:
                last_scrape_date = datetime.fromisoformat(result[0])
            except ValueError:
                last_scrape_date = None

        return handles, last_scrape_date

    def save_summary(self, summary_text, scraped_at, posts):
        """
        Save summary and related posts to database

        Args:
            summary_text (str): The summary text
            scraped_at (str): ISO format timestamp when scraping was done
            posts (list): List of InstagramPost objects
        """
        # Insert summary
        self.cursor.execute("""
        INSERT INTO summaries (summary, scraped_at)
        VALUES (?, ?)
        """, (summary_text, scraped_at))

        self.conn.commit()
        summary_id = self.cursor.lastrowid

        # Insert posts
        for post in posts:
            self.cursor.execute("""
            INSERT INTO post_summary (
                summary_id, post_id, handle, reference_url, caption, post_date
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """, (
                summary_id,
                post.post_id,
                post.handle,
                post.url,
                post.caption,
                post.date.isoformat()
            ))

        self.conn.commit()

    def update_scrape_metadata(self, scraped_at, handles=None):
        """Update last scrape metadata"""
        if handles is not None:
            handles_json = json.dumps(handles)
            self.cursor.execute("""
            INSERT INTO last_scrape_metadata (id, last_scrape, handles)
            VALUES (1, ?, ?)
            ON CONFLICT(id) DO UPDATE SET 
                last_scrape = excluded.last_scrape,
                handles = excluded.handles
            """, (scraped_at, handles_json))
        else:
            self.cursor.execute("""
            INSERT INTO last_scrape_metadata (id, last_scrape)
            VALUES (1, ?)
            ON CONFLICT(id) DO UPDATE SET last_scrape = excluded.last_scrape
            """, (scraped_at,))

        self.conn.commit()

    def get_posts(self, limit=100, offset=0):
        """
        Retrieve posts from the database

        Returns:
            list: List of InstagramPost objects
        """
        self.cursor.execute("""
        SELECT post_id, caption, post_date, reference_url, handle
        FROM post_summary
        ORDER BY post_date DESC
        LIMIT ? OFFSET ?
        """, (limit, offset))

        posts = []
        for row in self.cursor.fetchall():
            post_id, caption, date_str, url, handle = row
            post = InstagramPost(
                post_id=post_id,
                caption=caption,
                date=datetime.fromisoformat(date_str),
                url=url,
                handle=handle
            )
            posts.append(post)

        return posts

    def close(self):
        """Close database connection"""
        self.conn.close()