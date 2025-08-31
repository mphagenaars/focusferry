#!/usr/bin/env python3
"""
Configuration Loader for FocusFerry
Handles loading and validation of content source configuration
"""

import yaml
import os
from pathlib import Path
from typing import Dict, List, Any, Optional

class ConfigLoader:
    """Loads and validates FocusFerry configuration"""
    
    def __init__(self, config_name: str = "default"):
        self.config_name = config_name
        self.config_dir = Path(__file__).parent.parent / "config"
        self.config_file = self.config_dir / f"{config_name}.yaml"
        self._config = None
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        if not self.config_file.exists():
            raise FileNotFoundError(f"Configuration file not found: {self.config_file}")
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self._config = yaml.safe_load(f)
                
            self._validate_config()
            return self._config
            
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML configuration: {e}")
        except Exception as e:
            raise RuntimeError(f"Error loading configuration: {e}")
    
    def _validate_config(self):
        """Validate configuration structure"""
        if not self._config:
            raise ValueError("Configuration is empty")
        
        # Check required sections
        required_sections = ['content_sources']
        for section in required_sections:
            if section not in self._config:
                raise ValueError(f"Missing required configuration section: {section}")
        
        content_sources = self._config['content_sources']
        
        # Validate RSS feeds
        if 'rss_feeds' in content_sources:
            for feed in content_sources['rss_feeds']:
                required_fields = ['name', 'url', 'enabled']
                for field in required_fields:
                    if field not in feed:
                        raise ValueError(f"RSS feed missing required field '{field}': {feed}")
        
        # Validate YouTube channels
        if 'youtube_channels' in content_sources:
            for channel in content_sources['youtube_channels']:
                required_fields = ['name', 'identifier', 'enabled']
                for field in required_fields:
                    if field not in channel:
                        raise ValueError(f"YouTube channel missing required field '{field}': {channel}")
    
    def get_enabled_rss_feeds(self) -> List[Dict[str, Any]]:
        """Get list of enabled RSS feeds"""
        if not self._config:
            self.load_config()
        
        rss_feeds = self._config.get('content_sources', {}).get('rss_feeds', [])
        return [feed for feed in rss_feeds if feed.get('enabled', False)]
    
    def get_enabled_youtube_channels(self) -> List[Dict[str, Any]]:
        """Get list of enabled YouTube channels"""
        if not self._config:
            self.load_config()
        
        youtube_channels = self._config.get('content_sources', {}).get('youtube_channels', [])
        return [channel for channel in youtube_channels if channel.get('enabled', False)]
    
    def get_ai_settings(self) -> Dict[str, Any]:
        """Get AI processing settings"""
        if not self._config:
            self.load_config()
        
        return self._config.get('ai_settings', {})
    
    def get_collection_settings(self) -> Dict[str, Any]:
        """Get content collection settings"""
        if not self._config:
            self.load_config()
        
        return self._config.get('collection_settings', {})
    
    def save_config(self, config: Dict[str, Any]):
        """Save configuration to YAML file"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                yaml.dump(config, f, default_flow_style=False, allow_unicode=True, indent=2)
            
            self._config = config
            
        except Exception as e:
            raise RuntimeError(f"Error saving configuration: {e}")
    
    def update_feed_status(self, feed_name: str, enabled: bool, feed_type: str = "rss"):
        """Enable/disable a specific feed"""
        if not self._config:
            self.load_config()
        
        content_sources = self._config['content_sources']
        
        if feed_type == "rss":
            feeds = content_sources.get('rss_feeds', [])
        elif feed_type == "youtube":
            feeds = content_sources.get('youtube_channels', [])
        else:
            raise ValueError(f"Unknown feed type: {feed_type}")
        
        # Find and update the feed
        for feed in feeds:
            if feed['name'] == feed_name:
                feed['enabled'] = enabled
                self.save_config(self._config)
                return True
        
        raise ValueError(f"Feed not found: {feed_name}")


def main():
    """Test the configuration loader"""
    try:
        print("🔧 Testing Configuration Loader")
        
        config_loader = ConfigLoader("default")
        config = config_loader.load_config()
        
        print(f"✅ Configuration loaded successfully")
        
        # Test RSS feeds
        rss_feeds = config_loader.get_enabled_rss_feeds()
        print(f"📰 Enabled RSS feeds: {len(rss_feeds)}")
        for feed in rss_feeds:
            print(f"  - {feed['name']}: {feed['url']}")
        
        # Test YouTube channels
        youtube_channels = config_loader.get_enabled_youtube_channels()
        print(f"📺 Enabled YouTube channels: {len(youtube_channels)}")
        for channel in youtube_channels:
            print(f"  - {channel['name']}: {channel['identifier']}")
        
        # Test AI settings
        ai_settings = config_loader.get_ai_settings()
        print(f"🤖 AI settings loaded: {len(ai_settings)} sections")
        
        print("\n🎉 Configuration system working correctly!")
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")

if __name__ == "__main__":
    main()
