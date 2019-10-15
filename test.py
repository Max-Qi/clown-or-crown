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

subredditName = 'hiphopheads'
subreddit = reddit.subreddit(subredditName)

hots = subreddit.hot(limit = 1)


def depthFirstIteration (level, comment):
    print (4 * level * ' ', comment.body)
    comment.replies.replace_more(limit=None)
    for reply in comment.replies:
        depthFirstIteration (level + 1, reply)
    return


for submission in hots:
    # if not submission.stickied:
        print(submission.title, submission.num_comments)
        submission.comments.replace_more(limit=None)
        # comments.replace_more(limit = 0)
        for topLevelComment in submission.comments:
            depthFirstIteration(0, topLevelComment)
