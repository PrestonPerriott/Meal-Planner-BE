import schedule
import time
import asyncio
from app.data.loader.grocery_seed import GrocerySeedService

# async def job():
#     grocery_seed = GrocerySeedService()
#     await grocery_seed.run_weekly_scrape()

async def main():
    # Schedule the job to run every Monday at 1:00 am
    # schedule.every().tuesday.at("00:32").do(job)
    # Keep the script running
    #while True:
    #    schedule.run_pending()
    grocery_seed = GrocerySeedService()
    await grocery_seed.run_weekly_scrape()
    
if __name__ == "__main__":
    asyncio.run(main())