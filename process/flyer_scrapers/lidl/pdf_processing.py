import asyncio, os, aiohttp, ssl, re
from playwright.async_api import async_playwright
from .popup_helper import popup_watcher
from utils import safe_write_bytes, safe_mkdir

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

data_downloads_path = os.path.join("data", "downloads", "lidl")
lidl_downloads_path = os.path.join("process", "flyer_scrapers", "lidl", "downloads")
lidl_screenshots_path = os.path.join("process", "flyer_scrapers", "lidl", "screenshots")

safe_mkdir(data_downloads_path)
safe_mkdir(lidl_downloads_path)
safe_mkdir(lidl_screenshots_path)

async def download_pdf(url, filename):

    async with aiohttp.ClientSession() as session:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, ssl=ssl_context) as resp:
                if resp.status == 200:
                    file_bytes = await resp.read()
                    safe_write_bytes(os.path.join(lidl_downloads_path, filename), file_bytes)
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

        default_page = "https://www.lidl.bg/c/broshura/s10020060"
        await page.goto(default_page)
        await page.screenshot(path=f'{lidl_screenshots_path}/lidl_page.png')

        print('============== LIDL ==================')

        # Save sorted_images_labels download buttons
        num_buttons = len(await page.query_selector_all("a.flyer"))
        print(f"Found {num_buttons} download buttons.")

        for i in range(num_buttons):

            # Refresh the button list
            flyer = (await page.query_selector_all("a.flyer"))[i]

            # Get the name of the flyer
            flyer_name_element = await flyer.query_selector("h2.flyer__name")
            flyer_name = await flyer_name_element.inner_text()
            safe_name = re.sub(r'[\\/*?:"<>|]', "_", flyer_name)
            filename = f"Брошура_{i + 1}_{safe_name}.pdf"
            print("===================================================\n",filename)

            await flyer.click()

            # Download the pdf file process...
            await page.locator("span.button__label:has-text('Меню')").click()
            async with context.expect_page() as new_page_pdf:
                await page.locator("span.button__label:has-text('Свали PDF')").click()
                print(f"Downloading flyer {i+1}...")

            # Load the new pdf page
            new_page_pdf = await new_page_pdf.value
            await new_page_pdf.wait_for_load_state()
            pdf_url = new_page_pdf.url
            print(f"Download page of pdf {i+1}: {pdf_url}")

            # Download the PDF
            await download_pdf(pdf_url, filename)
            await page.screenshot(path=f'{lidl_screenshots_path}/{filename}.png')

            # Back to seeing the default page and closing the new page
            await new_page_pdf.close()
            await page.bring_to_front()
            await page.goto(default_page)

        # Close the program
        watcher_task.cancel()
        try:
            await watcher_task
        except asyncio.CancelledError:
            pass
        await browser.close()
        print('============== RETURN FROM LILD ==================')

if __name__ == "__main__":
    asyncio.run(download_all_flyers())
