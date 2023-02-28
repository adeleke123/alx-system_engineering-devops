#!/usr/bin/python3
"""Count it - a recursive function that queries the Reddit API"""
from requests import get
REDDIT = "https://www.reddit.com/"
HEADERS = {'user-agent': 'esw1229/0.0.1'}


def count_words(subreddit, word_list, after="", word_dic={}):
    """
    Returns a list containing the titles of all hot articles for a
    given subreddit.
    """
    if not word_dict:
        for word in word_list:
            word_dict[word] = 0

    if after is None:
        word_list = [[key, value] for key, value in word_dict.items()]
        word_list = sorted(word_list, key=lambda x: (-x[1], x[0]))
        for wrd in word_list:
            if wrd[1]:
                print("{}: {}".format(wrd[0].lower(), wrd[1]))
        return None

    url = REDDIT + "r/{}/hot/.json".format(subreddit)

    params = {
        'limit': 100,
        'after': after
    }

    r = get(url, headers=HEADERS, params=params, allow_redirects=False)

    if r.status_code != 200:
        return None

    try:
        js = r.json()

    except ValueError:
        return None

    try:

        data = js.get("data")
        after = data.get("after")
        children = data.get("children")
        for child in children:
            post = child.get("data")
            title = post.get("title")
            lower = [s.lower() for s in title.split(' ')]

            for wrd in word_list:
                word_dict[w] += lower.count(wrd.lower())

    except:
        return None

    count_words(subreddit, word_list, after, word_dict)
