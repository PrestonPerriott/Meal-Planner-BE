import os 
import logging
from datetime import datetime
from time import sleep
from app.core.config import settings
import concurrent.futures
import asyncio
from functools import wraps
from ratelimit import limits, sleep_and_retry
from tenacity import retry, stop_after_attempt, wait_exponential
from sqlmodel import Session
from app.core.db import get_db_session
from app.data.extractor.base_grocery_scraper import GroceryScraper
from app.data.extractor.trader_joes import TraderJoesScraper
from app.data.extractor.whole_foods import WholeFoodsScraper
from app.data.extractor.food_bazaar import FoodBazaarScraper
from app.data.extractor.lidl import LidlScraper

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# Rate limiting decorators w/ 60 calls per minute for each store
@sleep_and_retry
@limits(calls=10, period=60)
def rate_limited_call():
    """Rate limiting placeholder for the scraper"""
    pass

# Retry decorator w/ exponential backoff
def with_retry(max_attempts=3):
    return retry(
        stop=stop_after_attempt(max_attempts), 
        wait=wait_exponential(multiplier=1, min=4, max=30),
        reraise=True
    )

class GrocerySeedService:
    def __init__(self):
        self.basic_groceries = [item.strip() for item in settings.BASIC_GROCERIES.split(',')]
        
        # Base URLs
        self.tjs_base_url = settings.BASE_TRADER_JOES
        self.tj_append_url = settings.APPEND_TRADER_JOES
        
        self.wf_url = settings.BASE_WHOLEFOODS
        self.wf_append_url = settings.APPEND_WHOLEFOODS
                
        self.lidl_url = settings.BASE_LIDL
        self.lidl_append_url = settings.APPEND_LIDL
        
        self.fb_url = settings.BASE_FOODBAZAAR
        
        # Max workers for parallel scraping
        self.max_workers = 4
        
        self.rate_limits = {
            'trader_joes': 60,
            'whole_foods': 60,
            'food_bazaar': 30,
            'lidl': 60,
        }
    
    def _construct_urls(self, item: str):
        """Constructs the URL for the given food item and append URL"""
        return {
            'trader_joes': f"{self.tjs_base_url}{item}{self.tj_append_url}",
            'whole_foods': f"{self.wf_url}{item}{self.wf_append_url}",
            'food_bazaar': f"{self.fb_url}{item}",
            'lidl': f"{self.lidl_url}{item}{self.lidl_append_url}",
        }
    
    def get_scraper(self, store: str, url: str, db: Session) -> GroceryScraper:
        """Factory method to create scrapers with DB session"""
        scrapers = {
            'trader_joes': lambda: TraderJoesScraper(url=url, db_session=db),
            'whole_foods': lambda: WholeFoodsScraper(url=url, db_session=db),
            'food_bazaar': lambda: FoodBazaarScraper(url=url, db_session=db),
            'lidl': lambda: LidlScraper(url=url, db_session=db),
        }
        return scrapers[store]()
        
    @with_retry()
    async def _scrape_store(self, store: str, url: str, item: str, db: Session) -> None:
        """Scrape a single store with retry logic"""
        try:
            # Apply rate limiting
            rate_limited_call()
            print(f"\nScraping {item} from {store} at url: {url}")
            scraper = self.get_scraper(store, url, db)
            await scraper.set_source()
            await scraper.extract_specified_content(type=item)
            await scraper.process_specified_content()
        except Exception as e:
            print(f"Error scraping {item} from {store}: {e}\n")
            raise # Reraise the exception to be handled by the retry decorator
            
            
    async def scrape_item(self, item: str) -> None:
        """Scrapes the given food item from all the grocery stores"""
        urls = self._construct_urls(item)
        tasks = [] # tasks to be run in parallel
        for store, url in urls.items():
            tasks.append((store, url, item))
        
        async def process_task(store, url, item):
            db = get_db_session()
            try:
                await self._scrape_store(store, url, item, db)
            finally:
                db.close()
        
        await asyncio.gather(
            *[process_task(store, url, item) for store, url, item in tasks],
            return_exceptions=True
            )
        
        # Use ThreadPoolExecutor to run tasks in parallel
        # with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
        #     # Create new DB session for each worker
        #     futures = []
        #     for store, url, item in tasks:
        #         db = get_db_session()
        #         future = executor.submit(self._scrape_store, store, url, item, db)
        #         futures.append((future, store, db))
                
        #     # Handle completed tasks
        #     for future, store, db in futures:
        #         try:
        #             future.result()
        #         except Exception as e:
        #             print(f"Error scraping {item} from {store}: {e}")
        #         finally:
        #             db.close()
    
    async def run_weekly_scrape(self) -> None:
        """Run a complete scrape of all items"""
        print(f"Starting weekly scraper at {datetime.now()}")
        
        for item in self.basic_groceries:
            await self.scrape_item(item)
            # Sleep for 2 seconds to avoid rate limiting
            await asyncio.sleep(1)
            
        print(f"Weekly scraper completed at {datetime.now()}")
