import feedparser
import time
from pymongo import MongoClient
import datetime
# ---------------------------------------- >> Connect to Mongodb
client = MongoClient('localhost', 27017)
db = client.test_database
collection = db.mmd
# ---------------------------------------- >> Connect to rss site
feed = feedparser.parse("https://www.yjc.ir/fa/rss/3")


def rss():
    # ---------------------------------------- >> Get information of rss site
    feed_entries = feed.entries
    for entry in feed_entries:
        title = entry.title
        summary = entry.summary
        published = entry.published
        img_link = entry.links
        if img_link[1]['href']:
            img_link = img_link[1]['href']
        else:
            pass
        post = {'title': title, 'summary': summary, 'published': published, 'img_links': img_link}
        # ---------------------------------------- >> Check information and insert to Mongodb
        dd = datetime.date.today()
        dd = dd.strftime('%d %b %Y')
        if dd in published:
            if collection.find(dict(title=post.get('title'))).count() != 0:
                print('This value exists')
            else:
                print('This value does not exist')
                posts = collection.insert_one(post).inserted_id
        else:
            pass


while True:

    rss()
    print(datetime.datetime.now())
    time.sleep(1)
