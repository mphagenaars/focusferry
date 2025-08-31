#!/usr/bin/env python3
"""
Unified Content Collector for FocusFerry
Configuration-driven collector that handles both RSS feeds and YouTube channels

This replaces the hardcoded approaches with a flexible, configuration-based system.
"""

import sys
from pathlib import Path
from datetime import datetime

# Add scripts directory to path for imports
sys.path.append(str(Path(__file__).parent))

from config_loader import ConfigLoader
from rss_collector import RSSCollector
from youtube_collector import YouTubeCollector
from content_integrator import integrate_rss_to_content_feed
from content_summarizer import summarize_rss_articles

class UnifiedContentCollector:
    """Configuration-driven content collector for all sources"""
    
    def __init__(self, config_name: str = "default"):
        self.config_loader = ConfigLoader(config_name)
        self.config = self.config_loader.load_config()
        
        # Initialize collectors
        self.rss_collector = RSSCollector()
        try:
            self.youtube_collector = YouTubeCollector()
        except ValueError as e:
            print(f"⚠️  YouTube API not available: {e}")
            self.youtube_collector = None
    
    def collect_all_content(self):
        """Collect content from all enabled sources"""
        print("🚀 Unified Content Collection")
        print("=" * 50)
        
        results = {
            'rss_feeds': [],
            'youtube_channels': [],
            'errors': []
        }
        
        # Collect RSS feeds
        print("\n📰 RSS Feeds Collection")
        print("-" * 30)
        rss_results = self._collect_rss_feeds()
        results['rss_feeds'] = rss_results
        
        # Collect YouTube channels
        print("\n📺 YouTube Channels Collection")
        print("-" * 30)
        youtube_results = self._collect_youtube_channels()
        results['youtube_channels'] = youtube_results
        
        return results
    
    def _collect_rss_feeds(self):
        """Collect from all enabled RSS feeds"""
        enabled_feeds = self.config_loader.get_enabled_rss_feeds()
        
        if not enabled_feeds:
            print("ℹ️  No RSS feeds enabled in configuration")
            return []
        
        print(f"📊 Found {len(enabled_feeds)} enabled RSS feeds")
        
        results = []
        for feed in enabled_feeds:
            try:
                print(f"\n🔍 Processing: {feed['name']}")
                
                # Use configured max_articles or default
                max_articles = feed.get('max_articles', 10)
                
                # Collect articles
                output_file = self.rss_collector.collect_from_feed(
                    feed_url=feed['url'],
                    source_name=self._normalize_source_name(feed['name']),
                    max_items=max_articles
                )
                
                if output_file:
                    results.append({
                        'name': feed['name'],
                        'source_name': self._normalize_source_name(feed['name']),
                        'file_path': output_file,
                        'success': True
                    })
                    print(f"✅ Success: {feed['name']}")
                else:
                    print(f"❌ Failed: {feed['name']}")
                    results.append({
                        'name': feed['name'],
                        'success': False,
                        'error': 'Collection failed'
                    })
                    
            except Exception as e:
                print(f"❌ Error collecting {feed['name']}: {e}")
                results.append({
                    'name': feed['name'],
                    'success': False,
                    'error': str(e)
                })
        
        return results
    
    def _collect_youtube_channels(self):
        """Collect from all enabled YouTube channels"""
        if not self.youtube_collector:
            print("❌ YouTube collector not available (API key missing)")
            return []
        
        enabled_channels = self.config_loader.get_enabled_youtube_channels()
        
        if not enabled_channels:
            print("ℹ️  No YouTube channels enabled in configuration")
            return []
        
        print(f"📊 Found {len(enabled_channels)} enabled YouTube channels")
        
        results = []
        for channel in enabled_channels:
            try:
                print(f"\n🔍 Processing: {channel['name']}")
                
                # Use configured max_videos or default
                max_videos = channel.get('max_videos', 10)
                
                # Collect videos using identifier or channel_id
                identifier = channel.get('identifier', channel.get('channel_id'))
                
                output_file = self.youtube_collector.collect_from_channel(
                    channel_identifier=identifier,
                    max_results=max_videos
                )
                
                if output_file:
                    results.append({
                        'name': channel['name'],
                        'identifier': identifier,
                        'file_path': output_file,
                        'success': True
                    })
                    print(f"✅ Success: {channel['name']}")
                else:
                    print(f"❌ Failed: {channel['name']}")
                    results.append({
                        'name': channel['name'],
                        'success': False,
                        'error': 'Collection failed'
                    })
                    
            except Exception as e:
                print(f"❌ Error collecting {channel['name']}: {e}")
                results.append({
                    'name': channel['name'],
                    'success': False,
                    'error': str(e)
                })
        
        return results
    
    def _normalize_source_name(self, name: str) -> str:
        """Convert display name to file-safe source name"""
        import re
        # Convert to lowercase, replace spaces/special chars with underscore
        normalized = re.sub(r'[^a-zA-Z0-9]+', '_', name.lower())
        # Remove leading/trailing underscores
        normalized = normalized.strip('_')
        return normalized
    
    def integrate_all_content(self):
        """Integrate all collected content into unified feed"""
        print("\n🔄 Content Integration")
        print("-" * 30)
        
        try:
            # This will integrate all RSS files found in data/rss/
            success = integrate_rss_to_content_feed()
            
            if success:
                print("✅ Content integration successful")
            else:
                print("ℹ️  No new content to integrate")
                
            return success
            
        except Exception as e:
            print(f"❌ Content integration failed: {e}")
            return False
    
    def generate_summaries(self):
        """Generate AI summaries for all new content"""
        print("\n🤖 AI Summary Generation")
        print("-" * 30)
        
        ai_settings = self.config_loader.get_ai_settings()
        
        if not ai_settings.get('summarization', {}).get('enabled', True):
            print("ℹ️  AI summarization disabled in configuration")
            return True
        
        try:
            success = summarize_rss_articles()
            
            if success:
                print("✅ AI summarization successful")
            else:
                print("ℹ️  No articles needed summarization")
                
            return success
            
        except Exception as e:
            print(f"❌ AI summarization failed: {e}")
            return False
    
    def run_full_pipeline(self):
        """Run the complete content collection pipeline"""
        print("🎯 FocusFerry Unified Content Collection Pipeline")
        print("=" * 60)
        
        start_time = datetime.now()
        
        # Step 1: Collect content
        collection_results = self.collect_all_content()
        
        # Step 2: Integrate content
        integration_success = self.integrate_all_content()
        
        # Step 3: Generate summaries
        summary_success = self.generate_summaries()
        
        # Summary
        end_time = datetime.now()
        duration = end_time - start_time
        
        print("\n" + "=" * 60)
        print("📊 PIPELINE SUMMARY")
        print("=" * 60)
        
        # RSS results
        rss_successful = len([r for r in collection_results['rss_feeds'] if r.get('success')])
        rss_total = len(collection_results['rss_feeds'])
        print(f"📰 RSS Feeds: {rss_successful}/{rss_total} successful")
        
        # YouTube results
        youtube_successful = len([r for r in collection_results['youtube_channels'] if r.get('success')])
        youtube_total = len(collection_results['youtube_channels'])
        print(f"📺 YouTube: {youtube_successful}/{youtube_total} successful")
        
        # Integration & Summaries
        print(f"🔄 Integration: {'✅ Success' if integration_success else '❌ Failed'}")
        print(f"🤖 AI Summaries: {'✅ Success' if summary_success else '❌ Failed'}")
        
        print(f"⏱️  Total time: {duration.total_seconds():.1f} seconds")
        
        # Overall success
        overall_success = (
            (rss_successful > 0 or youtube_successful > 0) and
            integration_success and
            summary_success
        )
        
        if overall_success:
            print("\n🎉 PIPELINE COMPLETED SUCCESSFULLY!")
            print("🔄 Ready for Hugo build & deploy")
        else:
            print("\n⚠️  PIPELINE COMPLETED WITH ISSUES")
            print("Check logs above for details")
        
        return overall_success


def main():
    """Main function to run unified content collection"""
    try:
        collector = UnifiedContentCollector("default")
        success = collector.run_full_pipeline()
        
        if success:
            print(f"\n✅ Task 2.4 enhanced: Configuration-driven collection complete!")
        else:
            print(f"\n❌ Collection pipeline failed")
            
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
