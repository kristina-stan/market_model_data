import asyncio

async def kaufland_cookies(page):
    try:
        await page.click("button#onetrust-accept-btn-handler", timeout=3000)
        print("---Cookies accepted.---")
        return True
    except Exception:
        return False

async def kaufland_warning(page):
    try:
        await page.click("a.m-product-recall__close", timeout=3000)
        print("---Warning closed.---")
        return True
    except Exception:
        return False

async def popup_watcher(page):
    cookies_accepted = False
    warning_closed = False
    while True:
        accepted_now = await kaufland_cookies(page)
        if accepted_now and not cookies_accepted:
            cookies_accepted = True
            print("---Cookies accepted now.---")
        elif not accepted_now and not cookies_accepted:
            print("---No cookie button found or already accepted.---")

        closed_now = await kaufland_warning(page)
        if closed_now and not warning_closed:
            warning_closed = True
            print("---Warning popup closed now.---")
        elif not closed_now and not warning_closed:
            print("---No warning popup found or already closed.---")

        await asyncio.sleep(10)  # check every 10 seconds to reduce log spam
