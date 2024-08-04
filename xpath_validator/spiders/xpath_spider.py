import scrapy
from scrapy.http import Request
from xpath_validator.items import XpathValidatorItem


class XpathValidator(scrapy.Spider):
    """"Spider class that scrape the News website to extract the required
    data from the news articles and save it into their respective JSON files"""

    name = 'xpvalid'  # Name of spider

    def start_requests(self):
        """Start requests function to manually select URL from config.py"""
        url_first = "https://www.bendonpub.com/products-sitemap.xml"
        # sending url into the parse function through user agents like chrome, firefox etc
        yield Request(url_first, callback=self.parse, headers={'User-Agent': self.settings.get('USER_AGENT')})


    def parse(self, response):
        """Parse the XML sitemap to extract URLs"""
        self.logger.info(f"Successfully crawled: {response.url}")

        # Print the response body for debugging
        self.logger.debug(response.text)

        # Register namespace based on the XML file's namespace
        namespaces = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

        # Corrected XPath expression to extract loc elements within the namespace
        urls = response.xpath("//ns:url/ns:loc/text()", namespaces=namespaces).getall()

        for each in urls:
            full_url = response.urljoin(each)  # Ensure the URL is absolute
            self.logger.info(f"Found URL: {full_url}")

            # Yield the next request to follow the URL
            yield Request(full_url, callback=self.parse_category)

    def parse_category(self, response):
        """Parse the categorical page"""
        self.logger.info(f"Parsing category page: {response.url}")

        # Example of item extraction
        item = XpathValidatorItem()
        item['web_url'] = response.url
        item['title'] = response.xpath("//div[contains(@class, 'product-content-right')]//h2/text()").get()
        item['image'] = response.xpath("//div[contains(@class, 'slick-track')]//div/@style").get()
        item['short_description'] = response.xpath("//div[contains(@class, 'product-content-right')]//p/text()").get()
        item['specification'] = response.xpath("normalize-space(//div[contains(@class, 'product-content-highlight-details')])").get()
        item['long_specification'] = response.xpath("//div[contains(@class, 'product-content-list-details')]//li/text()").getall()
        # Add more fields to the item as necessary
        yield item