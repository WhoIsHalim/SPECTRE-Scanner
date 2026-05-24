from playwright.async_api import async_playwright


async def screenshot(url, output):
    async with async_playwright() as p:
        browser = await p.chromium.launch()

        page = await browser.new_page()

        await page.goto(url, wait_until="networkidle")

        await page.screenshot(path=output, full_page=True)

        await browser.close()