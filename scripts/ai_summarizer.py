#!/usr/bin/env python3
"""
AI Summarizer for FocusFerry
Generates summaries of YouTube video transcripts using OpenRouter AI
"""

import os
import json
import requests
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def read_transcript(video_id):
    """Read transcript file for given video ID"""
    transcript_path = Path(__file__).parent.parent / "transcripts" / f"{video_id}.txt"
    
    if not transcript_path.exists():
        raise FileNotFoundError(f"Transcript not found: {transcript_path}")
    
    with open(transcript_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract just the transcript content (skip the header)
    lines = content.strip().split('\n')
    transcript_lines = []
    
    for line in lines:
        if line.startswith('#'):
            continue  # Skip header lines
        if line.strip():
            transcript_lines.append(line.strip())
    
    return ' '.join(transcript_lines)

def get_video_info(video_id):
    """Get video info from the unified content feed"""
    content_feed_path = Path(__file__).parent.parent / "data" / "content_feed.json"
    
    with open(content_feed_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    video_item_id = f"youtube_{video_id}"
    for item in data['items']:
        if item['id'] == video_item_id:
            return item, data, content_feed_path
    
    raise ValueError(f"Video {video_id} not found in content_feed.json")

def save_summary_to_feed(video_id, summary, content_data, content_path):
    """Save the AI summary to the unified content feed"""
    video_item_id = f"youtube_{video_id}"
    
    for item in content_data['items']:
        if item['id'] == video_item_id:
            item['content']['ai_summary'] = summary
            item['metadata']['summarized_at'] = datetime.now().isoformat()
            break
    
    # Update generation timestamp
    content_data['generated_at'] = datetime.now().isoformat()
    
    # Write back to file
    with open(content_path, 'w', encoding='utf-8') as f:
        json.dump(content_data, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Summary saved to {content_path}")

def summarize_with_openrouter(title, transcript):
    """Generate summary using OpenRouter AI (Gemini 2.5 Flash)"""
    api_key = os.getenv('OPENROUTER_API_KEY')
    
    if not api_key or api_key == 'your_openrouter_api_key_here':
        raise ValueError("OPENROUTER_API_KEY not set in .env file")
    
    prompt = f"""Je bent een tech journalist die YouTube video's samenvat voor techneuten. 

Maak een samenvatting van deze video transcript in maximaal 400 karakters. De samenvatting moet:
- Technisch accuraat zijn maar begrijpelijk voor iemand met basiskennis van AI/tech
- De kernpunten benadrukken: wat wordt gedemonstreerd en waarom dat belangrijk is
- Concrete details vermelden (bijv. "20x20x20 Rubik's cube")
- Geschreven zijn in het Nederlands
- Enthousiast maar informatief van tone zijn

Video titel: {title}
Transcript: {transcript}

Samenvatting (max 400 karakters):"""

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    data = {
        'model': 'google/gemini-2.5-flash',
        'messages': [
            {
                'role': 'user',
                'content': prompt
            }
        ],
        'max_tokens': 200,
        'temperature': 0.7
    }
    
    response = requests.post(
        'https://openrouter.ai/api/v1/chat/completions',
        headers=headers,
        json=data
    )
    
    if response.status_code != 200:
        raise Exception(f"OpenRouter API error: {response.status_code} - {response.text}")
    
    result = response.json()
    summary = result['choices'][0]['message']['content'].strip()
    
    # Remove any "Samenvatting:" prefix if AI added it
    if summary.lower().startswith('samenvatting:'):
        summary = summary[13:].strip()
    
    return summary

def main():
    """Main function to test summarization"""
    video_id = "AxdWgxINWG8"
    
    try:
        print(f"🎬 Processing video: {video_id}")
        
        # Get video info from unified feed
        video_item, content_data, content_path = get_video_info(video_id)
        print(f"📺 Title: {video_item['content']['title']}")
        
        # Check if summary already exists
        if 'ai_summary' in video_item['content']:
            print(f"ℹ️  Summary already exists: {video_item['content']['ai_summary']}")
            print("🔄 Regenerating anyway...")
        
        # Read transcript
        transcript = read_transcript(video_id)
        print(f"📄 Transcript length: {len(transcript)} characters")
        print(f"📄 First 200 chars: {transcript[:200]}...")
        
        # Generate summary
        print("\n🤖 Generating AI summary...")
        summary = summarize_with_openrouter(video_item['content']['title'], transcript)
        
        print(f"\n✅ Summary ({len(summary)} chars):")
        print(f"'{summary}'")
        
        if len(summary) > 400:
            print(f"⚠️  Warning: Summary is {len(summary)} chars (over 400 limit)")
        
        # Save to unified feed
        save_summary_to_feed(video_id, summary, content_data, content_path)
        print("\n🎉 Task 1.3 progress: AI summary generated and saved!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
