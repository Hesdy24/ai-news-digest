# 🤖 AI News Digest

Een volledig automatisch AI-nieuws samenvattingssysteem dat dagelijks RSS-feeds verzamelt en wekelijks gepersonaliseerde samenvattingen verstuurt via e-mail.

## 🎯 Doel

Dit systeem:
- **Dagelijks** AI-gerelateerd nieuws verzamelt via RSS-feeds
- De ruwe data opslaat in gestructureerde JSON-bestanden
- **Wekelijks** (elke maandag) de afgelopen 7 dagen samenvat via OpenAI GPT
- Gepersonaliseerde e-mails verstuurt naar twee verschillende doelgroepen
- Alles draait via GitHub Actions, zodat je computer niet aan hoeft te blijven

## 👥 Doelgroepen

### Doelgroep 1: Marketing & SEO Professional
**Interessegebieden:**
- AI voor marketing
- AI voor SEO/SEA
- Automatisering van processen
- Google vs AI / Search updates

**RSS-feeds:**
- Ben's Bites
- The Rundown AI
- Marketing AI Institute
- Search Engine Journal
- Google AI Blog

### Doelgroep 2: AI Compliance & Ethics Professional
**Interessegebieden:**
- AI-compliance
- Ethiek, wetgeving (zoals EU AI Act)
- Klachtencommissies, zzp'ers en AI
- Transparantie en bias in AI

**RSS-feeds:**
- MIT Technology Review
- AI Policy Exchange
- Future of Privacy Forum
- AI Ethics Journal
- TechCrunch Privacy

## 🚀 Setup

### 1. Repository Clonen
```bash
git clone https://github.com/yourusername/ai-news-digest.git
cd ai-news-digest
```

### 2. Dependencies Installeren
```bash
pip install -r requirements.txt
```

### 3. Environment Variables Configureren

Kopieer `.env.example` naar `.env` en vul de waarden in:

```bash
cp .env.example .env
```

**Vereiste variabelen:**
- `OPENAI_API_KEY`: Je OpenAI API key
- `EMAIL_USERNAME`: Je Gmail adres
- `EMAIL_PASSWORD`: Je Gmail app password (niet je normale wachtwoord!)
- `RECIPIENT_1`: E-mailadres voor doelgroep 1
- `RECIPIENT_2`: E-mailadres voor doelgroep 2

### 4. Gmail App Password Instellen

Voor Gmail moet je een app password instellen:

1. Ga naar [Google Account Settings](https://myaccount.google.com/)
2. Ga naar "Security" → "2-Step Verification"
3. Scroll naar beneden naar "App passwords"
4. Genereer een nieuwe app password voor "Mail"
5. Gebruik dit wachtwoord in `EMAIL_PASSWORD`

### 5. GitHub Secrets Configureren

Ga naar je GitHub repository → Settings → Secrets and variables → Actions:

Voeg de volgende secrets toe:
- `OPENAI_API_KEY`
- `EMAIL_USERNAME`
- `EMAIL_PASSWORD`
- `RECIPIENT_1`
- `RECIPIENT_2`

## 🔧 GitHub Actions Workflows

### Daily Scraping (`scrape.yml`)
- **Schema:** Dagelijks om 07:00 UTC
- **Functie:** Verzamelt nieuws van alle RSS-feeds
- **Output:** JSON-bestanden in `data/` directory

### Weekly Email (`mail.yml`)
- **Schema:** Elke maandag om 08:00 UTC
- **Functie:** Genereert AI-samenvattingen en verstuurt e-mails
- **Output:** Gepersonaliseerde HTML e-mails

## 🧪 Lokaal Testen

### RSS Scraping Testen
```bash
python scrape.py
```

Dit zal:
- Alle RSS-feeds uitlezen
- Artikelen opslaan in `data/YYYY-MM-DD.json`
- Logs schrijven naar `scraper.log`

### E-mail Testen
```bash
python send_email.py
```

Dit zal:
- Artikelen van de afgelopen 7 dagen verzamelen
- AI-samenvattingen genereren
- E-mails versturen naar beide doelgroepen
- Logs schrijven naar `email_sender.log`

## 📁 Projectstructuur

```
ai-news-digest/
├── .github/
│   └── workflows/
│       ├── scrape.yml      # Dagelijkse RSS scraping
│       └── mail.yml        # Wekelijkse e-mail digest
├── data/                   # JSON bestanden met artikelen
├── scrape.py              # RSS scraping script
├── send_email.py          # E-mail generatie en verzending
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
└── README.md             # Deze file
```

## 🔄 Nieuwe RSS-feeds Toevoegen

Om nieuwe RSS-feeds toe te voegen, bewerk `scrape.py`:

1. Zoek de `RSS_FEEDS` dictionary
2. Voeg je feed toe aan de juiste doelgroep:

```python
RSS_FEEDS = {
    "audience_1": [
        # Bestaande feeds...
        {
            "name": "Nieuwe Feed",
            "url": "https://example.com/rss",
            "audience": "audience_1"
        }
    ],
    "audience_2": [
        # Bestaande feeds...
    ]
}
```

## 📊 Data Format

Artikelen worden opgeslagen in JSON formaat:

```json
{
  "title": "Artikel titel",
  "summary": "Artikel samenvatting...",
  "link": "https://example.com/article",
  "source": "Feed naam",
  "audience": "audience_1",
  "timestamp": "2024-01-15T10:30:00"
}
```

## 🐛 Troubleshooting

### Veelvoorkomende Problemen

1. **Gmail Authentication Error**
   - Zorg dat je een app password gebruikt, niet je normale wachtwoord
   - Controleer of 2FA is ingeschakeld

2. **OpenAI API Error**
   - Controleer of je API key geldig is
   - Zorg dat je voldoende credits hebt

3. **RSS Feed Errors**
   - Controleer of de RSS URL's nog werken
   - Sommige feeds kunnen tijdelijk offline zijn

### Logs Bekijken

- `scraper.log`: RSS scraping logs
- `email_sender.log`: E-mail verzending logs

## 🔒 Privacy & Security

- Alle API keys worden opgeslagen als GitHub Secrets
- E-mailadressen worden alleen gebruikt voor het versturen van digests
- Geen persoonlijke data wordt opgeslagen of gedeeld

## 📝 Licentie

MIT License - zie LICENSE file voor details.

## 🤝 Bijdragen

Pull requests zijn welkom! Voor grote wijzigingen, open eerst een issue om te bespreken wat je wilt veranderen.

## 📞 Support

Als je problemen ondervindt:
1. Check de logs in de repository
2. Controleer of alle environment variables correct zijn ingesteld
3. Open een GitHub issue met details over het probleem 