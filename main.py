import praw
import nltk
from textblob import TextBlob
import re
import wikipedia
from math import floor

def get_all_artists():
    wiki_artists = []
    wiki_groups = []
    raw_wiki_artists = wikipedia.page('List of hip hop musicians').links
    raw_wiki_groups = wikipedia.page('List of hip hop groups').links
    last = ''

    for each in raw_wiki_artists:
        another = re.search(r'(.*) \(.*\)', each)
        if another:
            another = another.group(1)
        else:
            another = each
        if 'ASAP' in another:
            another = another.replace('ASAP', 'A$AP')
        if (another != last):
            wiki_artists.append(another)
        last = another

    for each in raw_wiki_groups:
        another = re.search(r'(.*) \(.*\)', each)
        if another:
            another = another.group(1)
        else:
            another = each
        if 'ASAP' in another:
            another = another.replace('ASAP', 'A$AP')
        if (another != last):
            wiki_groups.append(another)
        last = another

    return combine(wiki_artists, wiki_groups)

def combine(arr1, arr2):
    everyone = []
    it1 = 0
    it2 = 0
    size1 = len(arr1)
    size2 = len(arr2)
    while (it1 != size1 - 1 and it2 != size2 - 1):
        if (it1 == len(arr1) - 1):
            everyone.append(arr2[it2])
            it2 += 2
        elif (it2 == len(arr2) - 1):
            everyone.append(arr1[it1])
            it1 += 1
        elif (arr1[it1] < arr2[it2]):
            everyone.append(arr1[it1])
            it1 += 1
        elif (arr1[it1] >= arr2[it2]):
            everyone.append(arr2[it2])
            it2 += 1
    everyone.sort()
    return everyone

def check_if_garbage(main_artists, feature_artists, all_artists):
    artists = []
    for artist in main_artists + feature_artists:
        if binary_search(artist, all_artists):
            artists.append(artist)
    return artists

def binary_search(e, array):
    if len(array) == 0:
        return False
    if len(array) != 1:
        mid = floor((len(array)-1)/2)
        if array[mid] == e:
            return True
        elif array[mid] < e:
            return binary_search(e, array[mid+1:])
        elif array[mid] > e:
            return binary_search(e, array[:mid])
    else:
        if array[0] == e:
            return True
        else:
            return False

def analyze_comment(comment):
    analysis = TextBlob(comment.body)
    opinion = comment.score * analysis.polarity
    return opinion

def depth_first_comment_iteration (level, comments, artists_dict):
    comments.replace_more(limit=None)
    opinion = 0
    relevance = 0

    for comment in comments:
        new_opinion = analyze_comment(comment)
        for artist in artists_dict:
            artists_dict[artist][opinion] += new_opinion
            artists_dict[artist][relevance] += comment.score
        print (3 * level * ' ', comment.body)
        artists_dict = depth_first_comment_iteration (level + 1, comment.replies, artists_dict)

    return artists_dict

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

def find_artists_from_regex(title):
    mains = []
    features = []
    raw_mains = (re.search(r"(?i)(?<=] )(.+?)(?= -| ft| featuring| feat)", title) or re.search(r"(?i)(?<=^)(.+?)(?= -| ft| featuring| feat)", title))
    if (raw_mains):
        mains = parse_main_artists(raw_mains.group(1))
    else:
        return mains, features

    raw_features = re.search(r"(?i)(?:featuring|feat|ft)[.]?[ ](.+?)(?=\)| -|$)", title)
    if (raw_features):
        features = parse_feature_artists(raw_features.group(1))

    return mains, features

def parse_main_artists(raw_artists):
    split_symbols = [', ', ' x ', ' & ']
    artists = []
    artists.append(raw_artists)
    for symbol in split_symbols:
        new_artists = raw_artists.split(symbol)
        if (len(new_artists) > 1):
            artists = new_artists
            break
    return artists

def parse_feature_artists(raw_artists):
    split_symbols = [', ', ' & ']
    artists = []
    for symbol in split_symbols:
        raw_artists = raw_artists.replace(symbol, '|BREAK|')

    artists = raw_artists.split('|BREAK|')
    return artists

# Need to fix capitalization somehow
def find_artists_from_text(text, all_artists):
    artists = []
    for each_artist in all_artists:
        regex = r'( |^)' + re.escape(each_artist) + '(\W|$)'
        if (re.search(regex, text)):
            artists.append(each_artist)
    return artists;


def parse_for_repeats(main_artists):
    artists = []
    artist_dict = {}
    for artist in main_artists:
        artist_dict[artist] = True

    for big_artist in main_artists:
        for small_artist in main_artists:
            if big_artist != small_artist and small_artist in big_artist:
                artist_dict[small_artist] = False

    for artist in artist_dict:
        if artist_dict[artist] == True:
            artists.append(artist)

    return artists


def main():
    with open('config.txt') as config:
        lines = config.readlines()
    comments = open('comments.txt', 'a')
    reddit = praw.Reddit(client_id = lines[0].rstrip(), client_secret = lines[1].rstrip(), username = lines[2].rstrip(), password = lines[3].rstrip(), user_agent = lines[4].rstrip())

    subreddit_name = 'hiphopheads'
    subreddit = reddit.subreddit(subreddit_name)
    news = reddit.subreddit(subreddit_name).new(limit = 50)
    tops = reddit.subreddit(subreddit_name).top('week', limit = 50)

    opinion = 0
    relevance = 0
    artists = []
    all_artists = get_all_artists()
    for post in tops:

        print(post.title)
        main_artists, feature_artists = find_artists_from_regex(post.title)
        if (main_artists or feature_artists):
            artists = check_if_garbage(main_artists, feature_artists, all_artists)
        if (not (main_artists or feature_artists or artists)):
            artists = find_artists_from_text(post.title, all_artists)
        artists = parse_for_repeats(artists)
        print(artists)

        titleBlob = TextBlob(post.title)
        artists_dict = {}
        for artist in artists:
            artists_dict[artist] = {
                opinion: 0,
                relevance: 0,
            }
        artists_dict = depth_first_comment_iteration(0, post.comments, artists_dict)
        artists = []

    print ('The total relevance is ', relevance, 'The total opinion is ', opinion)

if __name__ == "__main__":
    main()