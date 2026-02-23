from celery import Celery
from scraper import Scraper
from parser import Parser
from orm import ORM
import asyncio



celery_app = Celery("scraper", broker="redis://localhost:6379/0", backend="redis://localhost:6379/1")
celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="Europe/Kiev",
    enable_utc=True,
)



@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def worker(self, orm: ORM, parser: Parser, scraper: Scraper, number_of_start_page:int, number_of_pages:int, next_url:str):
    try:
    
        asyncio.run(process_loop(orm, parser, scraper, number_of_start_page, number_of_pages, next_url))
  
    except Exception as exc:
        raise self.retry(exc=exc)


async def process_loop(orm: ORM, parser: Parser, scraper: Scraper, number_of_start_page:int, number_of_pages:int, next_url:str):
    batch_size = 50
    current_page = 0 
    for i in range(number_of_start_page, number_of_pages):
            
            html = await scraper.fetch_page(next_url)
            urls = parser.parse_listing_page(html)

            for url in urls:
                orm.insert("https://auto.ria.com" + url)

            next_url = 'https://auto.ria.com/uk/search/?search_type=2&category=1&abroad=0&customs_cleared=1&page={i}&limit=100'
            current_page += 1

    while True:
        pending_listings = orm.get_pending_listings(batch_size=batch_size)
        if not pending_listings:
            break  

        for car in pending_listings:
            orm.update(car.url, parser.parse_all_info(await scraper.fetch_page(car.url)))