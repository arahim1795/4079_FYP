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


# X DEV X
# newly_annotated = []
# for sentence in segmented_text:
#     newly_annotated.append([sentence])

# with open("./data/auto_annotated.csv", "w", newline="") as csvfile:
#     csv_writer = csv.writer(csvfile)
#     csv_writer.writerows(newly_annotated)
# X DEV X


def main():
    # init
    db_handler = db.Db()
    annotator_instance = an.Annotator()

    # core
    # 1: scrape
    # 2: annotate
    # 3: evaluate

    # 1
    # TODO copy scraper

    # 2
    articles = db_handler.read(
        "SELECT content FROM articles.article WHERE url LIKE '%fool.com%';"
    )
    articles = [article[0] for article in articles][10:20]

    annotator_instance.automatic_annotation(articles, "auto_annotated")

    # 3
    # TODO evaluator


if __name__ == "__main__":
    main()
