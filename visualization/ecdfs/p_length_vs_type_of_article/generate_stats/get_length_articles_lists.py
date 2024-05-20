"""

    Author: Daniel Markusson

"""

from visualization.get_json_dict import database


def get_length_articles_lists():
    """ Get the lengths of the articles in the database.

    Returns:
        tuple: A tuple containing three lists. The first list contains the lengths of all articles,
        the second list contains the lengths of the fake articles, and the third list contains the
        lengths of the real articles.
    """

    lengths_of_articles = []
    lengths_of_fakes = []
    lengths_of_reals = []

    for body, title in zip(database["articles"]["fake-articles"]["bodies"],
                           database["articles"]["fake-articles"]["titles"]):
        lengths_of_fakes.append(len(body) + len(title))
        lengths_of_articles.append(len(body) + len(title))
    for body, title in zip(database["articles"]["real-articles"]["bodies"],
                           database["articles"]["real-articles"]["titles"]):
        lengths_of_reals.append(len(body) + len(title))
        lengths_of_articles.append(len(body) + len(title))

    return lengths_of_articles, lengths_of_fakes, lengths_of_reals