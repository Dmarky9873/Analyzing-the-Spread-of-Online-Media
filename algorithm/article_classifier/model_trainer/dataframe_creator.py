"""

    Author: Daniel Markusson


"""

import pandas as pd
from algorithm.get_json_dict import DATABASE
from visualization.ecdfs.sentiment_vs_type_of_article.generate_stats.get_sentiment_stats import \
    get_sentiment_score
import numpy as np
from readability import Readability
from readability.text import Analyzer
from rich.progress import track


def get_dataframe():
    """ Create a dataframe from the data in the DATABASE to be interpreted by a machine learning
        model.

    Returns:
        `Pandas Dataframe`: The dataframe containing the data.
    """
    column_labels = ['length', 'shares',
                     'num_authors', 'sentiment-score', 'readability-score', 'is-fake']

    data = []

    fake_titles = DATABASE['articles']['fake-articles']['titles']
    fake_bodies = DATABASE['articles']['fake-articles']['bodies']
    fake_authors = DATABASE['articles']['fake-articles']['authors']

    real_titles = DATABASE['articles']['real-articles']['titles']
    real_bodies = DATABASE['articles']['real-articles']['bodies']
    real_authors = DATABASE['articles']['real-articles']['authors']

    counts = DATABASE['articles']['counts']

    for i, article_id in track(enumerate(DATABASE['articles']['fake-articles']['ids']), description="Creating fake article data"):
        curr_article_data = []

        length = len(fake_titles[i]) + len(fake_bodies[i])

        num_authors = len(fake_authors[i])

        text = ' '.join([fake_bodies[i], fake_titles[i]])
        a = Analyzer()
        if a.analyze(text).stats["num_words"] >= 100:
            r = Readability(text)

            readability_score = r.dale_chall().score
        else:
            readability_score = np.nan

        sentiment_score = get_sentiment_score(text)

        curr_article_data.append(length)
        curr_article_data.append(counts[article_id]['shares'])
        curr_article_data.append(num_authors)
        curr_article_data.append(sentiment_score)
        curr_article_data.append(readability_score)
        curr_article_data.append(1)

        data.append(curr_article_data)

    for i, article_id in track(enumerate(DATABASE['articles']['real-articles']['ids']), description="Creating real article data"):
        curr_article_data = []

        length = len(real_titles[i]) + len(real_bodies[i])

        num_authors = len(real_authors[i])

        text = ' '.join([real_bodies[i], real_titles[i]])
        a = Analyzer()
        if a.analyze(text).stats["num_words"] >= 100:
            r = Readability(text)
            readability_score = r.dale_chall().score
        else:
            readability_score = np.nan

        sentiment_score = get_sentiment_score(text)

        curr_article_data.append(length)
        curr_article_data.append(counts[article_id]['shares'])
        curr_article_data.append(num_authors)
        curr_article_data.append(sentiment_score)
        curr_article_data.append(readability_score)
        curr_article_data.append(0)

        data.append(curr_article_data)

    df = pd.DataFrame(data, columns=column_labels)

    return df


def main():
    df = get_dataframe()

    df.to_csv(
        "./algorithm/article_classifier/model_trainer/training_set.csv", index=False)


if __name__ == "__main__":
    main()
