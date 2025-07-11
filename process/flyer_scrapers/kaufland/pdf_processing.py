import asyncio, os, aiohttp, ssl, re
from .popup_helper import popup_watcher
from playwright.async_api import async_playwright, TimeoutError
from utils import safe_write_bytes

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

async def download_pdf(url, filename):
    kaufland_downloads_path = f"flyer_scraper/kaufland/downloads/{filename}"
    data_downloads_path = f"data/downloads/{filename}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url, ssl=ssl_context) as resp:
            if resp.status == 200:
                file_bytes = await resp.read()
                safe_write_bytes(kaufland_downloads_path, file_bytes)
                safe_write_bytes(data_downloads_path, file_bytes)
                print(f"Downloaded: {filename}")
            else:
                print(f"Failed to download {url} (status: {resp.status})")

async def download_all_flyers():
    async with async_playwright() as p:

        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        watcher_task = asyncio.create_task(popup_watcher(page))

        default_page = "https://www.kaufland.bg/broshuri.html"
        await page.goto(default_page)
        await page.screenshot(path="screenshots/kaufland_page.png")

        print('============== KAUFLAND ==================')

        # Save all download buttons
        num_buttons = len(await page.query_selector_all("div.m-tab-navigation__inner-container--show div.a-button--download-flyer"))
        print(f"Found {num_buttons} download buttons!")

        for i in range(num_buttons):

            # Refresh the button list
            button = (await page.query_selector_all("div.a-button--download-flyer"))[i]

            # Try clicking
            try:
                await button.click(timeout=3000)  # 3 sec
            except TimeoutError:
                print("End of flyers!")
                break

            # Expect new page
            async with context.expect_page() as new_page_pdf:
                pass

            # Get the name of the flyer
            flyer_name_element = await page.wait_for_selector("p.m-flyer-tile__validity-date")
            flyer_name = await flyer_name_element.inner_text()
            safe_name = re.sub(r'[\\/*?:"<>|]', "_", flyer_name)
            filename = f"Брошура_{i+1}_{safe_name}.pdf"

            # Load the page
            new_page_pdf = await new_page_pdf.value
            pdf_url = new_page_pdf.url
            print(f"Download page of pdf {i+1}: {pdf_url}")

            # Download the PDF
            await download_pdf(pdf_url, filename)
            await new_page_pdf.screenshot(path=f"screenshots/Брошура_{i+1}_{safe_name}.png")
            print(f"Finished downloading {filename}.")

            # Back to seeing the default page and closing the new page
            await new_page_pdf.close()
            await page.bring_to_front()

        # Close the program
        watcher_task.cancel()
        try:
            await watcher_task
        except asyncio.CancelledError:
            pass
        await browser.close()
        print('============== RETURN FROM KAUFLAND ==================')

if __name__ == "__main__":
    asyncio.run(download_all_flyers())
