
import re, asyncio
from process.flyer_scrapers import kaufland_pdf_processing, lidl_pdf_processing
# --- SCRAPING FLYER PAGES, CALLING THE CORRESPONDING SUPERMARKET ---

supermarket_processors = {
        'kaufland': [kaufland_pdf_processing(), False],
        'lidl': [lidl_pdf_processing(), False],
        # 'billa': [billa_pdf_processing(), False]
    }

async def scrape_website(url):
    print('========== Scraping the website ============')
    for supermarket_name, (processor_func, checked) in supermarket_processors.items():

        if supermarket_name in url and not checked:
            print(f'Going to {supermarket_name}: {url}')
            await processor_func  # just run it!
            supermarket_processors[supermarket_name][1] = True
            return True

        elif supermarket_name in url and checked:
            print(f'Already went to {supermarket_name}: {url}')
            return True

    print(f'Supermarket for {url} not found in the system.')
    print('===================================================')
    return False


async def scrape_pages(page, safe_name):
    # base url = # https://www.broshura.bg/b/5531879#page-1
    base_url = page.url.split("#")[0]
    print(base_url) # https://www.broshura.bg/b/5531879
    page_number = 2

    print('========== Scraping the pages ============')
    while True:
        url = f"{base_url}#page-{page_number}"
        #print(f"Trying URL: {url}")
        try:
            # go to the next page
            await page.goto(url, wait_until='networkidle')
            current_url = page.url
            if re.search(r"#page-1$", current_url):
                print(f"Redirected to {current_url}. Invalid page. Stopping.")
                break

            await asyncio.sleep(1.5)
            await page.screenshot(path=f"screenshots/{safe_name}/page_{page_number}.png")
            #print(f"Captured screenshot for page {page_number}")

            page_number += 2

        except TimeoutError:
            print(f"Timeout at {url}. Stopping.")
            break
    print('===================================================')
