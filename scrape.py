#!/usr/bin/env python3
"""
AI News Digest - RSS Scraper
Scrapes RSS feeds and saves articles to JSON files with audience targeting.
"""

import json
import logging
import os
from datetime import datetime
from typing import Dict, List, Any
import feedparser
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# RSS Feed Configuration
RSS_FEEDS = {
    "audience_1": [  # Marketing/SEO focus
        {
            "name": "Ben's Bites",
            "url": "https://www.bensbites.co/rss",
            "audience": "audience_1"
        },
        {
            "name": "The Rundown AI",
            "url": "https://www.therundown.ai/feed",
            "audience": "audience_1"
        },
        {
            "name": "Marketing AI Institute",
            "url": "https://www.marketingaiinstitute.com/blog/rss.xml",
            "audience": "audience_1"
        },
        {
            "name": "Search Engine Journal",
            "url": "https://www.searchenginejournal.com/feed/",
            "audience": "audience_1"
        },
        {
            "name": "Google AI Blog",
            "url": "https://blog.google/technology/ai/feed/",
            "audience": "audience_1"
        },
        {
            "name": "Search Engine Land",
            "url": "https://searchengineland.com/feed",
            "audience": "audience_1"
        },
        {
            "name": "Moz Blog",
            "url": "https://moz.com/blog/feed",
            "audience": "audience_1"
        },
        {
            "name": "Ahrefs Blog",
            "url": "https://ahrefs.com/blog/feed",
            "audience": "audience_1"
        },
        {
            "name": "SEMrush Blog",
            "url": "https://www.semrush.com/blog/feed",
            "audience": "audience_1"
        },
        {
            "name": "Google Search Central Blog",
            "url": "https://developers.google.com/search/blog/atom.xml",
            "audience": "audience_1"
        }
    ],
    "audience_2": [  # Compliance/Ethics focus
        {
            "name": "AI Policy Exchange",
            "url": "https://aipolicyexchange.org/feed/",
            "audience": "audience_2"
        },
        {
            "name": "Future of Privacy Forum",
            "url": "https://fpf.org/feed/",
            "audience": "audience_2"
        },
        {
            "name": "AI Ethics Journal",
            "url": "https://www.aiethicsjournal.org/feed/",
            "audience": "audience_2"
        },
        {
            "name": "MIT Technology Review",
            "url": "https://www.technologyreview.com/feed/",
            "audience": "audience_2"
        },
        {
            "name": "IAPP Privacy",
            "url": "https://iapp.org/news/rss/",
            "audience": "audience_2"
        },
        {
            "name": "DataEthiek.info",
            "url": "https://www.dataethiek.info/nieuws/rss",
            "audience": "audience_2"
        }
    ]
}

def clean_text(text: str) -> str:
    """Clean and normalize text content."""
    if not text:
        return ""
    
    # Remove HTML tags
    soup = BeautifulSoup(text, 'html.parser')
    text = soup.get_text()
    
    # Normalize whitespace
    text = ' '.join(text.split())
    
    return text.strip()

def extract_article_data(entry, source_name: str, audience: str) -> Dict[str, Any]:
    """Extract relevant data from a feed entry."""
    try:
        # Get publication date
        if hasattr(entry, 'published_parsed') and entry.published_parsed:
            timestamp = datetime(*entry.published_parsed[:6]).isoformat()
        elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
            timestamp = datetime(*entry.updated_parsed[:6]).isoformat()
        else:
            timestamp = datetime.now().isoformat()
        
        # Extract summary
        summary = ""
        if hasattr(entry, 'summary'):
            summary = clean_text(entry.summary)
        elif hasattr(entry, 'description'):
            summary = clean_text(entry.description)
        
        # Extract title
        title = clean_text(entry.title) if hasattr(entry, 'title') else ""
        
        # Extract link
        link = entry.link if hasattr(entry, 'link') else ""
        
        return {
            "title": title,
            "summary": summary,
            "link": link,
            "source": source_name,
            "audience": audience,
            "timestamp": timestamp
        }
    except Exception as e:
        logger.error(f"Error extracting data from entry: {e}")
        return None

def scrape_feed(feed_config: Dict[str, str]) -> List[Dict[str, Any]]:
    """Scrape a single RSS feed and return articles."""
    articles = []
    
    try:
        logger.info(f"Scraping feed: {feed_config['name']} ({feed_config['url']})")
        
        # Fetch feed using requests (better SSL handling)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(feed_config['url'], headers=headers, timeout=10, verify=True)
        response.raise_for_status()
        
        # Parse RSS feed
        feed = feedparser.parse(response.content)
        
        if feed.bozo:
            logger.warning(f"Feed parsing issues for {feed_config['name']}: {feed.bozo_exception}")
        
        # Process entries
        for entry in feed.entries:
            article_data = extract_article_data(
                entry, 
                feed_config['name'], 
                feed_config['audience']
            )
            
            if article_data and article_data['title'] and article_data['link']:
                articles.append(article_data)
        
        logger.info(f"Found {len(articles)} articles from {feed_config['name']}")
        
    except Exception as e:
        logger.error(f"Error scraping {feed_config['name']}: {e}")
    
    return articles

def save_articles_to_json(articles: List[Dict[str, Any]], date_str: str):
    """Save articles to JSON file for the given date."""
    if not articles:
        logger.info("No articles to save")
        return
    
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    filename = f"data/{date_str}.json"
    
    try:
        # Load existing data if file exists
        existing_data = []
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
        
        # Add new articles
        all_articles = existing_data + articles
        
        # Remove duplicates based on link
        seen_links = set()
        unique_articles = []
        for article in all_articles:
            if article['link'] not in seen_links:
                seen_links.add(article['link'])
                unique_articles.append(article)
        
        # Save to file
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(unique_articles, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved {len(unique_articles)} articles to {filename}")
        
    except Exception as e:
        logger.error(f"Error saving articles to {filename}: {e}")

def main():
    """Main scraping function."""
    logger.info("Starting AI News Digest scraper")
    
    # Get current date
    date_str = datetime.now().strftime('%Y-%m-%d')
    
    all_articles = []
    
    # Scrape all feeds
    for audience, feeds in RSS_FEEDS.items():
        logger.info(f"Processing feeds for {audience}")
        
        for feed_config in feeds:
            articles = scrape_feed(feed_config)
            all_articles.extend(articles)
    
    # Save all articles
    save_articles_to_json(all_articles, date_str)
    
    logger.info(f"Scraping completed. Total articles: {len(all_articles)}")

if __name__ == "__main__":
    main() 