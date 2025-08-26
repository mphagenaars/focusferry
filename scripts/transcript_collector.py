#!/usr/bin/env python3
"""
YouTube Transcript Collector for FocusFerry
Task 1.2: Fetch transcript/captions from YouTube videos

This script uses the youtube-transcript-api to download captions/subtitles
from YouTube videos and saves them as text files.
"""

import os
import re
from pathlib import Path
from datetime import datetime

try:
    from youtube_transcript_api import YouTubeTranscriptApi
    from youtube_transcript_api.formatters import TextFormatter
except ImportError:
    print("❌ youtube-transcript-api not installed")
    print("Run: pip install youtube-transcript-api")
    exit(1)


class TranscriptCollector:
    def __init__(self):
        self.output_dir = Path(__file__).parent.parent / 'transcripts'
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.formatter = TextFormatter()
    
    def clean_transcript_text(self, text):
        """Clean and format transcript text"""
        # Remove extra whitespace and newlines
        text = re.sub(r'\s+', ' ', text)
        
        # Remove common transcript artifacts
        text = re.sub(r'\[Music\]|\[Applause\]|\[Laughter\]', '', text, flags=re.IGNORECASE)
        
        # Clean up punctuation spacing
        text = re.sub(r'\s+([,.!?])', r'\1', text)
        
        return text.strip()
    
    def get_video_transcript(self, video_id, languages=['en', 'en-US']):
        """
        Fetch transcript for a single video
        
        Args:
            video_id (str): YouTube video ID
            languages (list): Preferred languages for transcript
            
        Returns:
            dict: {'success': bool, 'transcript': str, 'language': str, 'error': str}
        """
        try:
            print(f"🔍 Fetching transcript for video: {video_id}")
            
            # Create API instance
            api = YouTubeTranscriptApi()
            
            # Try to get transcript list
            transcript_list = api.list(video_id)
            
            transcript = None
            used_language = None
            
            # First try manually created transcripts in preferred languages
            for lang in languages:
                try:
                    transcript = transcript_list.find_manually_created_transcript([lang])
                    used_language = lang
                    print(f"✅ Found manual transcript in {lang}")
                    break
                except:
                    continue
            
            # If no manual transcript, try auto-generated
            if not transcript:
                for lang in languages:
                    try:
                        transcript = transcript_list.find_generated_transcript([lang])
                        used_language = lang
                        print(f"✅ Found auto-generated transcript in {lang}")
                        break
                    except:
                        continue
            
            # If still no transcript, try any available language
            if not transcript:
                try:
                    # Get first available transcript
                    available_transcripts = list(transcript_list)
                    if available_transcripts:
                        transcript = available_transcripts[0]
                        used_language = transcript.language_code
                        print(f"✅ Found transcript in {used_language} (fallback)")
                    else:
                        return {
                            'success': False,
                            'transcript': '',
                            'language': '',
                            'error': 'No transcripts available for this video'
                        }
                except Exception as e:
                    return {
                        'success': False,
                        'transcript': '',
                        'language': '',
                        'error': f'No transcripts found: {str(e)}'
                    }
            
            # Fetch the transcript data
            transcript_data = transcript.fetch()
            
            # Format as plain text
            transcript_text = self.formatter.format_transcript(transcript_data)
            
            # Clean the text
            clean_text = self.clean_transcript_text(transcript_text)
            
            return {
                'success': True,
                'transcript': clean_text,
                'language': used_language,
                'error': ''
            }
            
        except Exception as e:
            return {
                'success': False,
                'transcript': '',
                'language': '',
                'error': f'Error fetching transcript: {str(e)}'
            }
    
    def save_transcript_to_file(self, video_id, transcript_data, video_title=""):
        """Save transcript to text file"""
        filename = f"{video_id}.txt"
        output_file = self.output_dir / filename
        
        # Create header with metadata
        header = f"""# YouTube Transcript - {video_title}
# Video ID: {video_id}
# Language: {transcript_data['language']}
# Collected: {datetime.now().isoformat()}
# URL: https://youtube.com/watch?v={video_id}

"""
        
        # Write transcript to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(header)
            f.write(transcript_data['transcript'])
        
        print(f"✅ Saved transcript to {output_file}")
        return output_file
    
    def collect_transcript(self, video_id, video_title="", languages=['en', 'en-US']):
        """
        Main method to collect and save transcript for a video
        
        Args:
            video_id (str): YouTube video ID
            video_title (str): Video title for metadata
            languages (list): Preferred languages
            
        Returns:
            dict: Result with success status and file path
        """
        # Check if transcript already exists
        output_file = self.output_dir / f"{video_id}.txt"
        if output_file.exists():
            print(f"⚠️ Transcript already exists: {output_file}")
            return {
                'success': True,
                'file_path': output_file,
                'cached': True,
                'message': 'Transcript already cached'
            }
        
        # Fetch transcript
        result = self.get_video_transcript(video_id, languages)
        
        if result['success']:
            # Save to file
            file_path = self.save_transcript_to_file(video_id, result, video_title)
            
            print(f"🎉 SUCCESS: Transcript collected for {video_id}")
            print(f"📝 Language: {result['language']}")
            print(f"📄 Length: {len(result['transcript'])} characters")
            
            return {
                'success': True,
                'file_path': file_path,
                'cached': False,
                'language': result['language'],
                'length': len(result['transcript']),
                'message': 'Transcript successfully collected'
            }
        else:
            print(f"❌ FAILED: {result['error']}")
            return {
                'success': False,
                'file_path': None,
                'cached': False,
                'error': result['error'],
                'message': f'Failed to collect transcript: {result["error"]}'
            }


def main():
    """Test the transcript collector with one video from our collection"""
    try:
        collector = TranscriptCollector()
        
        # Use the first video from our Matthew Berman collection
        test_video_id = "AxdWgxINWG8"  # "ChatGPT-5: The Rubik's Cube Test"
        test_video_title = "ChatGPT-5: The Rubik's Cube Test"
        
        print(f"🚀 Testing Task 1.2: Transcript Collection")
        print(f"📺 Video ID: {test_video_id}")
        print(f"📰 Title: {test_video_title}")
        print()
        
        # Collect transcript
        result = collector.collect_transcript(test_video_id, test_video_title)
        
        if result['success']:
            print(f"\n🎉 Task 1.2 SUCCESS!")
            print(f"📁 File: {result['file_path']}")
            print(f"💾 Cached: {result['cached']}")
            if not result['cached']:
                print(f"🌍 Language: {result['language']}")
                print(f"📏 Length: {result['length']} characters")
            print(f"\n✅ Ready for Task 1.3: Video summarization & display")
        else:
            print(f"\n❌ Task 1.2 FAILED!")
            print(f"Error: {result['error']}")
            
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()
