#!/usr/bin/env python3
"""
YouTube Video Collector for FocusFerry
Task 1.1: Fetch video list from one YouTube channel

This script uses the YouTube Data API v3 to fetch recent videos from a specified channel
and saves the video metadata to a JSON file.
"""

import json
import os
from datetime import datetime
from pathlib import Path

from googleapiclient.discovery import build
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class YouTubeCollector:
    def __init__(self):
        self.api_key = os.getenv('YOUTUBE_API_KEY')
        if not self.api_key:
            raise ValueError("YOUTUBE_API_KEY not found in environment variables")
        
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)
        self.output_dir = Path(__file__).parent.parent / 'data' / 'youtube'
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def get_channel_id_from_username(self, username):
        """Get channel ID from channel username/handle"""
        try:
            request = self.youtube.channels().list(
                part='id',
                forUsername=username
            )
            response = request.execute()
            
            if response['items']:
                return response['items'][0]['id']
            else:
                # Try with @ handle format
                search_request = self.youtube.search().list(
                    part='snippet',
                    q=username,
                    type='channel',
                    maxResults=1
                )
                search_response = search_request.execute()
                
                if search_response['items']:
                    return search_response['items'][0]['snippet']['channelId']
                
                raise ValueError(f"Channel not found: {username}")
                
        except Exception as e:
            print(f"Error finding channel {username}: {e}")
            return None
    
    def get_channel_videos(self, channel_id, max_results=10):
        """Fetch recent videos from a YouTube channel"""
        try:
            # Get channel's uploads playlist ID
            channel_request = self.youtube.channels().list(
                part='contentDetails',
                id=channel_id
            )
            channel_response = channel_request.execute()
            
            if not channel_response['items']:
                raise ValueError(f"Channel not found: {channel_id}")
            
            uploads_playlist_id = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
            
            # Get videos from uploads playlist
            playlist_request = self.youtube.playlistItems().list(
                part='snippet',
                playlistId=uploads_playlist_id,
                maxResults=max_results,
                order='date'
            )
            playlist_response = playlist_request.execute()
            
            videos = []
            for item in playlist_response['items']:
                snippet = item['snippet']
                video_data = {
                    'video_id': snippet['resourceId']['videoId'],
                    'title': snippet['title'],
                    'description': snippet['description'][:200] + '...' if len(snippet['description']) > 200 else snippet['description'],
                    'published_at': snippet['publishedAt'],
                    'channel_title': snippet['channelTitle'],
                    'channel_id': snippet['channelId'],
                    'thumbnail_url': snippet['thumbnails'].get('medium', {}).get('url', ''),
                    'collected_at': datetime.now().isoformat()
                }
                videos.append(video_data)
            
            return videos
            
        except Exception as e:
            print(f"Error fetching videos from channel {channel_id}: {e}")
            return []
    
    def save_videos_to_json(self, videos, filename):
        """Save video data to JSON file"""
        output_file = self.output_dir / filename
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                'collected_at': datetime.now().isoformat(),
                'total_videos': len(videos),
                'videos': videos
            }, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Saved {len(videos)} videos to {output_file}")
        return output_file
    
    def collect_from_channel(self, channel_identifier, max_results=10):
        """Main method to collect videos from a channel"""
        print(f"🔍 Fetching videos from channel: {channel_identifier}")
        
        # Try to get channel ID (handle both channel ID and username)
        if channel_identifier.startswith('UC') and len(channel_identifier) == 24:
            # Already a channel ID
            channel_id = channel_identifier
        else:
            # Try to get channel ID from username
            channel_id = self.get_channel_id_from_username(channel_identifier)
            if not channel_id:
                return None
        
        print(f"📺 Channel ID: {channel_id}")
        
        # Fetch videos
        videos = self.get_channel_videos(channel_id, max_results)
        
        if videos:
            # Save to JSON file
            filename = f"{channel_identifier.replace('@', '').replace(' ', '_')}_videos.json"
            output_file = self.save_videos_to_json(videos, filename)
            return output_file
        else:
            print("❌ No videos found")
            return None

def main():
    """Test the YouTube collector with a known tech channel"""
    try:
        collector = YouTubeCollector()
        
        # Test with Fireship channel (known tech YouTuber)
        test_channel = "Fireship"
        result = collector.collect_from_channel(test_channel, max_results=10)
        
        if result:
            print(f"\n🎉 Task 1.1 SUCCESS!")
            print(f"Generated: {result}")
            print(f"Next: Task 1.2 - Transcript collection")
        else:
            print("❌ Task 1.1 FAILED - No videos collected")
            
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        print("Please set YOUTUBE_API_KEY in your .env file")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
