import json
import sys

FEEDS_FILE = 'feeds.json'

def load_feeds():
    try:
        with open(FEEDS_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_feeds(feeds):
    with open(FEEDS_FILE, 'w') as f:
        json.dump(feeds, f, indent=2)
        f.write('\n') # Add newline at end of file

def add_feed(name, url):
    feeds = load_feeds()
    
    # Check for duplicates
    for feed in feeds:
        if feed['url'] == url:
            print(f"Feed with URL '{url}' already exists (Name: {feed['name']}).")
            return
        if feed['name'] == name:
            print(f"Warning: Feed with name '{name}' already exists.")
            # We allow duplicate names but warn

    feeds.append({'name': name, 'url': url})
    save_feeds(feeds)
    print(f"Successfully added '{name}' ({url}) to {FEEDS_FILE}.")

def main():
    if len(sys.argv) != 3:
        print("Usage: python add_feed.py <Name> <URL>")
        print("Example: python add_feed.py \"TechCrunch\" \"https://techcrunch.com/feed/\"")
        sys.exit(1)
    
    name = sys.argv[1]
    url = sys.argv[2]
    add_feed(name, url)

if __name__ == "__main__":
    main()
