import praw

reddit = praw.Reddit(client_id = 'e51alGh5lHsHRQ',
                     client_secret = 'b8E3JLiTtvGA8G2cPsb7Rht15sM',
                     username = 'BrickRos',
                     password = 'ASDasdreddit98!',
                     user_agent = 'JustATest')

subredditName = 'hiphopheads'
subreddit = reddit.subreddit(subredditName)

for comment in subreddit.stream.comments():
    try:
        print(comment.body)
    except praw.exceptions.PRAWException as e:
        pass
