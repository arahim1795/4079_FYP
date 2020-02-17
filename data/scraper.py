# %%
from bs4 import BeautifulSoup
from newspaper import Article
import requests
from tqdm import tqdm

import db


def download_article(url: str):
    try:
        article = Article(url)
        article.download()
        article.parse()
    except Exception as e:
        print(e)

    if article.url and article.title and article.text and article.authors:
        return (article.url, article.title, article.text, article.authors[0])

    return None


url = "https://seekingalpha.com/news/3542453-severe-worker-shortage-u-s-factories-in-china"

print(download_article(url))

# %%


def scrape(db):

    base_urls = ["https://www.fool.com/investing-news/?page="]

    for base_url in base_urls:
        # handler: fool.com
        if "fool.com" in base_url:
            for i in tqdm(range(1, 5)):

                return_data = db.execute("SELECT url FROM articles.article", None, True)
                stored_articles = [url[0] for url in return_data]

                url = base_url + str(i)

                html = requests.get(url)
                soup = BeautifulSoup(html.text)

                links = set(
                    [
                        "https://www.fool.com" + str(link["href"])
                        for link in soup.find_all("a", href=True)
                        if "/investing/2" in link["href"]
                    ]
                )

                links = [link for link in links if link not in stored_articles]

                query = """
                            INSERT INTO articles.article(url, title, content, author) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING
                        """

                for link in links:
                    parsed_article = download_article(link)

                    db.execute(query, parsed_article)


database = db.Db()
scrape(database)
