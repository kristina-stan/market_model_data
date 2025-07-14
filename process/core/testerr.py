import asyncio

from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright

async def get_image_urls():
    page_url = 'https://www.broshura.bg/b/5542394#page-1'

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(page_url)

        # Select the img element and get its 'src' and 'srcset' attributes
        img_src = page.eval_on_selector('img', 'el => el.getAttribute("src")')
        img_srcset = page.eval_on_selector('img', 'el => el.getAttribute("srcset")')
        print("SRC:", img_src)
        print("SRCSET:", img_srcset)

        await browser.close()
