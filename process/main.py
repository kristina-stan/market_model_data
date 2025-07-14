import asyncio
from playwright.async_api import async_playwright
from .core.finder import find_magazine_test
from utils import create_folder_if_not_exists
from .popup_helper import popup_watcher
from .core import to_pages
from .core import testerr

async def main():
    create_folder_if_not_exists(".data/screenshots")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        await context.tracing.start(screenshots=True, snapshots=True, sources=True)
        page = await context.new_page()
        await page.goto("https://www.broshura.bg/i/3")
        watcher_task = asyncio.create_task(popup_watcher(page))

        # get the pdf/screenshots
        await find_magazine_test(page, context)

        #'''
        watcher_task.cancel()
        try:
            await watcher_task
        except asyncio.CancelledError:
            pass
        await browser.close()
        #'''

        # to formated pages
        print("\n\n========== SAVING THE PAGES OF THE PDF-S ==========")
        await to_pages.save_all_pdfs_as_images()


if __name__ == "__main__":
    asyncio.run(main())
