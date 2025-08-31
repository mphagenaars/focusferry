#!/usr/bin/env python3
"""
Content Summarizer for FocusFerry
Task 2.2: Generate AI summaries for articles using OpenRouter AI
"""

import os
import json
import requests
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def summarize_with_openrouter(title, description):
    """Generate summary using OpenRouter AI (Gemini 2.5 Flash)"""
    api_key = os.getenv('OPENROUTER_API_KEY')
    
    if not api_key or api_key == 'your_openrouter_api_key_here':
        raise ValueError("OPENROUTER_API_KEY not set in .env file")
    
    prompt = f"""Je bent een tech journalist die nieuwsartikelen samenvat voor techneuten. 

Maak een samenvatting van dit artikel in maximaal 400 karakters. De samenvatting moet:
- Technisch accuraat zijn maar begrijpelijk voor iemand met basiskennis van AI/tech
- De kernpunten benadrukken: wat wordt aangekondigd en waarom dat belangrijk is
- Concrete details vermelden (bijv. "50 miljoen dollar", "Model Spec")
- Geschreven zijn in het Nederlands
- Enthousiast maar informatief van tone zijn

Artikel titel: {title}
Artikel beschrijving: {description}

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

def get_content_feed():
    """Load the unified content feed"""
    content_feed_path = Path(__file__).parent.parent / "data" / "content_feed.json"
    
    with open(content_feed_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    return data, content_feed_path

def save_content_feed(data, content_path):
    """Save the updated content feed"""
    data['generated_at'] = datetime.now().isoformat()
    
    with open(content_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Updated content feed: {content_path}")

def summarize_rss_articles():
    """Add AI summaries to RSS articles in the content feed"""
    
    # Load content feed
    content_data, content_path = get_content_feed()
    
    # Find RSS articles without summaries
    rss_articles = []
    for item in content_data['items']:
        if (item['source']['platform'] == 'rss' and 
            'ai_summary' not in item['content']):
            rss_articles.append(item)
    
    if not rss_articles:
        print("ℹ️  All RSS articles already have AI summaries")
        return True
    
    print(f"🤖 Found {len(rss_articles)} RSS articles to summarize")
    
    # Summarize each article
    summarized_count = 0
    for article in rss_articles:
        try:
            print(f"\n📰 Processing: {article['content']['title']}")
            
            # Generate summary
            summary = summarize_with_openrouter(
                article['content']['title'],
                article['content']['description']
            )
            
            print(f"✅ Summary ({len(summary)} chars): {summary}")
            
            if len(summary) > 400:
                print(f"⚠️  Warning: Summary is {len(summary)} chars (over 400 limit)")
            
            # Add summary to article
            article['content']['ai_summary'] = summary
            article['metadata']['summarized_at'] = datetime.now().isoformat()
            
            summarized_count += 1
            
        except Exception as e:
            print(f"❌ Error summarizing article '{article['content']['title']}': {e}")
            continue
    
    if summarized_count > 0:
        # Save updated content feed
        save_content_feed(content_data, content_path)
        
        print(f"\n🎉 Task 2.2 SUCCESS!")
        print(f"📊 Summarized {summarized_count} RSS articles")
        print(f"💾 Content feed updated with AI summaries")
    else:
        print(f"\n❌ Task 2.2 FAILED!")
        print("No articles were successfully summarized")
    
    return summarized_count > 0

def main():
    """Main function to test RSS article summarization"""
    print("🤖 Task 2.2: RSS Article Summarization")
    print("🎯 Adding AI summaries to RSS articles")
    print()
    
    try:
        success = summarize_rss_articles()
        
        if success:
            print(f"\n✅ Task 2.2 completed successfully!")
            print(f"🔄 Next: Hugo build & deploy to see summaries on site")
        else:
            print(f"\n❌ Task 2.2 failed!")
            
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
