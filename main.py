import csv

# from spacy.lang.en import English
# from spacy.pipeline import Sentencizer
# from spacy.tokenizer import Tokenizer
import multiprocessing as mp
import numpy
from sklearn.utils import gen_even_slices
from textblob import TextBlob

# from textblob.classifiers import NaiveBayesClassifier
from textblob.sentiments import NaiveBayesAnalyzer, PatternAnalyzer
from tqdm import tqdm


import annotator as an
import data.db as db

# import data.scraper as sc

# initialisation
# db_handler = db.Db()

# # run scraper on launch
# base_urls = db_handler.read("SELECT url FROM articles.source;")
# base_urls = [base_url[0] for base_url in base_urls]
# scraper = sc.Scraper(db_handler)
# for base_url in base_urls:
#     if "seekingalpha.com" in base_url:
#         scraper.scrape(base_url, True)
#     else:
#         scraper.scrape(base_url)
# scraper.quit_driver()

# annotator = an.Annotator(db_handler)


# articles = db_handler.read(
#     "SELECT content FROM articles.article WHERE url LIKE '%fool.com%';"
# )
# articles = [article[0] for article in articles][:10]

# annotate = an.Annotator(db)

# annotate._unannotated_csv_export(articles, "manual_annotated")

# TODO Implement Textblob Sentiment Analyser

# core
# 1: Basic Paragraphing
# 2: Pre Cleanse Text
# 3: Segment into Sentences via NLP
# 4: Post Cleanse Text
# 5: Lemmatise Text
# 6: Annotate Text

# # 1
# paragraphed_text = []
# for article in articles:
#     paragraphed_text += annotate._paragrapher(article)

# # 2
# paragraphed_text = [
#     annotate._pre_cleanse_text(paragraph) for paragraph in paragraphed_text
# ]

# # 3
# segmented_text = []
# for paragraph in paragraphed_text:
#     segmented_text += annotate._sentence_segmentor(paragraph)

# # 4
# segmented_text = [
#     annotate._post_cleanse_text(sentence) for sentence in segmented_text
# ]
# segmented_text = list(filter(None, segmented_text))

# # 5
# segmented_text = [
#     annotate._lemmatise_sentence(sentence) for sentence in segmented_text
# ]

# X DEV X
# newly_annotated = []
# for sentence in segmented_text:
#     newly_annotated.append([sentence])

# with open("./data/auto_annotated.csv", "w", newline="") as csvfile:
#     csv_writer = csv.writer(csvfile)
#     csv_writer.writerows(newly_annotated)
# X DEV X


def auto(data, blob):
    blobbed = []

    for i in tqdm(range(len(data))):
        blobbed.append([data[i][0], blob[i].sentiment.classification])

    return blobbed


def main():
    # setup multiprocessing
    num_threads = mp.cpu_count() - 2
    p = mp.Pool(processes=num_threads)

    data = []
    with open("./data/auto_annotated.csv", "r") as csvfile:
        data = list(csv.reader(csvfile))

    data_textblob = [
        TextBlob(datum[0], analyzer=NaiveBayesAnalyzer()) for datum in data
    ]

    slices = list(gen_even_slices(len(data), num_threads))

    sliced_data = []
    sliced_textblob = []

    for s in slices:
        sliced_data.append(data[s])
        sliced_textblob.append(data_textblob[s])

    dataset = p.starmap(auto, zip(sliced_data, sliced_textblob))

    print(dataset)

    # annotated = []
    # for i in tqdm(range(len(data))):
    #     annotated.append([data[i][0], data_textblob[i].sentiment.classification])


# with open("./data/auto_annonated.csv", "w", newline="") as csvfile:
#     csv_writer = csv.writer(csvfile)
#     csv_writer.writerows(data)

# print(data_textblob[0].sentiment.classification)

if __name__ == "__main__":
    main()
