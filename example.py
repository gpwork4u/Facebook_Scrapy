from scrapy.crawler import CrawlerProcess
from facebook_scrapy.spiders.facebook import facebook
process = CrawlerProcess(settings={
    "FEEDS": {
        "items.json": {"format": "json"},
    },
})
process.crawl(facebook)
process.start()