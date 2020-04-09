import datetime
import feedparser
import time
import wget
import os
from pymongo import MongoClient
from pyrogram import Client
from urllib.error import URLError
# ---------------------------------------- >> Connect to Mongodb
client = MongoClient('localhost', 27017)
db = client.rss_bot
collection = db.rss_news
# ---------------------------------------- >> Connect to Bot
app = Client('my_bot')

# ---------------------------------------- >> Chanel _id
chanel_id = -1001476077997

# ---------------------------------------- >> Get url site of File.txt
with open('C:/Users/Mohammad/Desktop/Python_Project/telegram_rss_bot/site.txt', 'r') as site:
    site = site.read()
    site = site.split('\n')
l_site = len(site)


# ---------------------------------------- >> Get information of rss site
def get_rss_news():
    global l_site, published
    try:
        for i in range(0, l_site):
            feed = feedparser.parse(site[i])
            feed_entries = feed.entries
            for entry in feed_entries:
                title = entry.title

                if entry.get('summary'):
                    summary = entry.summary
                else:
                    summary = None

                if entry.published:
                    published = entry.published
                elif entry.pubDate:
                    published = entry.pubDate

                if len(entry.links) == 2:
                    img_link = entry.links[1]['href']
                else:
                    img_link = None

                post = {'title': title, 'summary': summary, 'published': published, 'img_links': img_link}
                # ---------------------------------------- >> Check information and insert to Mongodb
                dd = datetime.date.today()
                dd = dd.strftime('%d %b %Y')
                count_repetitious_news = 0
                if dd in published:
                    for g in collection.find():
                        if str(g.get('title')) in str(post.get('title')) or str(g.get('summary')) in str(post.get('summary')):
                            count_repetitious_news += 1
                    print(count_repetitious_news)
                    if count_repetitious_news > 0:
                        print('This value exists')
                    elif count_repetitious_news == 0:
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
            print('This news for today : ', i['title'])
        else:
            collection.delete_one(i)
            print('Message is deleted : ', i['title'])


count_end = 0


# ----------------------------------- >> Send news to chanel
def send_news():
    try:
        with app:
            global count_end
            all_news = list(collection.find().sort('published'))
            count_all = len(all_news)
            for i in all_news[count_end:count_all]:
                if i['img_links']:
                    time.sleep(10)
                    img_file = wget.download(i['img_links'])
                    app.send_photo(chanel_id, photo=img_file, caption='✉ {0} \n\n 🔎{1} \n\n ✅@chanel_id'.format(i['title'], i['summary']))
                    os.remove(img_file)
                    print('This message :', i['title'], 'is SEND...')
                else:
                    time.sleep(10)
                    app.send_message(chanel_id, '✉ {0} \n\n 🔎{1} \n\n ✅@chanel_id'.format(i['title'], i['summary']))
            deleted_past_news()
            count_end = count_all
            print(count_end)
    except URLError or TimeoutError:
        pass


while True:
    get_rss_news()
    print(datetime.datetime.now())
    send_news()
    time.sleep(120)
