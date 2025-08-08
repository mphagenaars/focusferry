# 🚢 FocusFerry

**We ship the news, you keep your focus!**

Een automatische nieuwsaggregatie service die tech-content van RSS feeds en YouTube verzamelt, met AI samenvat, en als statische website publiceert.

## 🎯 Doel

's Avonds in één oogopslag alle relevante tech-artikelen en video's zien, zonder handmatig door fragmentated bronnen te hoeven scannen.

## 🚀 Quick Start

```bash
# Clone en setup
git clone <repository-url>
cd focusferry

# Lokale development
hugo serve --bind=0.0.0.0 --port=1313
# Browse naar http://localhost:1313

# Deployment naar productie
cp .env.example .env
# Edit .env met jouw server credentials
./deploy.sh
```

## 📊 Development Status

**✅ Voltooid:**
- 0.1 Hello-World deploy - Site live op https://hgnrs.nl

**🔄 Aan de slag:**
- 0.2 GitHub repo + CI/CD

**⏳ Todo:**
- YouTube API integratie
- RSS feed parsing  
- AI summarization
- En meer...

Zie [plan.md](plan.md) voor complete roadmap en micro-tasks.

## 🏗️ Architectuur

- **Frontend**: Hugo static site generator
- **Hosting**: bHosted.nl met LiteSpeed
- **Deployment**: rsync via SSH
- **AI**: OpenRouter.ai voor filtering en samenvattingen
- **Content**: RSS feeds + YouTube transcripts

## 📝 Development

Dit project volgt een **micro-task benadering** - elke feature is ~1.5 uur werk en onafhankelijk deploybaar.

Voor details zie:
- [plan.md](plan.md) - Volledige project plan en backlog
- [.github/instructions/](https://github.com/your-repo/tree/main/.github/instructions) - Coding guidelines

## 🤝 Contributing

1. Check [plan.md](plan.md) voor beschikbare micro-tasks
2. Pick een task met status ⏳ TODO
3. Work volgens de micro-task filosofie
4. Update status naar ✅ DONE bij completion

---

**Last updated**: August 8, 2025  
**Current milestone**: Basic infrastructure (Tasks 0.x)
