# 🚢 FocusFerry

**We ship the news, you keep your focus!**

Een geavanceerde, AI-gedreven nieuwsaggregatie service die automatisch tech-content van RSS feeds en YouTube verzamelt, in het Nederlands samenvat, en als blazendsnelle statische website publiceert.

🌐 **Live site**: https://hgnrs.nl

## 🎯 Mission

Elke dag worden er honderden AI/tech artikelen en video's gepubliceerd. FocusFerry filtert de ruis weg en biedt je 's avonds een curated overzicht van wat er echt toe doet - in het Nederlands, met korte samenvattingen, zodat je gefocust kunt blijven op wat belangrijk is.

## ✨ Features

- 🤖 **AI-Powered**: Nederlandse samenvattingen en titel vertalingen via OpenRouter (Gemini 2.5 Flash)
- ⚡ **Blazing Fast**: Statische site (<100ms load time), lazy loading, geoptimaliseerde assets
- 🔄 **Automated**: Configuration-driven content collection, smart duplicate detection
- 📱 **Responsive**: Perfect op desktop, tablet en mobile
- 🎨 **Clean Design**: Focus op content, geen afleiding
- 🔧 **Modular**: Easy toevoegen/verwijderen van content bronnen

## 🚀 Quick Start

### Lokale Development
```bash
git clone https://github.com/mphagenaars/focusferry.git
cd focusferry

# Installeer Hugo (als nog niet aanwezig)
# https://gohugo.io/installation/

# Start lokale server
hugo serve --bind=0.0.0.0 --port=1313
# Browse naar http://localhost:1313
```

### Content Collection (Optioneel)
```bash
# Setup Python environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
pip install -r requirements.txt

# Configure API keys (.env bestand)
cp .env.example .env
# Edit .env met jouw API keys

# Run content collection
python scripts/unified_collector.py
```

### Production Deployment
```bash
# Configure deployment
cp .env.example .env
# Edit .env met server credentials

# Deploy
./deploy.sh
```

## 🏗️ Pipeline Architectuur

### Overzicht
```
🎯 UNIFIED COLLECTOR (Entry Point)
├── � RSS COLLECTION
│   ├── OpenAI News Feed
│   ├── Google DeepMind Blog  
│   └── Ars Technica Tech Lab
├── 📺 YOUTUBE COLLECTION
│   ├── Matthew Berman (AI nieuws)
│   ├── Matt Wolfe (AI tools)
│   └── Two Minute Papers (AI research)
├── 🔄 CONTENT INTEGRATION
│   └── Unified JSON feed
├── 🤖 AI PROCESSING
│   ├── Nederlandse samenvattingen (≤400 chars)
│   └── Nederlandse titel vertalingen
└── 🌐 STATIC SITE GENERATION
    ├── Hugo build (minified)
    └── Deploy naar productie
```

### Execution Flow

**⚡ Performance**: Complete pipeline in ~1.6 seconden

1. **Content Collection** (parallel processing)
   - RSS feeds: 3 bronnen → 30 artikelen
   - YouTube channels: 3 kanalen → 30 videos
   - Smart duplicate detection

2. **AI Processing** (alleen nieuwe content)
   - Nederlandse titel vertaling (behoud technische impact)
   - Nederlandse samenvattingen (≤400 karakters, enthousiast maar informatief)
   - OpenRouter API (Gemini 2.5 Flash model)

3. **Static Site Generation**
   - Hugo template rendering met fallback logic
   - CSS minification & optimization
   - Responsive design, lazy loading

4. **Production Deployment**
   - rsync naar productie server
   - Incremental updates (alleen changed files)
   - Live binnen seconden

### Configuration-Driven Design

Alle content bronnen worden gedefinieerd in `config/default.yaml`:

```yaml
content_sources:
  rss_feeds:
    - name: "OpenAI"
      url: "https://openai.com/news/rss.xml"
      enabled: true
      max_articles: 10
    # ... meer feeds
  youtube_channels:
    - name: "Matthew Berman"
      identifier: "matthew_berman"
      enabled: true
      max_videos: 10
    # ... meer kanalen
```

## 🔧 Technical Stack

- **Static Site Generator**: Hugo (v0.123+)
- **Hosting**: bHosted.nl met LiteSpeed
- **AI Processing**: OpenRouter.ai (Gemini 2.5 Flash)
- **APIs**: YouTube Data API v3, RSS/XML parsing
- **Languages**: Python 3.8+, HTML/CSS, Bash
- **Deployment**: rsync over SSH
- **Version Control**: Git + GitHub

## 📂 Project Structure

