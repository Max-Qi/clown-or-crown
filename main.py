import praw
import mysql.connector
import time
import datetime
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

with open('config.txt') as f:
    lines = f.readlines()

reddit = praw.Reddit(client_id = lines[0].rstrip(), client_secret = lines[1].rstrip(), username = lines[2].rstrip(), password = lines[3].rstrip(), user_agent = lines[4].rstrip())
db = mysql.connector.connect(host = "localhost", user = "root", passwd = lines[5].rstrip(), database = "test1")
cursor = db.cursor()

subredditName = 'hiphopheads'
subreddit = reddit.subreddit(subredditName)

i = 0
for comment in subreddit.stream.comments():
    if i <= 100:
        command =  "INSERT IGNORE INTO comment (rid, message, upvotes, poster, time) VALUES (%s,%s,%s,%s,%s)"
    else:
        command = "INSERT INTO comment (rid, message, upvotes, poster, time) VALUES (%s,%s,%s,%s,%s)"
    parsedTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(comment.created_utc))
    values = (comment.id, comment.body, comment.score, comment.author.name, parsedTime)
    cursor.execute(command, values)
    db.commit()
    i += 1;
    print (i)