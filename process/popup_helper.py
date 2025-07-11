import asyncio

async def cookies(page):
    try:
        await page.click("div#cookiescript_accept", timeout=3000)
        print("---Cookies accepted.---")
        return True
    except Exception:
        return False

async def popup_watcher(page):
    cookies_accepted = False

    while True:
        accepted_now = await cookies(page)
        if accepted_now and not cookies_accepted:
            cookies_accepted = True
            print("---Cookies accepted now.---")
        elif not accepted_now and not cookies_accepted:
            print("---No cookie button found or already accepted.---")

        await asyncio.sleep(10)  # check every 10 seconds to reduce log spam