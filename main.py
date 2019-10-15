import praw
from praw.models import MoreComments
from textblob import TextBlob

def depth_first_comment_iteration (level, comments):
    comments.replace_more(limit=None)
    for comment in comments:
        print (level, 3 * level * ' ', comment.body)
        depth_first_comment_iteration (level + 1, comment.replies)
    return

def main():
    with open('config.txt') as config:
        lines = config.readlines()
    comments = open('comments.txt', 'a')
    reddit = praw.Reddit(client_id = lines[0].rstrip(), client_secret = lines[1].rstrip(), username = lines[2].rstrip(), password = lines[3].rstrip(), user_agent = lines[4].rstrip())

    subreddit_name = 'hiphopheads'
    subreddit = reddit.subreddit(subreddit_name)
    hots = reddit.subreddit(subreddit_name).hot(limit = 2)
    tops = reddit.subreddit(subreddit_name).top('day', limit = 1)

    for post in tops:
        print(post.title, '\n')
        depth_first_comment_iteration(0, post.comments)

if __name__ == "__main__":
    main()