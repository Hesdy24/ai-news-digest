#!/usr/bin/env python3
"""
AI News Digest - Monitoring System
Tracks daily system health and sends status reports.
"""

import json
import logging
import os
import smtplib
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Dict, List, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('monitor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Email configuration
EMAIL_CONFIG = {
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "username": os.getenv('EMAIL_USERNAME'),
    "password": os.getenv('EMAIL_PASSWORD'),
    "admin_email": os.getenv('RECIPIENT_1')  # Send reports to admin
}

def check_data_files() -> Dict[str, Any]:
    """Check if data files are being created daily."""
    data_dir = "data"
    if not os.path.exists(data_dir):
        return {"status": "error", "message": "Data directory not found"}
    
    # Check last 7 days
    today = datetime.now()
    missing_days = []
    total_articles = 0
    
    for i in range(7):
        check_date = today - timedelta(days=i)
        filename = f"{check_date.strftime('%Y-%m-%d')}.json"
        filepath = os.path.join(data_dir, filename)
        
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    articles = json.load(f)
                total_articles += len(articles)
            except Exception as e:
                logger.error(f"Error reading {filename}: {e}")
        else:
            missing_days.append(check_date.strftime('%Y-%m-%d'))
    
    return {
        "status": "warning" if missing_days else "ok",
        "total_articles": total_articles,
        "missing_days": missing_days,
        "data_files_checked": 7
    }

def check_log_files() -> Dict[str, Any]:
    """Check log files for errors."""
    log_files = ['scraper.log', 'email_sender.log', 'monitor.log']
    log_status = {}
    
    for log_file in log_files:
        if os.path.exists(log_file):
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                # Check last 24 hours
                recent_lines = []
                yesterday = datetime.now() - timedelta(days=1)
                
                for line in lines:
                    try:
                        # Extract timestamp from log line
                        timestamp_str = line.split(' - ')[0]
                        timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S,%f')
                        if timestamp >= yesterday:
                            recent_lines.append(line)
                    except:
                        continue
                
                # Count errors
                error_count = sum(1 for line in recent_lines if 'ERROR' in line)
                warning_count = sum(1 for line in recent_lines if 'WARNING' in line)
                
                log_status[log_file] = {
                    "status": "error" if error_count > 0 else "warning" if warning_count > 0 else "ok",
                    "error_count": error_count,
                    "warning_count": warning_count,
                    "total_lines": len(recent_lines)
                }
            except Exception as e:
                log_status[log_file] = {"status": "error", "message": str(e)}
        else:
            log_status[log_file] = {"status": "warning", "message": "Log file not found"}
    
    return log_status

def check_environment() -> Dict[str, Any]:
    """Check if all required environment variables are set."""
    required_vars = ['OPENAI_API_KEY', 'EMAIL_USERNAME', 'EMAIL_PASSWORD', 'RECIPIENT_1', 'RECIPIENT_2']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    return {
        "status": "error" if missing_vars else "ok",
        "missing_variables": missing_vars,
        "total_variables": len(required_vars)
    }

def generate_status_report() -> str:
    """Generate a comprehensive status report."""
    logger.info("Generating daily status report")
    
    # Run all checks
    data_status = check_data_files()
    log_status = check_log_files()
    env_status = check_environment()
    
    # Determine overall status
    overall_status = "ok"
    if any(check["status"] == "error" for check in [data_status, env_status]) or \
       any(log["status"] == "error" for log in log_status.values()):
        overall_status = "error"
    elif any(check["status"] == "warning" for check in [data_status, env_status]) or \
         any(log["status"] == "warning" for log in log_status.values()):
        overall_status = "warning"
    
    # Generate report
    report = f"""
🤖 AI News Digest - Dagelijkse Status Rapport
============================================
📅 Datum: {datetime.now().strftime('%d %B %Y')}
🕐 Tijd: {datetime.now().strftime('%H:%M:%S')}
📊 Algemene Status: {overall_status.upper()}

📁 DATA BESTANDEN:
  Status: {data_status['status'].upper()}
  Totaal artikelen (7 dagen): {data_status['total_articles']}
  Ontbrekende dagen: {', '.join(data_status['missing_days']) if data_status['missing_days'] else 'Geen'}

🔍 LOG BESTANDEN:
"""
    
    for log_file, status in log_status.items():
        report += f"  {log_file}:\n"
        report += f"    Status: {status['status'].upper()}\n"
        if 'error_count' in status:
            report += f"    Fouten: {status['error_count']}\n"
            report += f"    Waarschuwingen: {status['warning_count']}\n"
        if 'message' in status:
            report += f"    Bericht: {status['message']}\n"
    
    report += f"""
⚙️ OMGEVING:
  Status: {env_status['status'].upper()}
  Ontbrekende variabelen: {', '.join(env_status['missing_variables']) if env_status['missing_variables'] else 'Geen'}

💡 AANBEVELINGEN:
"""
    
    if overall_status == "error":
        report += "  ⚠️ Er zijn kritieke problemen die direct aandacht nodig hebben!\n"
    elif overall_status == "warning":
        report += "  ⚠️ Er zijn waarschuwingen die aandacht verdienen.\n"
    else:
        report += "  ✅ Alles werkt naar behoren!\n"
    
    if data_status['missing_days']:
        report += f"  📅 Ontbrekende data voor: {', '.join(data_status['missing_days'])}\n"
    
    if any(log['error_count'] > 0 for log in log_status.values() if 'error_count' in log):
        report += "  🔍 Controleer de log bestanden voor fouten.\n"
    
    report += "\n📧 Dit rapport wordt automatisch gegenereerd door het AI News Digest monitoring systeem."
    
    return report

def send_status_report(report: str) -> bool:
    """Send status report via email."""
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"🤖 AI News Digest - Dagelijkse Status - {datetime.now().strftime('%d %B %Y')}"
        msg['From'] = EMAIL_CONFIG['username']
        msg['To'] = EMAIL_CONFIG['admin_email']
        
        # Create HTML version
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background-color: #007bff; color: white; padding: 20px; text-align: center; }}
        .content {{ background-color: #f8f9fa; padding: 20px; white-space: pre-line; }}
        .footer {{ text-align: center; margin-top: 20px; color: #666; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 AI News Digest - Dagelijkse Status</h1>
        </div>
        <div class="content">
{report}
        </div>
        <div class="footer">
            <p>📧 Automatisch gegenereerd op {datetime.now().strftime('%d %B %Y om %H:%M:%S')}</p>
        </div>
    </div>
</body>
</html>
"""
        
        # Attach HTML content
        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)
        
        # Send email
        with smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port']) as server:
            server.starttls()
            server.login(EMAIL_CONFIG['username'], EMAIL_CONFIG['password'])
            server.send_message(msg)
        
        logger.info(f"Status report sent successfully to {EMAIL_CONFIG['admin_email']}")
        return True
        
    except Exception as e:
        logger.error(f"Error sending status report: {e}")
        return False

def main():
    """Main monitoring function."""
    logger.info("Starting AI News Digest monitoring")
    
    # Check if admin email is configured
    if not EMAIL_CONFIG['admin_email']:
        logger.error("No admin email configured for monitoring reports")
        return
    
    # Generate and send status report
    report = generate_status_report()
    success = send_status_report(report)
    
    if success:
        logger.info("Monitoring completed successfully")
    else:
        logger.error("Failed to send monitoring report")

if __name__ == "__main__":
    main() 