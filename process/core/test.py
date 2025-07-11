import asyncio

from playwright.async_api import async_playwright

from process.popup_helper import popup_watcher


async def test():

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        await context.tracing.start(screenshots=True, snapshots=True, sources=True)
        page = await context.new_page()
        await page.goto("https://www.broshura.bg/b/5536511#page-1")
        watcher_task = asyncio.create_task(popup_watcher(page))

        #print(f"Current URL: {page.url}")
        await page.wait_for_load_state('networkidle')
        url_selector = await page.wait_for_selector("div.component-pageflip")
        success = False
        if url_selector:
            print(f"FOUND supermarket site link!")
            href = await url_selector.get_attribute('data-back-url')
            print(href)
            success = True

        watcher_task.cancel()
        try:
            await watcher_task
        except asyncio.CancelledError:
            pass
        await browser.close()

if __name__ == "__main__":
    asyncio.run(test())