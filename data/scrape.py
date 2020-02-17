import newspaper
from newspaper import Article
import time

import db


def download_article(url):
    article = Article(url)
    article.download()
    article.parse()
    return (article.url, article.title, article.text, article.authors[0])


def scrape():
    con, cur = db.db_connect()

    cur.execute("SELECT * FROM articles.links")
    source_urls = [url[0] for url in cur.fetchall()]

    for source in source_urls:
        paper = newspaper.build(source, language="en", memoize_articles=False)

        articles = [s.url for s in paper.articles if "/investing" in s.url]

        for article in articles:
            try:
                parsed_article = download_article(article)

                query = """
                    INSERT INTO articles.article(url, title, content, author) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING
                """
                data = parsed_article

                cur.execute(query, data)
                con.commit()
            except Exception as e:
                print(e)
                print("Failed: " + article)
                continue

            time.sleep(1)

    db.db_disconnect(con)


scrape()
