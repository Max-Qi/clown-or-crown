import praw

with open('config.txt') as f:
    lines = f.readlines()

# for i in range(len(lines)):
#     lines[i].rstrip('\n')

reddit = praw.Reddit(client_id = lines[0].rstrip(),
                     client_secret = lines[1].rstrip(),
                     username = lines[2].rstrip(),
                     password = lines[3].rstrip(),
                     user_agent = lines[4].rstrip())

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
        # comments.replace_more(limit = 0)
        for topLevelComment in comments:
            depthFirstIteration(0, topLevelComment)
