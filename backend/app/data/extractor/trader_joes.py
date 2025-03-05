from backend.app.data.extractor.base_grocery_scraper import GroceryScraper
from backend.app.data.model.grocery import CreateGroceryItem, GroceryItem

class TraderJoesScraper(GroceryScraper):
    
    async def extract_specified_content(self):
        grocery_items = []
        try:
            food_items = self.soup.find_all('article', 'SearchResultCard_searchResultCard__3V-_h')
            for item in food_items:
                item_link = item.find('a', class_="Link_link__1AZfr SearchResultCard_searchResultCard__titleLink__2nz6x")['href']
                item_name = item.find('a', class_="Link_link__1AZfr SearchResultCard_searchResultCard__titleLink__2nz6x").text.strip()

            # Extract the srcset
                srcset = [source['srcset'].strip() for source in item.find_all('source')]

            # Extract the price and unit
                raw_price = item.find('span', class_="ProductPrice_productPrice__price__3-50j").text.strip()
                price = float(raw_price.split('$')[1])
                unit = item.find('span', class_="ProductPrice_productPrice__unit__2jvkA").text.strip()
                db_grocery_item = CreateGroceryItem(
                        name=item_name,
                        brand="Trader Joes Brand",
                        image=srcset[0],
                        link=item_link,
                        price=price,
                        uom=unit,
                        chain="Trader Joes",
                        store="Brooklyn", # TODO: Need to extract store number from GraphQL API
                    )
                item = GroceryItem.model_validate(db_grocery_item)
                grocery_items.append(item)
            self.mapped_groceries = grocery_items
            #print(f"\nTrader Joes Scraped: {self.mapped_groceries}")
        except Exception as e:
            print('Error while extracting specified content from string: ', e)
    
    async def process_specified_content(self):
        if self.mapped_groceries:
            await self.save_grocery_items()
  