
from .scraper import scrape_pages, scrape_website
from utils import create_folder_if_not_exists, sanitize_filename

# --- finding magazine, clicking links, talks to scraper ---

async def find_magazine_test(page, context):

    magazines = await page.query_selector_all("span.text-grid[data-tile-out]")
    print(f'Found {len(magazines)} magazines')
    for i in range(len(magazines)):

        # Refresh the selectors

        magazines = await page.query_selector_all("span.text-grid[data-tile-out]")
        try:
            magazine = magazines[i+3]
        except IndexError:
            print("End of flyers_images_labels in broshura.bg!")
            break

        name = await magazine.inner_text()
        safe_name = sanitize_filename(name)
        print(f"============ Processing magazine ============\n\"{safe_name}\"")

        # Opens the flyer
        await magazine.click()
        await page.wait_for_load_state('networkidle')

        # Picture for debugging
        folder_path = f"data/screenshots/{safe_name}"
        create_folder_if_not_exists(folder_path)
        await page.screenshot(path=f"{folder_path}/cover.png")

        #print(f"Current URL: {page.url}")
        url_selector = await page.wait_for_selector('div.component-pageflip')
        success = False

        print('============ Searching for link ============')
        if url_selector:
            print(f"FOUND supermarket site link for \"{safe_name}\"!")
            url = await url_selector.get_attribute('data-back-url')
            success = await scrape_website(url)

        if not success:
            print("Scraping pages...")
            await scrape_pages(page, safe_name)
            print("Finished scraping of the pages.")

        # Go back to the main page
        await page.goto("https://www.broshura.bg/i/3")
        await page.wait_for_load_state('networkidle')
        print("\n\n\n")
