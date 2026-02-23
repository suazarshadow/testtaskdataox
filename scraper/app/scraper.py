import asyncio 
from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright
from ua import getUserAgent


class Scraper:
    async def fetch_page(self, url): 
        async with async_playwright() as p: 
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent=getUserAgent(), 
                viewport={'width': 1200, 'height': 800}
            )
            page = await context.new_page()
            
            response = await page.goto(url)
            if response.status != 200:
                raise Exception("Something went wrong, probably got flaged change IP and try again!!")
            
            try:
                phone_button = page.locator('button.conversion:has-text("XXX")').first
                
                if await phone_button.count() > 0:
                    await phone_button.wait_for(state='visible', timeout=5000)
                    await phone_button.click()
                    await page.locator('a[href^="tel:"]').first.wait_for(state='visible', timeout=5000)
                                  
            except Exception as e:
                pass 

            html = await page.content()
            await browser.close()
            return html
        
    def get_number_of_pages(self, url):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            response = page.goto(url)
            if response.status != 200:
                raise Exception("Something went wrong, probably got flaged change IP and try again!")

            raw_pages = page.evaluate("""
            () => Array.from(document.querySelectorAll("a.link.page-link"))
                .map(el => el.innerText)
                .map(t => t.replace(/\\D/g, ''))
                .filter(t => t && t.length > 0)
            """)

            pages = list(map(int, raw_pages))

            browser.close()

            return pages[-1]



