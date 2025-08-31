#!/usr/bin/env python3
"""
RSS Feed Collector for FocusFerry
Task 2.1: Fetch articles from RSS feeds

This script fetches articles from RSS feeds and saves them to JSON files
in a format compatible with the unified content feed.
"""

import json
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

class RSSCollector:
    def __init__(self):
        self.output_dir = Path(__file__).parent.parent / 'data' / 'rss'
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # User agent to avoid blocking
        self.headers = {
            'User-Agent': 'FocusFerry/1.0 (News Aggregator; https://hgnrs.nl)'
        }
    
    def fetch_rss_feed(self, feed_url, max_items=10):
        """
        Fetch and parse RSS feed
        
        Args:
            feed_url (str): URL of the RSS feed
            max_items (int): Maximum number of articles to fetch
            
        Returns:
            list: List of article dictionaries
        """
        try:
            print(f"🔍 Fetching RSS feed: {feed_url}")
            
            # Fetch RSS content
            response = requests.get(feed_url, headers=self.headers, timeout=30)
            response.raise_for_status()
            
            # Parse XML
            root = ET.fromstring(response.content)
            
            # Find channel info
            channel = root.find('channel')
            if channel is None:
                raise ValueError("Invalid RSS feed - no channel element found")
            
            # Extract channel metadata
            channel_title = self.get_text(channel.find('title'), 'Unknown Source')
            channel_description = self.get_text(channel.find('description'), '')
            channel_link = self.get_text(channel.find('link'), '')
            
            print(f"📰 Channel: {channel_title}")
            
            # Extract articles
            articles = []
            items = channel.findall('item')[:max_items]
            
            for item in items:
                article = self.parse_rss_item(item, channel_title, channel_link)
                if article:
                    articles.append(article)
            
            print(f"✅ Parsed {len(articles)} articles")
            return articles
            
        except requests.RequestException as e:
            print(f"❌ Network error fetching RSS feed: {e}")
            return []
        except ET.ParseError as e:
            print(f"❌ XML parsing error: {e}")
            return []
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return []
    
    def parse_rss_item(self, item, channel_title, channel_link):
        """Parse a single RSS item into our article format"""
        try:
            title = self.get_text(item.find('title'), 'Untitled')
            link = self.get_text(item.find('link'), '')
            description = self.get_text(item.find('description'), '')
            pub_date = self.get_text(item.find('pubDate'), '')
            
            # Try to parse publication date
            published_at = self.parse_date(pub_date)
            
            # Clean description (remove HTML tags if present)
            clean_description = self.clean_html(description)
            
            # Truncate description for preview
            if len(clean_description) > 300:
                clean_description = clean_description[:297] + '...'
            
            # Extract domain from channel link for source identification
            domain = urlparse(channel_link).netloc if channel_link else 'unknown'
            
            article = {
                'article_id': self.generate_article_id(link),
                'title': title.strip(),
                'description': clean_description.strip(),
                'url': link.strip(),
                'published_at': published_at,
                'source_title': channel_title.strip(),
                'source_url': channel_link.strip(),
                'source_domain': domain,
                'collected_at': datetime.now().isoformat()
            }
            
            return article
            
        except Exception as e:
            print(f"⚠️ Error parsing RSS item: {e}")
            return None
    
    def get_text(self, element, default=''):
        """Safely extract text from XML element"""
        if element is not None and element.text:
            return element.text.strip()
        return default
    
    def clean_html(self, text):
        """Basic HTML tag removal"""
        import re
        # Remove HTML tags
        clean = re.sub(r'<[^>]+>', '', text)
        # Replace HTML entities
        clean = clean.replace('&amp;', '&')
        clean = clean.replace('&lt;', '<')
        clean = clean.replace('&gt;', '>')
        clean = clean.replace('&quot;', '"')
        clean = clean.replace('&#39;', "'")
        return clean
    
    def parse_date(self, date_string):
        """Parse RSS date string to ISO format"""
        if not date_string:
            return datetime.now().isoformat()
        
        try:
            # Try common RSS date formats
            import email.utils
            timestamp = email.utils.parsedate_to_datetime(date_string)
            return timestamp.isoformat()
        except:
            # Fallback to current time if parsing fails
            return datetime.now().isoformat()
    
    def generate_article_id(self, url):
        """Generate a unique ID for the article based on URL"""
        import hashlib
        if not url:
            return f"rss_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Use last part of URL path or hash
        path = urlparse(url).path
        if path and len(path) > 1:
            # Use filename or last path segment
            article_id = path.split('/')[-1]
            if article_id and len(article_id) > 3:
                return article_id.replace('.html', '').replace('.php', '')
        
        # Fallback: hash the URL
        url_hash = hashlib.md5(url.encode()).hexdigest()[:12]
        return f"rss_{url_hash}"
    
    def save_articles_to_json(self, articles, source_name):
        """Save articles to JSON file"""
        filename = f"{source_name}_articles.json"
        output_file = self.output_dir / filename
        
        data = {
            'collected_at': datetime.now().isoformat(),
            'source_name': source_name,
            'total_articles': len(articles),
            'articles': articles
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Saved {len(articles)} articles to {output_file}")
        return output_file
    
    def collect_from_feed(self, feed_url, source_name, max_items=10):
        """
        Main method to collect articles from an RSS feed
        
        Args:
            feed_url (str): RSS feed URL
            source_name (str): Name for the source (used in filename)
            max_items (int): Maximum articles to collect
            
        Returns:
            Path or None: Path to saved JSON file, or None if failed
        """
        print(f"🚀 Starting RSS collection for: {source_name}")
        
        # Fetch articles
        articles = self.fetch_rss_feed(feed_url, max_items)
        
        if not articles:
            print(f"❌ No articles collected from {source_name}")
            return None
        
        # Save to JSON
        output_file = self.save_articles_to_json(articles, source_name)
        
        print(f"\n🎉 Task 2.1 Progress: RSS collection successful!")
        print(f"📊 Collected {len(articles)} articles from {source_name}")
        print(f"📁 Saved to: {output_file}")
        
        return output_file


def main():
    """Test RSS collection with OpenAI news feed"""
    try:
        collector = RSSCollector()
        
        # Test with OpenAI RSS feed
        openai_feed_url = "https://openai.com/news/rss.xml"
        source_name = "openai"
        
        print("🧪 Testing Task 2.1: RSS Feed Collection")
        print(f"🎯 Target: {openai_feed_url}")
        print(f"📰 Source: {source_name}")
        print()
        
        # Collect articles
        result = collector.collect_from_feed(
            feed_url=openai_feed_url,
            source_name=source_name,
            max_items=10
        )
        
        if result:
            print(f"\n✅ Task 2.1 SUCCESS!")
            print(f"📂 Output: {result}")
            print(f"🔄 Next: Task 2.2 - Article summarization")
        else:
            print(f"\n❌ Task 2.1 FAILED!")
            print("Check network connection and RSS feed URL")
            
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()
