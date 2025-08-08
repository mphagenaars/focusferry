# ⚡ Quick YouTube API Setup

## Snelle stappen voor API key:

1. **Google Cloud Console**: https://console.cloud.google.com/
2. **Nieuw Project**: "FocusFerry" (of bestaand project)
3. **APIs & Services** → **Library** → Zoek "YouTube Data API v3" → **Enable**
4. **Credentials** → **Create Credentials** → **API Key**
5. **Kopieer de key** en plak in `.env`:

```bash
# In .env file:
YOUTUBE_API_KEY=AIzaSyYourRealKeyHere123456789
```

## Testen:

```bash
cd /home/matthijs/focusferry
.venv/bin/python scripts/youtube_collector.py
```

## Verwacht resultaat:

```
🔍 Fetching videos from channel: Fireship
📺 Channel ID: UCsBjURrPoezykLs9EqgamOA
✅ Saved 10 videos to /home/matthijs/focusferry/data/youtube/Fireship_videos.json

🎉 Task 1.1 SUCCESS!
Generated: /home/matthijs/focusferry/data/youtube/Fireship_videos.json
Next: Task 1.2 - Transcript collection
```

**API Quotas**: YouTube API heeft 10.000 gratis calls per dag - meer dan genoeg voor ons gebruik.
