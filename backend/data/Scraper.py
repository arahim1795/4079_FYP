from bs4 import BeautifulSoup

from newspaper import Article, Config
import requests
from selenium import webdriver

import os
from tqdm import tqdm
from typing import List
import warnings


class Scraper:
    def __init__(self):
        # newspaper3k
        user_agent = (
            "Mozilla/5.0 (Windows NT 10.0; rv:68.0) Gecko/20100101 Firefox/68.0"
        )
        self.config = Config()
        self.config.browser_user_agent = user_agent

        # driver
        path = os.path.join(os.getcwd() + "\\backend\\utils\\geckodriver.exe")
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")
        self.driver = webdriver.Firefox(executable_path=path, firefox_options=options)

    def _download_article(self, url: str) -> tuple:
        data = None

        try:
            article = Article(url, config=self.config)
            article.download()
            article.parse()
        except Exception as e:
            print(e)

        if article.url and article.title and article.text and article.authors:
            data = (str(article.url), str(article.title), str(article.text), str(article.authors[0]))

        return data

    def _extract_new_articles(self, base_url: str, soup, stored_articles: List[str]):
        links = []
        if "fool.com" in base_url:
            links = set(
                [
                    "https://www.fool.com" + str(link["href"])
                    for link in soup.find_all("a", href=True)
                    if "/investing/2" in link["href"]
                ]
            )
        elif "seekingalpha.com" in base_url:
            links = set(
                [
                    "https://seekingalpha.com" + str(link["href"])
                    for link in soup.find_all("a", href=True)
                    if "/news" in link["href"]
                ]
            )
        else:
            warnings.warn("URL not supported")

        if links:
            links = [link for link in links if link not in stored_articles]

        return links

    def quit_driver(self):
        self.driver.quit()
        self.driver = None

    def scrape(self, db, base_url: str, require_driver=False):
        query = "INSERT INTO articles.article (url, title, content, author) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING"

        stored_articles = db.read("SELECT url FROM articles.article")
        stored_articles = [article[0] for article in stored_articles]

        for i in tqdm(range(0, 5)):
            form_url = base_url + str(i + 1)

            if require_driver:
                # execute driver
                self.driver.get(base_url)
                html = self.driver.page_source
            else:
                form_url = base_url + str(1)
                html = requests.get(form_url).text

            soup = BeautifulSoup(html, features="lxml")

            links = self._extract_new_articles(base_url, soup, stored_articles)

            for link in links:
                parsed_article = self._download_article(link)
                if parsed_article:
                    db.write(query, parsed_article)
