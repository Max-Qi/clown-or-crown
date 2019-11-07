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
    perception = 0
    relevance = 0
    for comment in comments:
        relevance += 9
        # This is not a perfect way, need to count downvotes too
        relevance += comment.score
        new_weight = analyze_comment(comment)
        perception += new_weight
        print (new_weight, 3 * level * ' ', comment.body)
        new_perception, new_relevance = depth_first_comment_iteration (level + 1, comment.replies)
    return perception, relevance

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
    tops = reddit.subreddit(subreddit_name).top('day', limit = 10)

    perception = None
    relevance = None

    for post in tops:
        new_perception = 0
        new_relevance = 0
        new_relevance += 90
        print(post.title)
        testBlob = TextBlob(post.title)
        # testBlob.pos_tags = tag_artists(post.title)
        # extract_name(post.title)

        print(testBlob.pos_tags)
        new_perception, new_relevance = depth_first_comment_iteration(0, post.comments)
        relevance += new_relevance
        perception += new_perception

    print ('The total perception is ' , perception)

if __name__ == "__main__":
    main()