#!/usr/bin/env python3
"""
Content Integrator for FocusFerry
Integrates RSS articles into the unified content feed alongside YouTube videos
"""

import json
from datetime import datetime
from pathlib import Path

def integrate_rss_to_content_feed():
    """Integrate RSS articles into the unified content feed"""
    
    # Paths
    rss_file = Path(__file__).parent.parent / "data" / "rss" / "openai_articles.json"
    content_feed_file = Path(__file__).parent.parent / "data" / "content_feed.json"
    
    # Read existing content feed
    if content_feed_file.exists():
        with open(content_feed_file, 'r', encoding='utf-8') as f:
            content_feed = json.load(f)
        print(f"📂 Loaded existing content feed with {content_feed['total_items']} items")
    else:
        # Create new content feed if it doesn't exist
        content_feed = {
            "generated_at": datetime.now().isoformat(),
            "total_items": 0,
            "items": []
        }
        print("📂 Created new content feed")
    
    # Read RSS articles
    if not rss_file.exists():
        print(f"❌ RSS file not found: {rss_file}")
        return False
    
    with open(rss_file, 'r', encoding='utf-8') as f:
        rss_data = json.load(f)
    
    print(f"📰 Found {rss_data['total_articles']} articles from {rss_data['source_name']}")
    
    # Convert RSS articles to unified content feed format
    new_items = []
    existing_ids = {item['id'] for item in content_feed['items']}
    
    for article in rss_data['articles']:
        # Create unified item ID
        unified_id = f"rss_{rss_data['source_name']}_{article['article_id']}"
        
        # Skip if already exists
        if unified_id in existing_ids:
            print(f"⏭️  Skipping existing article: {article['title']}")
            continue
        
        # Convert to unified format
        unified_item = {
            "id": unified_id,
            "type": "article",
            "source": {
                "platform": "rss",
                "site_name": article['source_title'],
                "site_url": article['source_url'],
                "domain": article['source_domain']
            },
            "content": {
                "title": article['title'],
                "description": article['description'],
                "url": article['url'],
                "thumbnail_url": ""  # RSS articles don't have thumbnails by default
            },
            "metadata": {
                "published_at": article['published_at'],
                "collected_at": article['collected_at']
            }
        }
        
        new_items.append(unified_item)
        print(f"✅ Added: {article['title']}")
    
    if not new_items:
        print("ℹ️  No new articles to add")
        return True
    
    # Add new items to content feed
    content_feed['items'].extend(new_items)
    
    # Sort all items by published date (newest first)
    content_feed['items'].sort(
        key=lambda x: x['metadata']['published_at'], 
        reverse=True
    )
    
    # Update metadata
    content_feed['total_items'] = len(content_feed['items'])
    content_feed['generated_at'] = datetime.now().isoformat()
    
    # Save updated content feed
    with open(content_feed_file, 'w', encoding='utf-8') as f:
        json.dump(content_feed, f, indent=2, ensure_ascii=False)
    
    print(f"\n🎉 Content feed integration complete!")
    print(f"📊 Total items in feed: {content_feed['total_items']}")
    print(f"📊 New articles added: {len(new_items)}")
    print(f"💾 Updated: {content_feed_file}")
    
    return True

def main():
    """Main function to test RSS integration"""
    print("🔄 Task 2.1 Step 2: RSS to Content Feed Integration")
    print("🎯 Adding OpenAI articles to unified content feed")
    print()
    
    success = integrate_rss_to_content_feed()
    
    if success:
        print(f"\n✅ Task 2.1 Step 2 SUCCESS!")
        print(f"🔄 Next: Task 2.1 Step 3 - Frontend updates")
    else:
        print(f"\n❌ Task 2.1 Step 2 FAILED!")

if __name__ == "__main__":
    main()
