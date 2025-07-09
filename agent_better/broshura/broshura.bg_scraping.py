import asyncio, os, re
from playwright.async_api import TimeoutError

from playwright.async_api import async_playwright, expect
from sqlalchemy.util import await_only

os.makedirs("screenshots", exist_ok=True)
async def test_cookie_accept(page):
    try:
        await page.wait_for_selector("div#cookiescript_buttons", timeout=5000)  # wait max 5 sec
        accept_button = page.locator('div#cookiescript_accept')
        if await accept_button.is_visible():
            await accept_button.click(timeout=5000, delay=200)
            print("Cookies accepted.")
    except TimeoutError:
        print("Cookie popup not found, continuing...")

async def find_magazine_test(page):
    index = 0
    while True:
        # Get the list fresh every time to avoid stale references
        magazines = await page.query_selector_all("span.text-grid[data-tile-out]")

        if index >= len(magazines):
            break

        magazine = magazines[index]
        name = await magazine.inner_text()
        safe_name = name.replace("/", "-").replace("\\", "-").strip()

        print(f"Processing magazine: {safe_name}")

        await magazine.click()
        await page.wait_for_load_state('networkidle')

        folder_path = f"screenshots/{safe_name}"
        os.makedirs(folder_path, exist_ok=True)

        await page.screenshot(path=f"screenshots/{safe_name}/page_1.png")
        await scrape_pages(page, safe_name)
        print("Finished scraping of the pages.")

        # Go back to the main page
        await page.goto("https://www.broshura.bg/i/3")
        await page.wait_for_load_state('networkidle')

        index += 1


async def scrape_pages(page, safe_name):
    # base url = # https://www.broshura.bg/b/5531879#page-1
    base_url = page.url.split("#")[0]
    print(base_url) # https://www.broshura.bg/b/5531879
    page_number = 2

    while True:
        url = f"{base_url}#page-{page_number}"
        print(f"Trying URL: {url}")
        try:
            # go to the next page
            await page.goto(url, wait_until='networkidle')

            #
            current_url = page.url
            if re.search(r"#page-1$", current_url):
                print(f"Redirected to {current_url}. Invalid page. Stopping.")
                break

            await asyncio.sleep(1.5)
            await page.screenshot(path=f"screenshots/{safe_name}/page_{page_number}.png")
            print(f"Captured screenshot for page {page_number}")

            page_number += 2

        except TimeoutError:
            print(f"Timeout at {url}. Stopping.")
            break


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False) #browser
        context = await browser.new_context() # new context
        await context.tracing.start(screenshots=True, snapshots=True, sources=True) # start tracing
        page = await context.new_page()

        await page.goto("https://www.broshura.bg/i/3")

        # Actions
        await test_cookie_accept(page)
        await find_magazine_test(page)

        #await context.tracing.stop(path="logs/trace.zip")
        await browser.close()

asyncio.run(main())