import feedparser
import pandas as pd
from bs4 import BeautifulSoup

url = 'https://tg.i-c-a.su/rss/alexlesleynew?limit=50'
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

print(df)