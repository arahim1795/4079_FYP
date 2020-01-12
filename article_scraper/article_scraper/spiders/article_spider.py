import scrapy


class ArticleSpider(scrapy.Spider):
    name = "tutorial"

    # start_urls: (list) URLs to scrape
    start_urls = ["http://quotes.toscrape.com/"]

    # parse: Scrapy function
    def parse(self, response):
        # css selector: (list)
        # select subtag under tag: <parent_tag> <child_tag>
        # list access: .css(...)[X]
        # refined access:  tag .(class) or #(id)
        # functions: extract(), extract_first()
        title = response.css("title::text").extract()

        # xpath selector: (list)
        # format: response.xpath("//tag").extract
        # select tag: //<tag>
        # select class within tag: [@class='<value>']
        # select id within tag: [@id='<value>']
        # select text: /text()
        # list access: .xpath(...)[X]

        # can mix css and xpath

        # non-blocking return
        yield {"title_text": title}
