# from spacy.lang.en import English
# from spacy.pipeline import Sentencizer
# from spacy.tokenizer import Tokenizer
# from textblob import TextBlob
# from textblob.classifiers import NaiveBayesClassifier
# from textblob.sentiments import NaiveBayesAnalyzer

# import json
# import numpy
from nltk.corpus import stopwords
import re
import spacy
from typing import List

# import annotator as an
import data.db as db

# import data.scraper as sc

# initialisation
db_handler = db.Db()

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


def paragrapher(article: str) -> List[str]:
    paragprahs = list(filter(None, article.split("\n")))
    paragraphs = [paragpraph.strip() for paragpraph in paragprahs]

    return paragraphs


def pre_cleanse_text(text: str) -> str:
    # init
    # # TODO: More Stocker Tickers
    # tickers = ["OTC", "NASDAQ", "NYSE"]
    # ticker_patterns = ["\\(" + ticker + ":.+?\\)" for ticker in tickers]

    # # core
    # for pattern in ticker_patterns:
    #     text = re.sub(pattern, "", text)

    generic_patterns = [
        ["\\(.+?:.+?\\)", ""],
        ["\\.\\.\\.", ""],
        ["\\([\\w+, !\\?]+\\)", ""],
        ["  ", " "],
        [" \\.", "."],
        [" ,", ","],
        ["^\\d\\. ", ""],
        ["U\\.S\\.", "United States"],
        ["\\.+\\?", ""],
        ['"', ""],
        ["\\b\\w+n't\\b", "not"],
    ]
    for pattern in generic_patterns:
        text = re.sub(pattern[0], pattern[1], text)

    stop_words = stopwords.words("english")
    wanted_stopwords = [
        "above",
        "after",
        "against",
        "before",
        "below",
        "but",
        "down",
        "less",
        "more",
        "most",
        "no",
        "nor",
        "not",
        "off",
        "only",
        "under",
        "until",
        "too",
        "up",
    ]
    stop_words = [e for e in stop_words if e not in wanted_stopwords]

    text = [word for word in text.split() if word.lower() not in stop_words]
    text[0] = text[0].capitalize()
    text = " ".join(word for word in text).replace(" - - ", "--").replace(" - ", "-")

    stopword_pattern = ["[Hh]ere", "[TtWw]hat", "[Tt]here"]
    stopword_pattern = ["\\b" + pattern + "'s\\b" for pattern in stopword_pattern]
    stopword_pattern += ["\\b\\w+'ll\\b", "\\b[Ii]'ve\\b"]
    for pattern in stopword_pattern:
        text = re.sub(pattern, "", text)

    text = text.replace("  ", " ")

    return text.strip()


def sentence_segmentor(text: str, spacy_model) -> list:
    # init
    segmented = []

    # core
    # TODO: More NLP sentence segmentation libraries
    # - spaCy
    segmented += [sentence.text.strip() for sentence in spacy_model(text).sents]

    return segmented


def post_cleanse_text(text: str) -> str:
    generic_patterns = [[".+\\?", ""], [".+vs\\..+", ""], [".*[Ll]et's.*", ""]]
    for pattern in generic_patterns:
        text = re.sub(pattern[0], pattern[1], text)

    return text


articles = db_handler.read(
    "SELECT content FROM articles.article WHERE url LIKE '%fool.com%';"
)
articles = [article[0] for article in articles][:10]

# FLOW
# 1: Basic Paragraphing
# 2: Cleanse Text
# 3: Segment into Sentences via NLP

# 1
paragraphed_text = []
for article in articles:
    paragraphed_text += paragrapher(article)

with open("./data/texts_orig.txt", "w", encoding="UTF-8") as f:
    for text in paragraphed_text:
        f.write(text + "\n")

# 2
paragraphed_text = [pre_cleanse_text(paragraph) for paragraph in paragraphed_text]

with open("./data/texts_ori.txt", "w", encoding="UTF-8") as f:
    for text in paragraphed_text:
        f.write(text + "\n")

# 3
segmented_text = []
spacy_nlp = spacy.load("en_core_web_lg")
for paragraph in paragraphed_text:
    segmented_text += sentence_segmentor(paragraph, spacy_nlp)

segmented_text = [post_cleanse_text(sentence) for sentence in segmented_text]
segmented_text = list(filter(None, segmented_text))


with open("./data/texts.txt", "w", encoding="UTF-8") as f:
    for sentence in segmented_text:
        f.write(sentence + "\n")
