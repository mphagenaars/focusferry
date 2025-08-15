#!/usr/bin/env python3
"""
Content Feed Migrator for FocusFerry
Migrates existing YouTube data to unified content feed format
"""

import os
import json
from pathlib import Path
from datetime import datetime

def migrate_youtube_to_unified():
    """Migrate YouTube videos to unified content feed"""
    
    # Paths
    youtube_file = Path(__file__).parent.parent / "data" / "youtube" / "matthew_berman_videos.json"
    content_feed_file = Path(__file__).parent.parent / "data" / "content_feed.json"
    
    # Read existing YouTube data
    with open(youtube_file, 'r', encoding='utf-8') as f:
        youtube_data = json.load(f)
    
    # Create unified content feed
    content_feed = {
        "generated_at": datetime.now().isoformat(),
        "total_items": 0,
        "items": []
    }
    
    # Convert YouTube videos to unified format
    for video in youtube_data['videos']:
        # Only include videos that have AI summaries
        if 'ai_summary' not in video:
            print(f"⏭️  Skipping {video['video_id']} - no AI summary")
            continue
            
        unified_item = {
            "id": f"youtube_{video['video_id']}",
            "type": "video",
            "source": {
                "platform": "youtube",
                "channel_name": video['channel_title'],
                "channel_id": video['channel_id']
            },
            "content": {
                "title": video['title'],
                "description": video.get('description', ''),
                "ai_summary": video['ai_summary'],
                "url": f"https://youtube.com/watch?v={video['video_id']}",
                "thumbnail_url": video['thumbnail_url']
            },
            "metadata": {
                "published_at": video['published_at'],
                "collected_at": video['collected_at'],
                "summarized_at": video.get('summary_generated_at', video['collected_at'])
            }
        }
        
        content_feed['items'].append(unified_item)
        print(f"✅ Migrated: {video['title']}")
    
    # Sort by published date (newest first)
    content_feed['items'].sort(
        key=lambda x: x['metadata']['published_at'], 
        reverse=True
    )
    
    content_feed['total_items'] = len(content_feed['items'])
    
    # Save unified content feed
    with open(content_feed_file, 'w', encoding='utf-8') as f:
        json.dump(content_feed, f, indent=2, ensure_ascii=False)
    
    print(f"\n🎉 Migration complete!")
    print(f"📊 Total items: {content_feed['total_items']}")
    print(f"💾 Saved to: {content_feed_file}")

def main():
    """Main migration function"""
    print("🚀 Starting migration to unified content feed...")
    migrate_youtube_to_unified()

if __name__ == "__main__":
    main()
