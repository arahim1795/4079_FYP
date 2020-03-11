import annotator as an
import data.db as db
import data.scraper as sc


def main():
    # init
    db_handler = db.Db()
    annotator_instance = an.Annotator()
    # scraper = sc.Scraper(db_handler)

    # core
    # 1: scrape
    # 2: annotate
    # 3: evaluate

    # 1
    base_urls = db_handler.read("SELECT url FROM articles.source;")
    # base_urls = [base_url[0] for base_url in base_urls]
    # for base_url in base_urls:
    #     if "seekingalpha.com" in base_url:
    #         scraper.scrape(base_url, True)
    #     else:
    #         scraper.scrape(base_url)
    # scraper.quit_driver()

    # 2
    # TODO Complete Analysis of All Articles
    articles = db_handler.read(
        "SELECT content FROM articles.article WHERE url LIKE '%fool.com%';"
    )
    articles = [article[0] for article in articles][50:60]

    annotator_instance.automatic_annotation(articles, "auto_annotated")
    # annotator_instance._unannotated_csv_export(articles, "auto_annotated")

    # 3
    # TODO evaluator


if __name__ == "__main__":
    main()
