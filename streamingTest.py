import praw

reddit = praw.Reddit(client_id = 'XQ8g_-vzWINK6w',
                     client_secret = 'w6oQWVna7ufQ0OnSUHl0p2UO1J8',
                     username = 'BrickRos',
                     password = 'ASDasdreddit98',
                     user_agent = 'JustATest')

subredditName = 'hiphopheads'
subreddit = reddit.subreddit(subredditName)

for comment in subreddit.stream.comments():
    try:
        print(comment.body)
    except praw.exceptions.PRAWException as e:
        pass
