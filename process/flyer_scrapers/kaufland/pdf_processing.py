import asyncio, os, aiohttp, ssl,  re
from playwright.async_api import async_playwright, TimeoutError
from .popup_helper import popup_watcher
from utils import safe_write_bytes, safe_mkdir

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

data_downloads_path = os.path.join("data", "downloads", "kaufland")
kaufland_downloads_path = os.path.join("process", "flyer_scrapers", "kaufland", "downloads")
kaufland_screenshots_path = os.path.join("process", "flyer_scrapers", "kaufland", "screenshots")

safe_mkdir(data_downloads_path)
safe_mkdir(kaufland_downloads_path)
safe_mkdir(kaufland_screenshots_path)

async def download_pdf(url, filename):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, ssl=ssl_context) as resp:
            if resp.status == 200:
                file_bytes = await resp.read()
                safe_write_bytes(os.path.join(kaufland_downloads_path, filename), file_bytes)
                safe_write_bytes(os.path.join(data_downloads_path, filename), file_bytes)
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
        await page.screenshot(path=f'{kaufland_screenshots_path}/kaufland_page.png')

        print('============== KAUFLAND ==================')

        # Wait for download buttons to appear
        all_download_flyer_btn = await page.query_selector_all("div.a-button--download-flyer")
        download_flyer_btn = [btn for btn in all_download_flyer_btn if await btn.is_visible()]

        num_for_downloads = len(download_flyer_btn)
        print(f"Found {num_for_downloads} download buttons!")

        print(download_flyer_btn)

        for i in range(num_for_downloads):
            # Refresh buttons list inside the loop (page might change)
            download_flyer_bnts = await page.query_selector_all("div.a-button--download-flyer")

            try:
                button = download_flyer_bnts[i]
                async with context.expect_page() as new_page_pdf:
                    await button.click(timeout=3000)
                new_page_pdf = await new_page_pdf.value
            except TimeoutError:
                print("End of flyers_images_labels or timeout reached!")
                break
            except IndexError:
                print(f"Index {i} out of range for {len(download_flyer_bnts)} buttons")
                break

            # Get flyer name safely
            flyer_name_element = await page.wait_for_selector("p.m-flyer-tile__validity-date")
            flyer_name = await flyer_name_element.inner_text()
            safe_name = re.sub(r'[\\/*?:"<>|]', "_", flyer_name)
            filename = f"Брошура_{i+1}_{safe_name}.pdf"
            print("===================================================\n", filename)

            pdf_url = new_page_pdf.url
            print(f"Download page of pdf {i+1}: {pdf_url}")

            # Download the PDF bytes
            await download_pdf(pdf_url, filename)

            # Save a screenshot of the flyer page
            #await page.screenshot(path=f'{kaufland_screenshots_path}/{filename}.png')
            print(f"Finished downloading and screenshot for {filename}.")

            await new_page_pdf.close()
            await page.bring_to_front()
            await page.goto(default_page)
            await page.wait_for_load_state('networkidle')

        watcher_task.cancel()
        try:
            await watcher_task
        except asyncio.CancelledError:
            pass
        await browser.close()
        print('============== RETURN FROM KAUFLAND ==================')

if __name__ == "__main__":
    asyncio.run(download_all_flyers())
