from web_scraper import *
import asyncio

async def main():
    while True:
        await character_scrape()
        print("Do you want to check another character? (yes/no)")
        user_input = input().lower()
        if user_input != 'yes':
            break
        
asyncio.run(main())