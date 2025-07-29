# 🚀 Setup Guide - AI News Digest

## Snelle Start

### 1. GitHub Repository Aanmaken

1. Ga naar [GitHub](https://github.com) en maak een nieuwe repository aan
2. Naam: `ai-news-digest`
3. Maak de repository **public** (voor gratis GitHub Actions)
4. Upload alle bestanden uit deze directory

### 2. Dependencies Installeren

```bash
pip install -r requirements.txt
```

### 3. Environment Variables Instellen

Kopieer `.env.example` naar `.env` en vul in:

```bash
cp .env.example .env
```

**Vereiste waarden:**
- `OPENAI_API_KEY`: Haal op van [OpenAI Platform](https://platform.openai.com/api-keys)
- `EMAIL_USERNAME`: Je Gmail adres
- `EMAIL_PASSWORD`: Gmail app password (zie instructies hieronder)
- `RECIPIENT_1`: Jouw e-mailadres
- `RECIPIENT_2`: E-mailadres van je vriendin

### 4. Gmail App Password Instellen

**Stap 1: 2FA Inschakelen**
1. Ga naar [Google Account](https://myaccount.google.com/)
2. Security → 2-Step Verification → Turn On

**Stap 2: App Password Genereren**
1. Security → 2-Step Verification → App passwords
2. Select "Mail" en "Other (Custom name)"
3. Naam: "AI News Digest"
4. Kopieer het gegenereerde wachtwoord (16 karakters)

### 5. GitHub Secrets Configureren

1. Ga naar je repository → Settings → Secrets and variables → Actions
2. Klik "New repository secret"
3. Voeg toe:
   - `OPENAI_API_KEY`
   - `EMAIL_USERNAME`
   - `EMAIL_PASSWORD`
   - `RECIPIENT_1`
   - `RECIPIENT_2`

### 6. Lokaal Testen

```bash
python test_local.py
```

Dit script controleert:
- ✅ Environment variables
- ✅ RSS scraping functionaliteit
- ✅ E-mail verzending
- ✅ Data bestanden

### 7. GitHub Actions Activeren

De workflows zijn automatisch actief zodra je de repository hebt aangemaakt:

- **Daily Scraping**: Dagelijks om 07:00 UTC
- **Weekly Email**: Elke maandag om 08:00 UTC

Je kunt ze ook handmatig triggeren via de "Actions" tab.

## 🔧 Troubleshooting

### Veelvoorkomende Problemen

**1. "ModuleNotFoundError: No module named 'dotenv'"**
```bash
pip install python-dotenv
```

**2. Gmail Authentication Error**
- Controleer of je app password correct is
- Zorg dat 2FA is ingeschakeld
- Test met een andere e-mail provider als alternatief

**3. OpenAI API Error**
- Controleer of je API key geldig is
- Zorg dat je voldoende credits hebt
- Test de key op [OpenAI Platform](https://platform.openai.com/)

**4. RSS Feed Errors**
- Sommige feeds kunnen tijdelijk offline zijn
- Controleer de logs in de repository
- Voeg alternatieve feeds toe indien nodig

### Logs Bekijken

- **Lokaal**: `scraper.log` en `email_sender.log`
- **GitHub Actions**: Actions tab → klik op workflow run → logs

## 📊 Monitoring

### GitHub Actions Status
- Ga naar Actions tab in je repository
- Groene vinkjes = alles werkt
- Rode kruizen = er is een probleem

### E-mail Ontvangst
- Controleer je inbox elke maandag
- Check spam folder als je geen e-mails ontvangt
- Test handmatig via Actions tab

## 🔄 Onderhoud

### RSS Feeds Bijwerken
Bewerk `scrape.py` en voeg nieuwe feeds toe:

```python
RSS_FEEDS = {
    "audience_1": [
        # Bestaande feeds...
        {
            "name": "Nieuwe Feed",
            "url": "https://example.com/rss",
            "audience": "audience_1"
        }
    ]
}
```

### E-mail Templates Aanpassen
Bewerk `send_email.py` om de e-mail styling aan te passen.

### Scheduling Wijzigen
Bewerk de cron expressies in `.github/workflows/`:
- `scrape.yml`: `'0 7 * * *'` (dagelijks 07:00 UTC)
- `mail.yml`: `'0 8 * * 1'` (maandag 08:00 UTC)

## 💡 Tips

1. **Test eerst lokaal** voordat je naar GitHub pusht
2. **Monitor de logs** regelmatig voor problemen
3. **Backup je data** door de repository te clonen
4. **Update dependencies** regelmatig voor security patches
5. **Controleer RSS feeds** maandelijks op beschikbaarheid

## 🆘 Support

Als je problemen ondervindt:
1. Check de logs eerst
2. Test lokaal met `python test_local.py`
3. Controleer GitHub Actions status
4. Open een issue in de repository

---

**Succes met je AI News Digest systeem! 🎉** 