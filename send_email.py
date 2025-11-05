#!/usr/bin/env python3
"""
AI News Digest - Email Sender
Generates AI summaries and sends personalized emails to different audiences.
"""

import json
import logging
import os
import smtplib
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Dict, List, Any
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('email_sender.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configure OpenAI client
openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Email configuration
EMAIL_CONFIG = {
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "username": os.getenv('EMAIL_USERNAME'),
    "password": os.getenv('EMAIL_PASSWORD'),
    "recipients": {
        "audience_1": os.getenv('RECIPIENT_1'),
        "audience_2": os.getenv('RECIPIENT_2')
    }
}

# Audience-specific prompts
AUDIENCE_PROMPTS = {
    "audience_1": {
        "name": "Marketing & SEO Professional",
        "interests": "AI voor marketing, AI voor SEO/SEA, automatisering van processen, Google vs AI / Search updates",
        "focus": "Focus op praktische toepassingen van AI in marketing en SEO, nieuwe tools en trends die direct toepasbaar zijn."
    },
    "audience_2": {
        "name": "AI Compliance & Ethics Professional", 
        "interests": "AI-compliance, ethiek, wetgeving (zoals EU AI Act), klachtencommissies, zzp'ers en AI, transparantie en bias in AI",
        "focus": "Focus op regelgeving, ethische overwegingen, compliance-uitdagingen en maatschappelijke impact van AI."
    }
}

def get_articles_from_last_week() -> Dict[str, List[Dict[str, Any]]]:
    """Get articles from the last 7 days, organized by audience."""
    articles_by_audience = {
        "audience_1": [],
        "audience_2": []
    }
    
    # Calculate date range (last 7 days)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    
    logger.info(f"Collecting articles from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    
    # Iterate through data files
    data_dir = "data"
    if not os.path.exists(data_dir):
        logger.warning("Data directory not found")
        return articles_by_audience
    
    for filename in os.listdir(data_dir):
        if filename.endswith('.json'):
            file_date_str = filename.replace('.json', '')
            try:
                file_date = datetime.strptime(file_date_str, '%Y-%m-%d')
                
                # Check if file is within our date range
                if start_date <= file_date <= end_date:
                    file_path = os.path.join(data_dir, filename)
                    
                    with open(file_path, 'r', encoding='utf-8') as f:
                        articles = json.load(f)
                    
                    # Organize articles by audience
                    for article in articles:
                        audience = article.get('audience')
                        if audience in articles_by_audience:
                            articles_by_audience[audience].append(article)
                    
                    logger.info(f"Loaded {len(articles)} articles from {filename}")
                    
            except ValueError:
                logger.warning(f"Invalid date format in filename: {filename}")
    
    return articles_by_audience

def generate_ai_summary(articles: List[Dict[str, Any]], audience: str) -> str:
    """Generate AI summary using OpenAI GPT."""
    if not articles:
        return "Geen artikelen gevonden voor deze week."
    
    audience_info = AUDIENCE_PROMPTS[audience]
    
    # Prepare articles for the prompt
    articles_text = ""
    for i, article in enumerate(articles[:20], 1):  # Limit to 20 articles to avoid token limits
        articles_text += f"{i}. {article['title']}\n"
        articles_text += f"   Bron: {article['source']}\n"
        articles_text += f"   Samenvatting: {article['summary'][:200]}...\n\n"
    
    prompt = f"""
Je bent een AI-nieuws samenvatter die een wekelijkse digest maakt voor een {audience_info['name']}.

Interessegebieden: {audience_info['interests']}
Focus: {audience_info['focus']}

Hier zijn de artikelen van de afgelopen week:

{articles_text}

Maak een samenvatting van maximaal 250 woorden in het Nederlands met de volgende structuur:

1. **Intro** (1-2 zinnen): Wat is de algemene trend deze week?
2. **Highlights** (3-4 punten): De belangrijkste ontwikkelingen
3. **Leestip**: Het meest interessante artikel voor deze doelgroep

Schrijf in een professionele maar toegankelijke stijl. Focus op wat relevant is voor {audience_info['name']}.
"""
    
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Je bent een ervaren nieuws samenvatter die complexe AI-ontwikkelingen toegankelijk maakt voor professionals."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        summary = response.choices[0].message.content.strip()
        logger.info(f"Generated summary for {audience} ({len(summary)} characters)")
        return summary
        
    except Exception as e:
        logger.error(f"Error generating AI summary: {e}")
        return f"Er is een fout opgetreden bij het genereren van de samenvatting: {str(e)}"

def create_html_email(summary: str, audience: str, article_count: int) -> str:
    """Create HTML email template."""
    audience_info = AUDIENCE_PROMPTS[audience]
    
    html_template = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI News Digest - {audience_info['name']}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .header {{
            text-align: center;
            border-bottom: 3px solid #007bff;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        .header h1 {{
            color: #007bff;
            margin: 0;
            font-size: 28px;
        }}
        .header p {{
            color: #666;
            margin: 10px 0 0 0;
            font-size: 16px;
        }}
        .summary {{
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
            white-space: pre-line;
        }}
        .footer {{
            text-align: center;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #eee;
            color: #666;
            font-size: 14px;
        }}
        .stats {{
            background-color: #e3f2fd;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 AI News Digest</h1>
            <p>Wekelijkse samenvatting voor {audience_info['name']}</p>
            <p>{datetime.now().strftime('%d %B %Y')}</p>
        </div>
        
        <div class="stats">
            📊 Deze week {article_count} artikelen geanalyseerd
        </div>
        
        <div class="summary">
{summary}
        </div>
        
        <div class="footer">
            <p>📧 Deze e-mail wordt automatisch gegenereerd door het AI News Digest systeem</p>
            <p>🔗 Gebaseerd op {len(AUDIENCE_PROMPTS[audience].get('sources', []))} RSS-feeds</p>
        </div>
    </div>
</body>
</html>
"""
    
    return html_template

def send_email(recipient: str, subject: str, html_content: str) -> bool:
    """Send email via SMTP."""
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = EMAIL_CONFIG['username']
        msg['To'] = recipient
        
        # Attach HTML content
        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)
        
        # Send email
        with smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port']) as server:
            server.starttls()
            server.login(EMAIL_CONFIG['username'], EMAIL_CONFIG['password'])
            server.send_message(msg)
        
        logger.info(f"Email sent successfully to {recipient}")
        return True
        
    except Exception as e:
        logger.error(f"Error sending email to {recipient}: {e}")
        return False

def main():
    """Main email sending function."""
    logger.info("Starting AI News Digest email sender")
    
    # Check required environment variables
    required_vars = ['OPENAI_API_KEY', 'EMAIL_USERNAME', 'EMAIL_PASSWORD', 'RECIPIENT_1']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        logger.error(f"Missing required environment variables: {missing_vars}")
        return
    
    # Only process audiences that have recipients configured
    audiences_to_process = []
    if os.getenv('RECIPIENT_1'):
        audiences_to_process.append('audience_1')
    if os.getenv('RECIPIENT_2'):
        audiences_to_process.append('audience_2')
    
    if not audiences_to_process:
        logger.error("No recipients configured. Please set RECIPIENT_1 or RECIPIENT_2")
        return
    
    # Get articles from last week
    articles_by_audience = get_articles_from_last_week()
    
    # Process each audience that has a recipient
    for audience in audiences_to_process:
        articles = articles_by_audience.get(audience, [])
        if not articles:
            logger.warning(f"No articles found for {audience}")
            continue
        
        audience_info = AUDIENCE_PROMPTS[audience]
        recipient = EMAIL_CONFIG['recipients'][audience]
        
        if not recipient:
            logger.warning(f"No recipient configured for {audience}")
            continue
        
        logger.info(f"Processing {len(articles)} articles for {audience}")
        
        # Generate AI summary
        summary = generate_ai_summary(articles, audience)
        
        # Create HTML email
        html_content = create_html_email(summary, audience, len(articles))
        
        # Send email
        subject = f"🤖 AI News Digest - {audience_info['name']} - {datetime.now().strftime('%d %B %Y')}"
        success = send_email(recipient, subject, html_content)
        
        if success:
            logger.info(f"Successfully sent digest to {audience}")
        else:
            logger.error(f"Failed to send digest to {audience}")
    
    logger.info("Email sending completed")

if __name__ == "__main__":
    main() 