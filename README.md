# Instagram Post Scraper

This tool scrapes Instagram posts from specified handles, stores them in a SQLite database and creates a markdown pdf summary with AI.

## Files Structure

- `main.py`: Entry point for the application
- `browser_utils.py`: Browser setup and login functions
- `scraper.py`: Instagram post scraping functionality
- `database.py`: Database management operations
- `config.py`: Configuration settings
- `.env`: Environment variables for sensitive data (credentials)

## Setup and Installation

1. Install required packages:
   ```
   pip install -r requirements.txt
   ```

2. Create a `.env` file in the project root with your credentials:
   ```
   INSTAGRAM_USERNAME=your_username
   INSTAGRAM_PASSWORD=your_password
   ```

3. Create the data directory:
   ```
   mkdir -p data
   ```

4. Run the scraper:
   ```
   python main.py
   ```

## Features
- Authenticates with Instagram via cookies or username/password
- Uses environment variables for secure credential management
- Scrapes posts from multiple Instagram handles
- Filters posts by date
- Stores post data in a SQLite database
- Handles pinned posts appropriately
- Creates summaries of scraped content

## Database Structure
- `summaries`: Stores summary information about scraped posts
- `post_summary`: Stores details about individual posts
- `last_scrape_metadata`: Stores information about the last scraping run

## Usage Notes
- The script uses a random delay between actions to mimic human behavior
- Be mindful of Instagram's rate limits to avoid being blocked
- Login cookies are saved to disk for future sessions
- Never commit your `.env` file to version control