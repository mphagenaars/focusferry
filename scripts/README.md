# YouTube API Setup Guide

## Task 1.1: YouTube Video Collection

Dit script haalt video-metadata op van YouTube kanalen via de YouTube Data API v3.

## Setup Stappen

### 1. YouTube API Key verkrijgen

1. Ga naar de [Google Cloud Console](https://console.cloud.google.com/)
2. Maak een nieuw project of selecteer een bestaand project
3. Ga naar "APIs & Services" > "Library"
4. Zoek naar "YouTube Data API v3" en enable deze
5. Ga naar "APIs & Services" > "Credentials"
6. Klik "Create Credentials" > "API Key"
7. Kopieer de API key

### 2. API Key configureren

1. Open het `.env` bestand in de root van het project
2. Vervang `your_youtube_api_key_here` met je echte API key:
   ```
   YOUTUBE_API_KEY=AIzaSyYourActualAPIKeyHere
   ```

### 3. Script uitvoeren

```bash
# Vanuit de focusferry directory:
.venv/bin/python scripts/youtube_collector.py
```

## Wat het script doet

- Haalt de laatste 10 video's op van het Matthew Berman YouTube kanaal (AI content)
- Slaat video-metadata op in `data/youtube/matthew_berman_videos.json`
- Elke video bevat:
  - video_id
  - title
  - description (eerste 200 karakters)
  - published_at
  - channel_title
  - channel_id
  - thumbnail_url
  - collected_at

## Success Criteria Task 1.1

✅ JSON-bestand met minimaal 10 recente video's van één kanaal  
✅ Elk item bevat: video-ID, titel, publicatiedatum, kanaal-naam  
✅ Script kan herhaald worden zonder fouten  

## Volgende stap

Task 1.2: Transcript ophalen van individuele video's
