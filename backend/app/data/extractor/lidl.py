from app.data.extractor.base_grocery_scraper import GroceryScraper
from app.data.model.grocery import CreateGroceryItem, GroceryItem

class LidlScraper(GroceryScraper):
    
    async def extract_specified_content(self, type: str):
        grocery_items = []
        try:
            # TODO: Need to add pagination to the request
            results = self.source['results']
            for result in results:
                db_grocery_item = CreateGroceryItem(
                        name=result["name"],
                        brand=result["brands"][0] if result["brands"] else None,
                        type=type,
                        image=result["images"][0]['url'] if result["images"] else None,
                        link=None,
                        price=result["priceInformation"]['currentPrice']['currentPrice']['value'],
                        uom=result["description"],
                        chain="Lidl",
                        store="US08015", #TODO: Need to pull store from url request
                    )
                item = GroceryItem.model_validate(db_grocery_item)
                grocery_items.append(item)
            self.mapped_groceries = grocery_items
            #print(f"\nLidl Scraped: {self.mapped_groceries}")
        except Exception as e:
            print('Error while extracting/mapping specified content from Lidl api: ', e)
                
    async def process_specified_content(self):
        if self.mapped_groceries:
            await self.save_grocery_items()