from flask import Flask, render_template
import feedparser
from datetime import datetime

app = Flask(__name__)

# List of RSS feed URLs
FEED_URLS = [
    'https://www.theverge.com/rss/index.xml',
    'https://www.wired.com/feed/rss',
    'https://mashable.com/feed'
]

@app.route('/')
def home():
    articles = []
    for url in FEED_URLS:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            # Filter articles published after January 1st, 2022
            try:
                # Attempt to parse the published date
                published_date = datetime.strptime(entry.published, '%a, %d %b %Y %H:%M:%S %Z')
                if published_date.year >= 2022:
                    articles.append({
                        'title': entry.title,
                        'url': entry.link,
                        'published': entry.published
                    })
            except ValueError:
                # If there's a ValueError, skip this entry
                continue
    # Sort articles by publish date in reverse order
    try:
        articles.sort(key=lambda x: datetime.strptime(x['published'], '%a, %d %b %Y %H:%M:%S %Z'), reverse=True)
    except ValueError:
        # If there's a ValueError, return an error message
        return "Error: Unable to sort articles by publish date."

    return render_template('index.html', articles=articles)

if __name__ == '__main__':
    app.run(debug=True)
