import datetime
import feedparser
import time
import wget
import os
from pymongo import MongoClient
from pyrogram import Client
# ---------------------------------------- >> Connect to Mongodb
client = MongoClient('localhost', 27017)
db = client.rss_bot
collection = db.rss_news
# ---------------------------------------- >> Connect to rss site
feed = feedparser.parse("https://www.khabaronline.ir/rss/tp/1")

app = Client('my_bot')

chanel_id = -1001476077997


def get_rss_news():
    # ---------------------------------------- >> Get information of rss site
    try:
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
    except TimeoutError as Ter:
        print('message Error : ', Ter)


# --------------------------------------- >> Deleted past news of Mongodb
def deleted_past_news():
    dd = datetime.date.today()
    dd = dd.strftime('%d %b %Y')
    all_news = collection.find()
    for i in all_news:
        if dd in i['published']:
            print('This news is new')
        else:
            collection.delete_one(i)
            print('Message is deleted')


count_end = 0


def send_news():
    with app:
        global count_end
        count_find = collection.find().count()
        all_news = collection.find().sort('published')
        try:
            if count_find > count_end:
                for i in all_news:
                    if i['img_links']:
                        img_file = wget.download(i['img_links'])
                        time.sleep(2)
                        app.send_photo(chanel_id, photo=img_file, caption='✉ {0} \n\n 🔎{1} \n\n '.format(i['title'], i['summary']))
                        print('Send message')
                        os.remove(img_file)
                    else:
                        time.sleep(2)
                        app.send_message(chanel_id, '✉ {0} \n\n 🔎{1} \n\n '.format(i['title'], i['summary']))
                deleted_past_news()
                count_end = count_find
        except TimeoutError as Ter:
            print('message Error : ', Ter)


while True:
    get_rss_news()
    print(datetime.datetime.now())
    send_news()
    time.sleep(120)
