import datetime
import feedparser
import time
from pymongo import MongoClient
from pyrogram import Client, MessageHandler

# ---------------------------------------- >> Connect to Mongodb
client = MongoClient('localhost', 27017)
db = client.test_database
collection = db.mmd
# ---------------------------------------- >> Connect to rss site
feed = feedparser.parse("https://www.yjc.ir/fa/rss/3")
app = Client('my_bot')


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


count_end = 0


def bot():
    with app:
        print(app.get_me())
        print('1')
        global count_end
        count_find = collection.find().count()
        all_news = collection.find()
        print('count_find : ', count_find)
        print('count_end : ', count_end)
        if count_find > count_end:
            for i in all_news:
                print(i)
                time.sleep(3)
                app.send_message(-1001476077997, '{0} \n {1} \n {2}'.format(i['title'], i['summary'], i['published']))
            count_end = count_find
            print('count_end : ', count_end)


while True:
    rss()
    print(datetime.datetime.now())
    bot()
    time.sleep(10)
