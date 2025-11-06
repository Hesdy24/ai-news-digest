#!/usr/bin/env python3
"""
Test script to generate email summary without sending
"""

import json
import os
import sys
from datetime import datetime
from dotenv import load_dotenv
from send_email import get_articles_from_last_week, generate_ai_summary, create_html_email

# Load environment variables
load_dotenv()

def test_email_generation():
    """Test email generation without sending."""
    print("🧪 Testing Email Generation\n")
    
    # Check if OpenAI API key is set
    if not os.getenv('OPENAI_API_KEY'):
        print("❌ OPENAI_API_KEY not found in .env file")
        return False
    
    print("✅ OpenAI API key found")
    
    # Check if recipient is set
    if not os.getenv('RECIPIENT_1'):
        print("❌ RECIPIENT_1 not found in .env file")
        return False
    
    print(f"✅ Recipient configured: {os.getenv('RECIPIENT_1')}\n")
    
    # Get articles from last week
    print("📰 Collecting articles from last 7 days...")
    articles_by_audience = get_articles_from_last_week()
    
    if 'audience_1' not in articles_by_audience or not articles_by_audience['audience_1']:
        print("❌ No articles found for audience_1 (SEO)")
        print("💡 Tip: Run 'python scrape.py' first to collect articles")
        return False
    
    articles = articles_by_audience['audience_1']
    print(f"✅ Found {len(articles)} articles for SEO audience\n")
    
    # Generate AI summary
    print("🤖 Generating AI summary with GPT-4o-mini...")
    print("   (This may take 10-30 seconds)\n")
    
    try:
        summary = generate_ai_summary(articles, 'audience_1')
        print("✅ Summary generated successfully!\n")
        print("=" * 60)
        print("SUMMARY:")
        print("=" * 60)
        print(summary)
        print("=" * 60)
        print()
        
        # Create HTML email
        print("📧 Creating HTML email template...")
        html_content = create_html_email(summary, 'audience_1', len(articles))
        
        # Save HTML to file for preview
        output_file = f"test_email_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ HTML email saved to: {output_file}")
        print(f"💡 Open this file in your browser to preview the email\n")
        
        # Ask if user wants to send test email
        print("📤 Ready to send test email?")
        print(f"   To: {os.getenv('RECIPIENT_1')}")
        response = input("   Send test email? (y/n): ").strip().lower()
        
        if response == 'y':
            from send_email import send_email
            subject = f"🤖 AI News Digest - Marketing & SEO Professional - Test - {datetime.now().strftime('%d %B %Y')}"
            success = send_email(os.getenv('RECIPIENT_1'), subject, html_content)
            
            if success:
                print("\n✅ Test email sent successfully!")
                return True
            else:
                print("\n❌ Failed to send email. Check logs for details.")
                return False
        else:
            print("\n⏭️  Skipping email send. You can test sending later with: python send_email.py")
            return True
        
    except Exception as e:
        print(f"\n❌ Error generating summary: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_email_generation()
    sys.exit(0 if success else 1)


