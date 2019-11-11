import praw
import nltk
from praw.models import MoreComments
from textblob import TextBlob
import re

def analyze_comment(comment):
    analysis = TextBlob(comment.body)
    weight = comment.score * analysis.polarity
    return weight

def depth_first_comment_iteration (level, comments):
    comments.replace_more(limit=None)
    opinion = 0
    relevance = 0
    for comment in comments:
        new_opinion = analyze_comment(comment)
        opinion += new_opinion
        relevance += comment.score
        print (new_opinion, 3 * level * ' ', comment.body)
        new_perception, new_relevance = depth_first_comment_iteration (level + 1, comment.replies)
        opinion += new_opinion
        relevance += comment.score

    return opinion, relevance

def tag_artists(raw_title):
    artist_patterns = [
        # Everything after  '] ' and before ' -'
        (r'(?<=] )(.*)(?=( ft| -))','NNP')
        # Only one feature so far
        # (r'(?i)(?:featuring|feat\.|feat|ft.|ft)[ ]?(.*?)[ ]?(?=\)|\,|\&)','NNP'),
    ]
    tokens = nltk.word_tokenize(raw_title)
    regex_artist_tagger = nltk.RegexpTagger(artist_patterns)
    tagged = regex_artist_tagger.tag(tokens)
    return tagged

def find_artist(title, tags):
    artists = []
    raw_mains = re.search(r"(?i)(?<=] )(.+?)(?= -| ft| featuring| feat)", title)
    mains = raw_mains.parse_main(raw_mains.match)
    raw_features = re.search('regex to find features', title)
    if (raw_features):
        features = raw_features.parse_features(raw_features.match)
    return

def parse_main(raw_main):
    mains = raw_main.split('&')
    mains

def main():
    with open('config.txt') as config:
        lines = config.readlines()
    comments = open('comments.txt', 'a')
    reddit = praw.Reddit(client_id = lines[0].rstrip(), client_secret = lines[1].rstrip(), username = lines[2].rstrip(), password = lines[3].rstrip(), user_agent = lines[4].rstrip())

    subreddit_name = 'hiphopheads'
    subreddit = reddit.subreddit(subreddit_name)
    hots = reddit.subreddit(subreddit_name).hot(limit = 1)
    tops = reddit.subreddit(subreddit_name).top('day', limit = 10)

    opinion = 0
    relevance = 0
    artists = []

    for post in tops:
        new_opinion = 0
        new_relevance = 0
        print(post.title)
        titleBlob = TextBlob(post.title)
        print(titleBlob.pos_tags)
        lowerTitleBlob = TextBlob(post.title.lower())
        print(lowerTitleBlob.pos_tags)
        # new_opinion, new_relevance = depth_first_comment_iteration(0, post.comments)
        # relevance += new_relevance
        # opinion += new_opinion
        find_artist(post.title, titleBlob.pos_tags)

    print ('The total relevance is ' , relevance, 'The total opinion is ', opinion)

if __name__ == "__main__":
    main()