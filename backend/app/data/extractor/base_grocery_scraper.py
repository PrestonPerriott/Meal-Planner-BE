from seleniumwire import webdriver
import requests
import json
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from abc import ABC, abstractmethod
import time
from sqlmodel import Session
from aiohttp import ClientSession
class GroceryScraper(ABC):
    def __init__(self, url: str, parser: str = "lxml", wait: float = 4.0, db_session: Session = None):
        self.url = url
        self.parser = parser
        self.wait = wait
        self.db_session = db_session
        self.session_requests = []
        self.agent = "Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 640 XL LTE) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Mobile Safari/537.36 Edge/12.10166"
        #self.agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:133.0) Gecko/20100101 Firefox/133.0"
        self.is_api = True if 'api' in self.url else False

        self.soup = None
        self.links = None
        self.page_images = []
        self.source = None
        self.mapped_groceries = None
        self.available_pages = None
              
        # if not self.is_api:
        #     # TODO: Need to decouple __set_soup_content from init
        #     # Without self.source set, __set_soup_content cannot set a BeautifulSoup object
        #     self.soup = self.__set_soup_content()
        #     self.links = self.__process_links()
        #     self.page_images = []
        # else:
        #     self.soup = None
        #     self.links = None
        #     pass
        
    async def set_source(self):
        if self.is_api:
            try: 
                async with ClientSession() as session:
                    response = await session.get(self.url)
                    self.source = json.loads(await response.text())
                    return
            except Exception as e:
                print('Request Error - Could not get api source: ', e)
              
        try: 
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            options.add_argument(f'--user-agent={self.agent}')
            
            driver = webdriver.Chrome(options=options)
            driver.get(self.url)
            driver.implicitly_wait(self.wait)
            time.sleep(self.wait) # Bad practice, shoudl wait for specific elements
            for req in driver.requests:
                if req.response:
                    self.session_requests.append(req.url)
            
            #wait = WebDriverWait(driver=driver, timeout=self.wait)
            #wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.w-pie--product-tile:nth-child(2) > a:nth-child(1) > div:nth-child(2) > span:nth-child(3)')))
    
            self.source = driver.page_source
            self.soup = self.__set_soup_content()
            self.links = self.__process_links()
            self.page_images = []
            return
        except Exception as e:
            print('Web Driver Error - Could not get page source: ', e)
            
    def __set_soup_content(self) -> BeautifulSoup:
        return BeautifulSoup(self.source, self.parser)

    def __process_links(self) -> dict:
        links = {}
        for link in (urls := self.soup.find_all('a', href=True)):
            try:
                links[link.text] = urljoin(self.url, link['href'])
            except Exception as e:
                print('Error while mapping page links')
                continue
        return links
    
    def remove_tags(self, tags: list = []):
        if self.is_api:
            raise TypeError('Cannot call remove tags with Scraper type of API')
        
        tags_to_remove = ['script', 'style']
        tags_to_remove.extend(tags)
        tags_to_remove = list(set(tags_to_remove))
        for tag in self.soup.find_all(tags_to_remove):
            try:
                tag.extract()
            except Exception as e:
                print('Error removing tag: ', e)
                continue
    
    #TODO: Figure out a better way to get the associated iamges with the food item
    def process_images(self, save_images:bool = False, image_types_to_remove: list = []):
        if self.is_api:
            raise TypeError('Cannot call remove tags with Scraper type of API')
    
        image_types = ['.svg', '.gif']
        image_types.extend(image_types_to_remove)
        image_types = list(set(image_types))
        for image in (images := self.soup.find_all('img')):
            try:
                if not save_images:
                    image.replace_with('')
                else:
                    image_link = image.get('src')
                    replaced = False
                    if type(image_link) == str:
                        for image_type in image_types:
                            if not replaced and image_type in image_link:
                                image.replace_with('')
                                replaced = True
                    if not replaced:
                        image.replace_with(urljoin(self.url, image_link))
                        self.page_images.append(image)                    
            except Exception as e:
                print('Error getting image link: ', e)
                continue
    
    async def save_grocery_items(self):
        print("Attempting to save grocery items")
        if not self.db_session or not self.mapped_groceries:
            raise ValueError('Cannot save grocery items without a db session or mapped groceries')
        
        try:
            for item in self.mapped_groceries:
                print(f"Saving grocery item: {item}")
                self.db_session.add(item)
            await self.db_session.commit()
        except Exception as e:
            print('Error while saving grocery items: ', e)
    
    @abstractmethod
    async def extract_specified_content(self):
       pass
    
    @abstractmethod
    async def process_specified_content(self):
        pass          
     