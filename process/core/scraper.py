
import re, asyncio, requests

from process.flyer_scrapers import kaufland_pdf_processing, lidl_pdf_processing
# --- SCRAPING FLYER PAGES, CALLING THE CORRESPONDING SUPERMARKET ---

supermarket_processors = {
        'kaufland': [kaufland_pdf_processing, False],
        'lidl': [lidl_pdf_processing, False],
        # 'billa': [billa_pdf_processing, False]
    }

async def scrape_website(url):
    print('========== Scraping the website ============')
    for supermarket_name, (processor_func, checked) in supermarket_processors.items():

        if supermarket_name in url and not checked:
            print(f'Going to {supermarket_name}: {url}')
            await processor_func() # just run it!
            supermarket_processors[supermarket_name][1] = True
            return True

        elif supermarket_name in url and checked:
            print(f'Already went to {supermarket_name}: {url}')
            return True

    print(f'Supermarket for {url} not found in the system.')
    print('===================================================')
    return False

def save_image_from_url(url, file_name):
    response = requests.get(url)
    if response.status_code == 200:
        with open(file_name, 'wb') as f:
            f.write(response.content)
        print(f"Image saved as {file_name}")
    else:
        print("Failed to download image")

async def scrape_pages(page, safe_name):
    base_url, page_number_str = page.url.split("#page-")
    print(base_url,'\n',page_number_str)
    page_number = int(page_number_str)

    print('========== Scraping the pages ============')
    while True:
        # Wait before taking a screenshot
        await asyncio.sleep(1.5)

        # Find the next url OR button
        #await page.screenshot(path=f"data/screenshots/{safe_name}/page_{page_number}.png")
        #print(f"Captured screenshot for page {page_number}")
        '''
        src, srcset = get_image_urls(page.url)
        print("SRC:", src)
        print("SRCSET:", srcset)
        
        img_src = page.eval_on_selector('img', 'el => el.getAttribute("src")')
        img_srcset = page.eval_on_selector('img', 'el => el.getAttribute("srcset")')
        save_image_from_url(img_src, f'process/core/images/{page_number}_src.webp')
        save_image_from_url(img_srcset, f'process/core/images/{page_number}_srcset.webp')
        '''

        await page.screenshot(path=f'data/pages/{safe_name}/{page_number}.png')
        # Prepare next page number
        if page_number == 1:
            page_number += 1
        else:
            page_number += 2

        next_url = f"{base_url}#page-{page_number}"
        print(page_number)

        # Navigate to next page
        await page.goto(next_url, wait_until='networkidle')
        # Check if redirected to an invalid page
        if page.url.endswith("#page-1") and page_number != 1:
            print(f"Redirected to {page.url}. Page {page_number} is invalid. Stopping.")
            print('===================================================')
            return
