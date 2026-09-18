import os
import time
import requests
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
    
    Format the output strictly as a JSON object with two keys: "english_content" and "urdu_content". The values should be the formatted HTML for each.
    """
    
    for attempt in range(3):
        try:
            response = model.generate_content(prompt)
            # Find JSON start and end
            content_text = response.text
            start = content_text.find('{')
            end = content_text.rfind('}') + 1
            if start != -1 and end != -1:
                return content_text[start:end]
            return None
        except Exception as e:
            time.sleep(2 ** attempt)
    return None

def update_website(ai_data_json):
    import json
    try:
        data = json.loads(ai_data_json)
        urdu_news = data['urdu_content']
        english_news = data['english_content']
        
        # Read the current index.html
        with open("index.html", "r", encoding="utf-8") as f:
            html_content = f.read()
            
        # Replace the placeholders with the actual news
        # Ensure your index.html has these IDs: latest-news-urdu and latest-news-english
        new_html = html_content.replace('<div id="latest-news-urdu">جیمنائی سے خبر جنریٹ ہو رہی ہے... (صبح 6 بجے اپ ڈیٹ ہوگی)</div>', f'<div id="latest-news-urdu">{urdu_news}</div>')
        new_html = new_html.replace('<div id="latest-news-english">Gemini is generating news... (Will update at 6 AM)</div>', f'<div id="latest-news-english">{english_news}</div>')
        
        # Write the updated HTML back to index.html
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(new_html)
        print("index.html successfully updated!")
    except Exception as e:
        print(f"Error updating website: {e}")

if __name__ == "__main__":
    title, summary = get_latest_news()
    if title and summary:
        print("Generating News...")
        ai_data = generate_blog_post(title, summary)
        if ai_data:
            print("Updating index.html...")
            update_website(ai_data)
        else:
            print("Failed to generate AI content.")
    else:
        print("No news found in the feed.")

