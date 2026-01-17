import feedparser
import json
import datetime
from bs4 import BeautifulSoup
import os
import time

# Configuration
FEEDS_FILE = 'feeds.json'
TEMPLATE_FILE = 'template.html'
OUTPUT_FILE = 'index.html'
AVG_READING_SPEED = 230  # words per minute

def load_feeds():
    with open(FEEDS_FILE, 'r') as f:
        return json.load(f)

def clean_text(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.get_text(separator=' ', strip=True)

def get_reading_time(text):
    word_count = len(text.split())
    minutes = max(1, round(word_count / AVG_READING_SPEED))
    return minutes

def categorize(minutes):
    if minutes < 3:
        return 'flash', '⚡️ Flash'
    elif minutes <= 10:
        return 'short', '☕️ Short'
    else:
        return 'deep', '🧠 Deep'

def process_feed(feed_config):
    print(f"Fetching {feed_config['name']}...")
    try:
        feed = feedparser.parse(feed_config['url'])
        articles = []
        
        for entry in feed.entries:
            # Get content (summary or full content)
            content = ''
            if 'content' in entry:
                content = entry.content[0].value
            elif 'summary' in entry:
                content = entry.summary
            else:
                content = entry.title # Fallback

            text = clean_text(content)
            minutes = get_reading_time(text)
            category_slug, category_name = categorize(minutes)
            
            # Publish date
            published = 'Unknown date'
            if hasattr(entry, 'published'):
                published = entry.published
            elif hasattr(entry, 'updated'):
                published = entry.updated
                
            # Parse date for sorting if possible, otherwise use current time as fallback for sorting
            try:
                # This is a simplification; robust date parsing might need dateutil
                timestamp = time.mktime(entry.published_parsed) if hasattr(entry, 'published_parsed') and entry.published_parsed else time.time()
            except:
                timestamp = time.time()

            articles.append({
                'site': feed_config['name'],
                'title': entry.title,
                'url': entry.link,
                'minutes': minutes,
                'category_slug': category_slug,
                'category_name': category_name,
                'excerpt': text[:140] + '...' if len(text) > 140 else text,
                'timestamp': timestamp,
                'published_str': published
            })
        return articles
    except Exception as e:
        print(f"Error processing {feed_config['name']}: {e}")
        return []

def generate_html(articles):
    with open(TEMPLATE_FILE, 'r') as f:
        template = f.read()
    
    # Sort articles by date (newest first)
    articles.sort(key=lambda x: x['timestamp'], reverse=True)
    
    html_items = []
    for article in articles:
        item = f'''
        <li class="card" data-category="{article['category_slug']}">
            <a href="{article['url']}" target="_blank" rel="noopener noreferrer" style="text-decoration: none; color: inherit;">
                <div class="card-meta">
                    <span>{article['site']} • {article['minutes']} min read</span>
                    <span class="tag tag-{article['category_slug']}"></span>
                </div>
                <h2 class="card-title">{article['title']}</h2>
                <p class="card-excerpt">{article['excerpt']}</p>
            </a>
        </li>
        '''
        html_items.append(item)
    
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    
    final_html = template.replace('<!-- CONTENT_PLACEHOLDER -->', '\n'.join(html_items))
    final_html = final_html.replace('{{LAST_UPDATED}}', current_time)
    
    with open(OUTPUT_FILE, 'w') as f:
        f.write(final_html)
    print(f"Generated {OUTPUT_FILE} with {len(articles)} articles.")

def main():
    feeds = load_feeds()
    all_articles = []
    
    for feed in feeds:
        articles = process_feed(feed)
        all_articles.extend(articles)
    
    generate_html(all_articles)

if __name__ == "__main__":
    main()
