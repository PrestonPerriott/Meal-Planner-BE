from backend.app.data.extractor.base_grocery_scraper import GroceryScraper
from backend.app.data.model.grocery import CreateGroceryItem, GroceryItem
import requests
import json
from aiohttp import ClientSession
import asyncio

class FoodBazaarScraper(GroceryScraper):
    """_summary_
        Since the FoodBazaar endpoint doesn't have '/api' w/i the string,
        it will headless load the webpage and capture the ensuing requests - self.session_requests
    Args:
        GroceryScraper (_type_): _description_
    """
    async def extract_specified_content(self):
        grocery_items = []
        #for req in self.session_requests:
        #    print(f'\n{req.headers}')
        bazaar_graphql = filter(lambda url: 'shop.foodbazaar.com/graphql?operationName=Items' in url, 
                                self.session_requests)
        async with ClientSession() as session:
            tasks = []
            for graph_url in bazaar_graphql:
                tasks.append(session.get(graph_url))
            responses = await asyncio.gather(*tasks)
            
        try:
            for res in responses:
                bazaar_res = json.loads(await res.text())
                bazaar_items = bazaar_res['data']['items']
            for result in bazaar_items:
                print(f"\nFood Bazaar Result: {result}\n")
                db_grocery_item = CreateGroceryItem(
                        name=result.get("name"),
                        brand=result.get("brandName"),
                        image=(result.get("viewSection") or {}).get('itemImage', {}).get('url'),
                        link=(result.get('evergreenUrl') or None),
                        price=(result.get('price') or {}).get('viewSection', {}).get('itemDetails', {}).get('priceString'),
                        uom=(result.get("size") or None),
                        chain="Food Bazaar",
                        store="22961", #TODO: Need to pull store from bazaar_graphql var 
                    )
                item = GroceryItem.model_validate(db_grocery_item)
                grocery_items.append(item)
            self.mapped_groceries = grocery_items
            #print(f"\nFood Bazaar Scraped: {self.mapped_groceries}")
        except Exception as e:
            print('Error while extracting/mapping specified content from Food Bazaar api: ', e)
          
    async def process_specified_content(self):
        if self.mapped_groceries:
           await self.save_grocery_items()
 