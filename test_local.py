#!/usr/bin/env python3
"""
AI News Digest - Local Test Script
Helps test the system locally before deploying to GitHub Actions.
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_environment():
    """Check if all required environment variables are set."""
    print("🔍 Checking environment variables...")
    
    required_vars = [
        'OPENAI_API_KEY',
        'EMAIL_USERNAME', 
        'EMAIL_PASSWORD',
        'RECIPIENT_1',
        'RECIPIENT_2'
    ]
    
    missing_vars = []
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            missing_vars.append(var)
        else:
            # Show first few characters for verification
            display_value = value[:8] + "..." if len(value) > 8 else value
            print(f"  ✅ {var}: {display_value}")
    
    if missing_vars:
        print(f"  ❌ Missing variables: {missing_vars}")
        print("\n📝 Please set these in your .env file:")
        for var in missing_vars:
            print(f"   {var}=your_value_here")
        return False
    
    print("  ✅ All environment variables are set!")
    return True

def test_scraping():
    """Test the RSS scraping functionality."""
    print("\n📰 Testing RSS scraping...")
    
    try:
        from scrape import main as scrape_main
        scrape_main()
        print("  ✅ Scraping completed successfully!")
        return True
    except Exception as e:
        print(f"  ❌ Scraping failed: {e}")
        return False

def test_email():
    """Test the email functionality."""
    print("\n📧 Testing email functionality...")
    
    try:
        from send_email import main as email_main
        email_main()
        print("  ✅ Email sending completed successfully!")
        return True
    except Exception as e:
        print(f"  ❌ Email sending failed: {e}")
        return False

def check_data_files():
    """Check if data files exist and show statistics."""
    print("\n📊 Checking data files...")
    
    data_dir = "data"
    if not os.path.exists(data_dir):
        print("  ❌ Data directory not found")
        return False
    
    files = [f for f in os.listdir(data_dir) if f.endswith('.json')]
    
    if not files:
        print("  ❌ No data files found")
        return False
    
    print(f"  ✅ Found {len(files)} data files:")
    
    total_articles = 0
    for file in sorted(files)[-5:]:  # Show last 5 files
        file_path = os.path.join(data_dir, file)
        try:
            import json
            with open(file_path, 'r', encoding='utf-8') as f:
                articles = json.load(f)
            print(f"    📄 {file}: {len(articles)} articles")
            total_articles += len(articles)
        except Exception as e:
            print(f"    ❌ {file}: Error reading file - {e}")
    
    print(f"  📈 Total articles in recent files: {total_articles}")
    return True

def main():
    """Main test function."""
    print("🤖 AI News Digest - Local Test Suite")
    print("=" * 50)
    
    # Check environment
    env_ok = check_environment()
    
    if not env_ok:
        print("\n❌ Environment check failed. Please fix the issues above.")
        return
    
    # Check data files
    data_ok = check_data_files()
    
    # Test scraping
    scrape_ok = test_scraping()
    
    # Test email (only if scraping worked)
    email_ok = False
    if scrape_ok:
        email_ok = test_email()
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 Test Summary:")
    print(f"  Environment: {'✅' if env_ok else '❌'}")
    print(f"  Data Files: {'✅' if data_ok else '❌'}")
    print(f"  Scraping: {'✅' if scrape_ok else '❌'}")
    print(f"  Email: {'✅' if email_ok else '❌'}")
    
    if all([env_ok, scrape_ok, email_ok]):
        print("\n🎉 All tests passed! Your system is ready for GitHub Actions.")
    else:
        print("\n⚠️  Some tests failed. Please fix the issues before deploying.")

if __name__ == "__main__":
    main() 