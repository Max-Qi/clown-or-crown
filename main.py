import praw
import nltk
from textblob import TextBlob
import re
import wikipedia

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

def find_artists_from_song(title):
    mains = []
    features = []
    raw_mains = re.search(r"(?i)(?<=] )(.+?)(?= -| ft| featuring| feat)", title)
    if (raw_mains):
        mains = raw_mains.parse_main_artists(raw_mains.match)
    else:
        return mains, features

    raw_features = re.search(r"(?i)(?:featuring|feat|ft)[.]?[ ](.+?)(?=\)| -|$)", title)
    if (raw_features):
        features = raw_features.parse_feature_artists(raw_features.match)

    return mains, features

def parse_main_artists(raw_artists):
    split_symbols = [', ', ' x ', ' & ']
    artists = []
    for symbol in split_symbols:
        new_artists = raw_artists.split(symbol)
        if (len(new_artists) > 1):
            artists = new_artists
            break;
    return artists

def parse_feature_artists(raw_artists):
    split_symbols = [', ', ' & ']
    artists = []
    artists.append(raw_artists)
    for symbol in split_symbols:
        for artist in artists:
            split = artist.split(symbol)

    return

def find_artists_from_text(title):
    wiki_artists = []
    wiki_groups = []
    raw_wiki_artists = wikipedia.page('List of hip hop musicians').links
    raw_wiki_groups = wikipedia.page('List of hip hop groups').links
    for each in raw_wiki_artists:
        another = re.search(r"(.*) \(.*\)", each)
        if another:
            another = another.group(1)
        else:
            another = each
        wiki_artists.append(another)

    for each in raw_wiki_groups:
        another = re.search(r"(.*) \(.*\)", each)
        if another:
            another = another.group(1)
        else :
            another = each
        wiki_groups.append(another)

    return combine(wiki_artists, wiki_groups)

def combine (arr1, arr2):
    return;

def main():
    with open('config.txt') as config:
        lines = config.readlines()
    comments = open('comments.txt', 'a')
    reddit = praw.Reddit(client_id = lines[0].rstrip(), client_secret = lines[1].rstrip(), username = lines[2].rstrip(), password = lines[3].rstrip(), user_agent = lines[4].rstrip())

    subreddit_name = 'hiphopheads'
    subreddit = reddit.subreddit(subreddit_name)
    news = reddit.subreddit(subreddit_name).new(limit = 5)
    tops = reddit.subreddit(subreddit_name).top('day', limit = 10)

    opinion = 0
    relevance = 0
    artists = []

    for post in news:
        new_opinion = 0
        new_relevance = 0
        print(post.title)
        main_artists, feature_artists = find_artists_from_song(post.title)
        if not main_artists:
            main_artists = find_artists_from_text(post.title)
        # titleBlob = TextBlob(post.title)
        # print(titleBlob.pos_tags)
        # new_opinion, new_relevance = depth_first_comment_iteration(0, post.comments)
        # relevance += new_relevance
        # opinion += new_opinion

    print ('The total relevance is ' , relevance, 'The total opinion is ', opinion)

if __name__ == "__main__":
    main()