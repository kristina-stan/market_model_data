import asyncio

async def lidl_cookies(page):
    try:
        await page.click("button.ot-button-order-2", timeout=3000)
        print("---Cookies accepted.---")
        return True
    except Exception:
        return False

async def popup_watcher(page):
    cookie_accepted = False
    while True:
        accepted_now = await lidl_cookies(page)
        if accepted_now and not cookie_accepted:
            cookie_accepted = True
            print("---Cookies accepted now.---")
        elif not accepted_now and not cookie_accepted:
            print("---No cookie button found or already accepted.---")
        await asyncio.sleep(10)  # check every 10 seconds, less spammy
