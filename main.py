import os
import asyncio
from twisted.internet import asyncioreactor

# Set the event loop policy to use SelectorEventLoop on Windows
if os.name == 'nt':
    policy = asyncio.WindowsSelectorEventLoopPolicy()
    asyncio.set_event_loop_policy(policy)

# Install the asyncio reactor
asyncioreactor.install()

from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from xpath_validator.spiders.xpath_spider import XpathValidator

def main():
    configure_logging()
    settings = get_project_settings()
    runner = CrawlerRunner(settings=settings)

    async def run_spider():
        # Run the spider and wait for it to complete
        await runner.crawl(XpathValidator)

    async def main_crawl():
        await run_spider()
        # Stop the reactor after the spider completes
        reactor.stop()

    # Ensure the reactor is stopped cleanly
    asyncio.ensure_future(main_crawl())
    reactor.run()

if __name__ == '__main__':
    main()
