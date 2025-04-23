# Instagram Post Scraper

This tool scrapes Instagram posts from specified handles, stores them in a SQLite database, and creates a markdown PDF summary using AI.

[![demo](https://img.youtube.com/vi/WoVhrl_4a28/0.jpg)](https://www.youtube.com/embed/WoVhrl_4a28)

## Files Structure

- `main.py`: Entry point for the application  
- `browser_utils.py`: Browser setup and login functions  
- `cli_utls.py`: functions to prompt for usage from the cli
- `file_utils.py`: folder and pdf creation operations
- `scraper.py`: Instagram post scraping functionality  
- `database.py`: Database management operations  
- `models.py`: classes used trought the program
- `summarizer.py`: ollama interaction functions
- `config.py`: Configuration settings  
- `.env`: Environment variables for sensitive data (credentials)

## Setup and Installation

1. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a .env file in the project root with your Instagram credentials:
   ```
   INSTAGRAM_USERNAME=your_username
   INSTAGRAM_PASSWORD=your_password
   ```

3. Create the data directory (if it doesn’t exist):
   ```
   mkdir -p data
   ```

4. Run the scraper:
   ```
   python main.py
   ```

## Requirements
- Ollama must be installed and running on your system: https://ollama.com  
- The model specified in the `MODEL_NAME` variable in `config.py` must be pulled using Ollama before running the script. For example:
   ```
   ollama pull mistral:7b-instruct
   ```

## Features
- Authenticates with Instagram via cookies or username/password
- Uses environment variables for secure credential management
- Scrapes posts from multiple Instagram handles
- Filters posts by date
- Detects and counts pinned posts
- Stores post data in a SQLite database
- Summarizes post content using a local AI model
- Outputs a Markdown file and a PDF summary

## Database Structure
- summaries: Stores summary information about scraped sessions
- post_summary: Stores details about individual posts
- last_scrape_metadata: Tracks information about the last scraping run

## Usage Notes
- The script introduces random delays between actions to mimic human behavior
- Be mindful of Instagram’s rate limits to avoid account issues
- Login cookies are saved locally to improve future login speed
- Never commit your .env file to version control
