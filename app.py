from flask import Flask, render_template, request
import feedparser
import pandas as pd
from bs4 import BeautifulSoup

app = Flask(__name__)

def get_data(url):
    feed = feedparser.parse(url)

    if feed.bozo:
        print(f"Error reading feed: {feed.bozo_exception}")
    else:
        print(f"Feed read successfully, {len(feed.entries)} entries found")

    data = []

    for entry in feed.entries:
        cleaned_summary = BeautifulSoup(getattr(entry, 'summary', None), 'html.parser').get_text().split('#', 1)[0].replace("\n","")
        data.append({
            'title': getattr(entry, 'title', None),
            'link': getattr(entry, 'link', None),
            'published': pd.to_datetime(getattr(entry, 'published', None)),
            'summary': cleaned_summary
        })

    df = pd.DataFrame(data)
    return df['summary'].tolist()

@app.route('/', methods=['GET', 'POST'])
def home():
    summary = None
    if request.method == 'POST':
        url = request.form.get('url')
        summary = get_data(url)
    return render_template('index.html', summary=summary)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
