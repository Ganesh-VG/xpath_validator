# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class XpathValidatorItem(scrapy.Item):
    web_url = scrapy.Field()
    title = scrapy.Field()
    image = scrapy.Field()
    short_description = scrapy.Field()
    specification = scrapy.Field()
    long_specification = scrapy.Field()
