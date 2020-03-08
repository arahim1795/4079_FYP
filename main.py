# from spacy.lang.en import English
# from spacy.pipeline import Sentencizer
# from spacy.tokenizer import Tokenizer
# from textblob import TextBlob
# from textblob.classifiers import NaiveBayesClassifier
# from textblob.sentiments import NaiveBayesAnalyzer
# import numpy

import annotator as an
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


articles = db_handler.read(
    "SELECT content FROM articles.article WHERE url LIKE '%fool.com%';"
)
articles = [article[0] for article in articles][:10]

annotate = an.Annotator(db)

annotate._unannotated_csv_export(articles, "annotated_data")
