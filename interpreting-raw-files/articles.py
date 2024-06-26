"""


    Author: Daniel Markusson


"""

import linecache
import pandas as pd
from file_retrieval import get_raw_file_location

BUZZFEED_NAMES_DIR = get_raw_file_location("BuzzFeedNews.txt")
POLITIFACT_NAMES_DIR = get_raw_file_location("PolitiFactNews.txt")


def get_fake_real_dataframes():
    """ Returns the dataframes of the fake and real news articles from the BuzzFeed and PolitiFact 
        datasets.

    Returns:
        tuple: A tuple where the first element is a list of the real news dataframes and the second
        element is a list of the fake news dataframes.
    """
    # Reads the CSV files, filters the "NaN" characters, and stores them in temporary variables.
    buzzfeed_dataframe_fake = pd.read_csv(get_raw_file_location(
        "BuzzFeed_fake_news_content.csv")).fillna("None")
    buzzfeed_dataframe_real = pd.read_csv(get_raw_file_location(
        "BuzzFeed_real_news_content.csv")).fillna("None")
    politifact_dataframe_fake = pd.read_csv(get_raw_file_location(
        "PolitiFact_fake_news_content.csv")).fillna("None")
    politifact_dataframe_real = pd.read_csv(get_raw_file_location(
        "PolitiFact_real_news_content.csv")).fillna("None")

    real_dataframes = [buzzfeed_dataframe_real, politifact_dataframe_real]
    fake_dataframes = [buzzfeed_dataframe_fake, politifact_dataframe_fake]

    return real_dataframes, fake_dataframes


def get_articles_dict():
    """ Returns a dictionary where `get_articles_dict()['fake']` has the content of the fake news
        articles and `get_fake_real()['real']` has the content of the real news articles.

    Args:
        `showinfo` (bool, optional): If true, get_articles_dict() will print information regarding
        the files it reads. If false, it doesn't. Defaults to True.

    Returns:
        `dict()`: A dictionary who's key `['fake']` is a pandas dataframe of the various fake news
        articles within the dataset, and who's key `['real']` is a pandas dataframe of the various
        real news articles within the dataset.
    """

    # Creates a dictionary to store the data.
    data = {
        "fake-articles": {
            "ids": [],
            "titles": [],
            "bodies": [],
            "urls": [],
            "authors": [],
            "sources": [],
            "publish-dates": []
        },
        "real-articles": {
            "ids": [],
            "titles": [],
            "bodies": [],
            "urls": [],
            "authors": [],
            "sources": [],
            "publish-dates": []
        }
    }

    real_dataframes, fake_dataframes = get_clean_dataframes()

    for _, df in enumerate(real_dataframes):
        for uid in df.id:
            data["real-articles"]["ids"].append(uid)

        for title in df.title:
            data["real-articles"]["titles"].append(title)

        for body in df.text:
            data["real-articles"]["bodies"].append(body)

        for url in df.url:
            data["real-articles"]["urls"].append(url)

        for author_string in df.authors:
            a = author_string.split(",")
            author_list = []
            for author in a:
                if author == "None" or author.lower() == "view all posts":
                    continue
                author_list.append(author)
            data["real-articles"]["authors"].append(author_list)

        for source in df.source:
            data["real-articles"]["sources"].append(source)

        for publish_date in df.publish_date:
            data["real-articles"]["publish-dates"].append(publish_date)

    for _, df in enumerate(fake_dataframes):
        for uid in df.id:
            data["fake-articles"]["ids"].append(uid)

        for title in df.title:
            data["fake-articles"]["titles"].append(title)

        for body in df.text:
            data["fake-articles"]["bodies"].append(body)

        for url in df.url:
            data["fake-articles"]["urls"].append(url)

        for author_string in df.authors:
            a = author_string.split(",")
            author_list = []
            for author in a:
                if author == "None" or author.lower() == "view all posts":
                    continue
                author_list.append(author)
            data["fake-articles"]["authors"].append(author_list)

        for source in df.source:
            data["fake-articles"]["sources"].append(source)

        for publish_date in df.publish_date:
            data["fake-articles"]["publish-dates"].append(publish_date)

    return data


def get_clean_dataframes():
    """ Returns the dataframes of the fake and real news articles from the BuzzFeed and PolitiFact 
        datasets, but with the IDs changed to the format of the article names.

    Returns:
        tuple: A tuple where the first element is a list of the cleaned real news dataframes and 
        the second element is a list of the cleaned fake news dataframes.
    """
    real_dataframes, fake_dataframes = get_fake_real_dataframes()

    for i in range(2):
        for _, k in real_dataframes[i].iterrows():
            old_id = k.id
            num = int(old_id[old_id.index('_') + 1:old_id.index('-')]) + 1
            outlet = "buzzfeed" if i == 0 else "politifact"
            new_id = get_article_name(num, outlet, False)
            k.id = new_id

        for _, k in fake_dataframes[i].iterrows():
            old_id = k.id
            num = int(old_id[old_id.index('_') + 1:old_id.index('-')]) + 1
            outlet = "buzzfeed" if i == 0 else "politifact"
            new_id = get_article_name(num, outlet, True)
            k.id = new_id

    return real_dataframes, fake_dataframes


def get_article_name(id_num: int, outlet: str, is_fake: bool):
    """Gets the name of the article based on its `ID` and `outlet`.

    Args:
        ID (`int`): The ID of the article so that it can be found in the [outlet]News.txt file.
        outlet (`str`): The outlet of the article. ALL LOWERCASE (`buzzfeed` or `politifact`).
        is_fake: Is the article fake?

    Returns:
        `str`: Returns the name of the article.
    """
    # Because IDs correspond to the line number in the [outlet]News.txt files, we can use linecache
    # to quickly find the name within the file.
    if outlet == "buzzfeed":
        if is_fake:
            return linecache.getline(BUZZFEED_NAMES_DIR, id_num - 1 + 91)\
                .replace('\n', '')
        return linecache.getline(BUZZFEED_NAMES_DIR, id_num - 1)\
            .replace('\n', '')
    if is_fake:
        return linecache.getline(POLITIFACT_NAMES_DIR, id_num - 1 + 120)\
            .replace('\n', '')
    return linecache.getline(POLITIFACT_NAMES_DIR, id_num - 1)\
        .replace('\n', '')


def is_article_fake(name: str):
    """Returns `True` if article `name` is fake, and `False` if it is true.

    Args:
        name (`str`): The unique name of an article.

    Returns:
        `bool`: Returns `True` if article `name` is fake, and `False` if it is true.
    """
    if "Fake" in name:
        return True
    return False


ARTICLES_DICT = get_articles_dict()


def main():
    """ Main function to be run when current file is ran.
    """
    print('orange')
    print(ARTICLES_DICT["fake-articles"]["titles"])
    print('green')
    print(ARTICLES_DICT["real-articles"]["titles"])


if __name__ == "__main__":
    main()
