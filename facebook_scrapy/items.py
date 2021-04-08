# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PostItem(scrapy.Item):
    id = scrapy.Field()
    author = scrapy.Field()
    content = scrapy.Field()
    time = scrapy.Field()
    images = scrapy.Field()
    post_url = scrapy.Field()
