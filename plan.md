Here is the detailed technical specification for your Time-First Personal Reader. Since you know C++, you will find the Python logic very straightforward.

Markdown

# Project Spec: "Time-First" Personal Reader
**Goal:** A blazing fast, distraction-free reading web app that aggregates content and sorts it by "Available Attention."
**Stack:** Python (Backend Logic), GitHub Actions (Automation), HTML/CSS (Frontend), GitHub Pages (Hosting).

## Phase 1: The Data Layer (The "Engine")

We need a central list of sources and a script to process them.

### 1.1 Source Management (`feeds.json`)
A simple JSON file in your repository to manage your subscriptions.
```json
[
  { "name": "Paul Graham", "url": "[http://www.paulgraham.com/rss.html](http://www.paulgraham.com/rss.html)" },
  { "name": "Hacker News", "url": "[https://news.ycombinator.com/rss](https://news.ycombinator.com/rss)" },
  { "name": "The Verge", "url": "[https://www.theverge.com/rss/index.xml](https://www.theverge.com/rss/index.xml)" }
]
1.2 The Builder Script (builder.py)
This script runs on the server (GitHub Actions). It does the heavy lifting so your phone doesn't have to.

Logic Flow:

Fetch: Load feeds.json and request every URL.

Parse: Use a library like feedparser to extract Title, Link, and Content.

Clean & Measure:

Strip HTML tags from the content (using BeautifulSoup).

Count words.

Reading Time = Word Count / 230 (Average reading speed).

Categorize: Assign a "Bucket" tag:

⚡️ Flash: < 3 mins

☕️ Short: 3 - 10 mins

🧠 Deep: > 10 mins

Generate: Create a static index.html file populated with this data.

Phase 2: The Interface (The "Delight")
The output is a single, static HTML file. Zero database queries on load.

2.1 The UI Structure (index.html template)
Header: "Read [Time of Last Update]"

Filter Tabs: [All] [Flash] [Short] [Deep]

Tip: Use simple JavaScript to hide/show list items based on class names when these are clicked. Instant interaction.

The Feed:

List of cards.

Card Layout:

Top: Site Name (e.g., "Paul Graham") • 5m read

Middle: Article Title (Bold, Large)

Bottom: First 140 chars of text (the hook)...

Footer: "Built by Aditya"

2.2 The "App" Feel (PWA)
To make it feel like a native iPhone app, we add specific meta tags to the <head> of your HTML:

HTML

<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no">
Result: When you "Add to Home Screen," it removes the Safari address bar and navigation buttons. It looks 100% native.

Phase 3: Automation (The "Set and Forget")
You don't want to run the script manually. GitHub Actions will do it for you.

3.1 Workflow File (.github/workflows/update_feed.yml)
Trigger:

schedule: cron: '0 * * * *' (Runs every hour).

workflow_dispatch: (Allows you to click a button to force update manually).

Steps:

Checkout code.

Set up Python.

Install dependencies (pip install feedparser beautifulsoup4).

Run python builder.py.

Commit the new index.html to the gh-pages branch (or main).

Phase 4: Discovery (The "Hack")
You mentioned discovery is a problem.

Initial: Start with the "classics" (Paul Graham, Stratechery, etc.).

The Feature: Add a "Feed Discovery" section in your feeds.json later. You can scrape "Best of" lists from Hacker News periodically to auto-populate a "Suggestions" bucket.

Summary of Files Needed
feeds.json (Your list)

requirements.txt (Python libs)

builder.py (The brain)

template.html (The skeleton)

.github/workflows/update.yml (The heartbeat)


### Ready to build?
The first step is simply creating a GitHub repository. I can provide the **exact code** for `builder.py` and the `template.html` whenever you are ready to copy-paste. Would you like the code now?