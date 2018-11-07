import praw

reddit = praw.Reddit(client_id = 'I dont know about you',
                     client_secret = 'but im feeling 22',
                     username = 'everythings gonna be alright',
                     password = 'you keep me next to you',
                     user_agent = 'you dont know about me')

subredditName = 'hiphopcirclejerk'
subreddit = reddit.subreddit(subredditName)

hots = subreddit.hot(limit = 3)


def depthFirstIteration (level, comment):
    print (4 * level * ' ', comment.body)
    for reply in comment.replies:
        depthFirstIteration (level + 1, reply)
    return

def breadthFirstIteration (comment):
    for comment in comments.list():
        commentCount = commentCount + 1
        print (comment.body)
    return

for submission in hots:
    if not submission.stickied:
        print(submission.title, submission.num_comments)
        comments = submission.comments
        commentCount = 0
        comments.replace_more(limit = 1)

        for topLevelComment in comments:
            depthFirstIteration(0, topLevelComment)
