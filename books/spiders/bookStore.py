import scrapy
from ..items import BooksItem

class BookstoreSpider(scrapy.Spider):
    name = 'bookStore'
    page_number = 2
    start_urls = ['http://books.toscrape.com/catalogue/page-1.html']

    def parse(self, response, **kwargs):
        items = BooksItem()
        all_books = response.css("li article.product_pod")

        for book in all_books:
            title = book.css("h3 a::attr(title)")[0].extract()
            rating = book.css('p.star-rating::attr(class)').extract_first().replace('star-rating', '').strip()
            price = "£" + book.css(".price_color::text").extract_first().replace("£", "")
            imagelink = "http://books.toscrape.com/" + book.css(".thumbnail::attr(src)")[0].extract()

            items["title"] = title
            items["rating"] = rating
            items["price"] = price
            items["imagelink"] = imagelink

            yield items

        next_page = response.css("li.next a::attr(href)").extract_first()
        if next_page is not None:
            url = 'http://books.toscrape.com/catalogue/' + next_page
            yield response.follow(url, callback=self.parse)
