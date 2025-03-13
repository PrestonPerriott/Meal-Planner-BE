from app.data.extractor.base_grocery_scraper import GroceryScraper
from app.data.model.grocery import CreateGroceryItem, GroceryItem

class WholeFoodsScraper(GroceryScraper):
    
    async def extract_specified_content(self):
        grocery_items = []
        try:  
            results = self.source['results']
            for result in results:
                print(f"\nWhole Foods Result: {result}\n")
                db_grocery_item = CreateGroceryItem(
                        name=result.get("name"),
                        brand=result.get("brand"),
                        image=result.get("imageThumbnail"),
                        link=result.get("slug"),
                        price=result.get("regularPrice"),
                        uom=result.get("uom", None),
                        chain="Whole Foods",
                        store=f"{result['store']}",
                    )
                item = GroceryItem.model_validate(db_grocery_item)
                grocery_items.append(item)
            self.mapped_groceries = grocery_items
            #print(f"\nWhole Foods Scraped: {self.mapped_groceries}")
        except Exception as e:
            print('Error while extracting/mapping specified content from Whole foods api: ', e)
        
    async def process_specified_content(self):
         if self.mapped_groceries:
            await self.save_grocery_items()
    