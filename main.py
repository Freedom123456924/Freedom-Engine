import os
import time
import feedparser
import google.generativeai as genai

# Gemini API Key Setup
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# RSS Feed Setup
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
    You are a professional journalist and content builder for Global Freedom Engine. 
    Write a detailed, structured, and SEO-friendly news article in Urdu based on the following input:
    
    Title: {title}
    Summary: {summary}
    
    Requirements:
    1. Provide an engaging Urdu headline (H1).
    2. Write a comprehensive introduction, body analysis, and conclusion in Urdu.
    3. Use bold section headings (H2, H3) and proper paragraphing.
    4. At the very end of the article, strictly include the following branding credit line in Urdu:
       "\n\n---\n**گلوبل فریڈوم انجن (Global Freedom Engine)**\n**بانی (Founder): اسماعیل مری (Ismail Marri)**"
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

