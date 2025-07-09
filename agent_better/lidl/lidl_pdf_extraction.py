import asyncio, os, aiohttp, ssl, re

from popup_helper import popup_watcher_lidl
from playwright.async_api import async_playwright

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

async def download_pdf(url, filename):
    os.makedirs("downloads", exist_ok=True)
    async with aiohttp.ClientSession() as session:
        async with session.get(url, ssl=ssl_context) as resp:
            if resp.status == 200:
                with open(f"downloads/{filename}", "wb") as f:
                    f.write(await resp.read())
                print(f"Downloaded: {filename}")
            else:
                print(f"Failed to download {url} (status: {resp.status})")

async def main():
    async with async_playwright() as p:

        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        watcher_task = asyncio.create_task(popup_watcher_lidl(page))

        default_page = "https://www.lidl.bg/c/broshura/s10020060"
        await page.goto(default_page)
        await page.screenshot(path="screenshots/lidl_page.png")

        # Save all download buttons
        num_buttons = len(await page.query_selector_all("img.flyer__image"))
        print(f"Found {num_buttons} download buttons.")

        for i in range(num_buttons):

            # Refresh the button list
            flyer = (await page.query_selector_all("a.flyer"))[i]

            # Get the name of the flyer
            flyer_name_element = await flyer.query_selector("h2.flyer__name")
            flyer_name = await flyer_name_element.inner_text()
            safe_name = re.sub(r'[\\/*?:"<>|]', "_", flyer_name)
            filename = f"Брошура_{i + 1}_{safe_name}.pdf"
            print(filename)

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
            await new_page_pdf.screenshot(path=f"screenshots/{filename}.png")
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

asyncio.run(main())