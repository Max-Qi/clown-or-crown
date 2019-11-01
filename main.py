import praw
import nltk
from praw.models import MoreComments
from textblob import TextBlob

def analyze_comment(comment):
    analysis = TextBlob(comment.body)
    weight = comment.score * analysis.polarity
    return weight

def depth_first_comment_iteration (level, comments):
    comments.replace_more(limit=None)
    weight = 0
    for comment in comments:
        new_weight = analyze_comment(comment)
        weight += new_weight
        print (new_weight, 3 * level * ' ', comment.body)
        weight += depth_first_comment_iteration (level + 1, comment.replies)
    return weight

def tag_artists(title):
    artist_patterns = [
        (r'','NNP'),
        (r'','NNP'),
        (r'','NNP'),
    ]
    regex_artist_tagger = nltk.RegexpTagger(artist_patterns)
    return


def extract_name(title):

    return


def main():
    with open('config.txt') as config:
        lines = config.readlines()
    comments = open('comments.txt', 'a')
    reddit = praw.Reddit(client_id = lines[0].rstrip(), client_secret = lines[1].rstrip(), username = lines[2].rstrip(), password = lines[3].rstrip(), user_agent = lines[4].rstrip())

    subreddit_name = 'hiphopheads'
    subreddit = reddit.subreddit(subreddit_name)
    hots = reddit.subreddit(subreddit_name).hot(limit = 1)
    tops = reddit.subreddit(subreddit_name).top('day', limit = 1)

    weight = 0

    for post in tops:
        print(post.title, '\n')
        testBlob = TextBlob(post.title)
        testBlob.pos_tags = tag_artists(post.title)
        extract_name(post.title)

        print(testBlob.pos_tags)
        weight += depth_first_comment_iteration(0, post.comments)

    print ('The total weight is ' , weight)

if __name__ == "__main__":
    main()