```
focusferry/
├── config/
│   └── default.yaml          # Content sources configuratie
├── scripts/
│   ├── unified_collector.py  # Main orchestrator
│   ├── config_loader.py      # YAML configuration
│   ├── rss_collector.py      # RSS parsing toolkit
│   ├── youtube_collector.py  # YouTube API toolkit
│   ├── content_integrator.py # Content merging
│   └── content_summarizer.py # AI processing
├── data/
│   ├── content_feed.json     # Unified content feed
│   ├── rss/                  # RSS artikel cache
│   └── youtube/              # YouTube video cache
├── layouts/
│   └── index.html           # Hugo template
├── static/                  # Static assets
├── public/                  # Generated site
├── deploy.sh               # Deployment script
└── hugo.toml              # Hugo configuration
```

## 🚀 Development Workflow

### Daily Content Update
```bash
# Complete pipeline (automatisch of handmatig)
python scripts/unified_collector.py  # ~1.6s
hugo --minify                        # ~20ms  
./deploy.sh                         # ~2s
# Result: Fresh Nederlandse content live!
```

### Adding New Content Sources

**RSS Feed toevoegen:**
```yaml
# In config/default.yaml
rss_feeds:
  - name: "TechCrunch AI"
    url: "https://techcrunch.com/category/artificial-intelligence/feed/"
    enabled: true
    max_articles: 15
```

**YouTube kanaal toevoegen:**
```yaml
# In config/default.yaml  
youtube_channels:
  - name: "Lex Fridman"
    identifier: "lexfridman"
    enabled: true
    max_videos: 5
```

### Micro-Task Philosophy

Dit project volgt een **micro-task benadering**:
- Elke feature is ~1.5 uur werk
- Onafhankelijk deploybaar
- Incrementele verbetering
- Zie [status.md](status.md) voor voortgang

## 📊 Current Status

**✅ COMPLETED** (Basic Infrastructure + Content Pipeline):
- Infrastructure Setup (Tasks 0.1-0.2)
- Video Pipeline (Tasks 1.1-1.5) 
- Article Pipeline (Tasks 2.1-2.4)
- **Nederlandse titels + samenvattingen**
- **Configuration-driven architectuur**

**⏳ TODO** (Enhancement & Automation):
- Enhancement Layer (Tasks 3.1-3.2)
- Configuration API (Tasks 4.1-4.8)
- Automation & Cron (Tasks 5.1-5.4)
- Search Features (Tasks 6.1-6.2)

Zie [status.md](status.md) voor gedetailleerde voortgang en [plan.md](plan.md) voor complete roadmap.

## 🌟 Live Example

**Huidige content op** https://hgnrs.nl:
- 📰 **30 RSS artikelen** van OpenAI, Google DeepMind, Ars Technica
- 📺 **6 YouTube videos** van AI experts (Matthew Berman, Matt Wolfe, Two Minute Papers)
- 🔤 **Nederlandse titels** en samenvattingen voor alle content
- ⚡ **Sub-second loading** met lazy-loaded thumbnails

## 🤝 Contributing

1. Check [status.md](status.md) voor beschikbare tasks
2. Pick een task met status ⏳ TODO  
3. Follow micro-task approach (~1.5 uur, deploybaar)
4. Test lokaal, commit, deploy
5. Update status naar ✅ DONE

## 📝 Development Guidelines

- **KISS**: Simplest working solution first
- **DRY**: Reuse existing functions 
- **Modular**: Each collector should be replaceable
- **Config-driven**: No hardcoded sources
- **Performance**: <100ms page load target

## 🚨 Error Handling

De pipeline is robuust gebouwd:
- **Graceful failures**: Eén bron falen = andere bronnen blijven werken
- **Smart retries**: Exponential backoff voor API calls
- **Detailed logging**: Colored output voor debugging
- **Fallback content**: Site blijft altijd beschikbaar

## 📈 Performance Stats

- **Pipeline execution**: ~1.6 seconden totaal
- **Site build time**: ~20ms (Hugo)
- **Page load time**: <100ms (static + CDN)
- **Success rate**: 100% (6/6 bronnen)
- **Content freshness**: Dagelijks bijgewerkt

## 🔐 Security & Privacy

- **Static site**: Geen database of server-side code = minimale attack surface
- **API keys**: Via environment variables, niet in git
- **Fair use**: Alleen korte samenvattingen + source links
- **No tracking**: Privacy-respecterende implementatie

## 📜 License

MIT License - zie [LICENSE](LICENSE) voor details.

---

**Last updated**: August 31, 2025  
**Current version**: v2.4 (Nederlandse titels + unified configuration)  
**Live site**: https://hgnrs.nl  
**Repository**: https://github.com/mphagenaars/focusferry
