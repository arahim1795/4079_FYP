from bs4 import BeautifulSoup
from newspaper import Article
import requests
import time
from tqdm import tqdm

import db


def download_article(url):
    article = Article(url)
    article.download()
    article.parse()
    return (article.url, article.title, article.text, article.authors[0])


def scrape():
    con, cur = db.db_connect()

    base_url = "https://www.fool.com/investing-news/?page="

    for i in tqdm(range(251, 501)):

        specified_url = base_url + str(i)

        html = requests.get(specified_url)
        soup = BeautifulSoup(html.text)

        articles = set(["https://www.fool.com" + str(link['href']) for link in soup.find_all("a", href=True) if "/investing/2" in link['href']])

        cur.execute("SELECT url FROM articles.article")
        scanned = [url[0] for url in cur.fetchall()]

        for article in articles:
            if article not in scanned:
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

                # time.sleep(1)

    db.db_disconnect(con)


scrape()
