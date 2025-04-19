# models.py
from datetime import datetime


class InstagramPost:
    """
    Class representing an Instagram post with its metadata and content.
    """

    def __init__(self, post_id, caption, date, url, handle=None):
        """
        Initialize a new Instagram post object.

        Args:
            post_id (str): The unique ID of the post
            caption (str): The HTML content of the post caption
            date (datetime): The timestamp of when the post was created
            url (str): The full URL to the post
            handle (str, optional): The Instagram handle of the post author
        """
        self.post_id = post_id
        self.caption = caption
        self.date = date
        self.url = url
        self.handle = handle

    def __str__(self):
        """String representation of the post for logging and debugging."""
        date_str = self.date.strftime('%Y-%m-%d %H:%M:%S')
        caption_preview = self.caption[:100] + "..." if len(self.caption) > 100 else self.caption
        handle_str = f" from {self.handle}" if self.handle else ""
        return f"Post {self.post_id}{handle_str}: {date_str} - {caption_preview}"

    def to_dict(self):
        """Convert post to dictionary for database storage or serialization."""
        return {
            'post_id': self.post_id,
            'caption': self.caption,
            'date': self.date.isoformat(),
            'url': self.url,
            'handle': self.handle
        }

    @classmethod
    def from_dict(cls, data):
        """Create a post object from a dictionary."""
        return cls(
            post_id=data['post_id'],
            caption=data['caption'],
            date=datetime.fromisoformat(data['date']),
            url=data['url'],
            handle=data.get('handle')
        )