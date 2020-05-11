from backend.Annotator import Annotator
from backend.Evaluator import Evaluator
from backend.data.Database import Database
from backend.data.Scraper import Scraper
import csv
from textblob.classifiers import NaiveBayesClassifier


def main():
    # init
    db_handler = Database()
    scraper = Scraper()
    annotator_instance = Annotator()
    evaluator = Evaluator()

    # 1: scrape
    base_urls = db_handler.read("SELECT url FROM articles.source;")
    base_urls = [base_url[0] for base_url in base_urls]
    for base_url in base_urls:
        if "seekingalpha.com" in base_url:
            scraper.scrape(db_handler, base_url, True)
        else:
            scraper.scrape(db_handler, base_url)
    scraper.quit_driver()

    # 2: annotate
    articles = db_handler.read(
        "SELECT content FROM articles.article WHERE url LIKE '%fool.com%';"
    )
    articles = [article[0] for article in articles]

    # run either

    # - manual (either)
    # -- internal annotation
    # annotator_instance.manual_annotation(articles[:50], "auto_annotated")
    # -- csv export
    annotator_instance.unannotated_csv_export(articles[:50], "auto_annotated")

    # - automatic
    # annotator_instance.automatic_annotation(articles, "auto_annotated")

    # 3: evaluate
    model_file = "auto_annotated"

    data = None
    with open("./backend/data/" + model_file + ".csv", "r") as csvfile:
        data = list(csv.reader(csvfile))

    data = [tuple((datum[0], datum[1])) for datum in data]
    classifier = NaiveBayesClassifier(data)

    for i in range(6, 11):
        evaluator.evaluate_0("article_" + str(i), classifier)


if __name__ == "__main__":
    main()
