import os
import time
import feedparser
import google.generativeai as genai

# Gemini API Key Setup
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# Global RSS Feed Setup
RSS_URL = "https://www.reutersagency.com/feed/?best-topics=top-news&post_type=best"

def get_latest_news():
    feed = feedparser.parse(RSS_URL)
    if feed.entries:
        first_entry = feed.entries[0]
        return first_entry.title, first_entry.summary
    return None, None

def generate_blog_post(title, summary):
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    prompt = f"""
    You are an international journalist for Global Freedom Engine.
    Generate a dual-language (English and Urdu) comprehensive article based on this news:
    
    Title: {title}
    Summary: {summary}
    
    Requirements:
    1. First, write the complete article in professional ENGLISH (Headline, Key Points, Analysis, Conclusion).
    2. Next, write the complete article in professional URDU (عنوان، اہم نکات، تجزیہ، خلاصہ).
    3. End the entire post with this strict founder branding credit in BOTH languages:
       
       ---
       **Global Freedom Engine**
       *Founder & Visionary:* **Ismail Marri**
       
       **گلوبل فریڈوم انجن**
       *بانی:* **اسماعیل مری**
    """
    
    for attempt in range(3):
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            time.sleep(2 ** attempt)
    return None

if __name__ == "__main__":
    title, summary = get_latest_news()
    if title and summary:
        post_content = generate_blog_post(title, summary)
        print("Generated Article Output:")
        print(post_content)
