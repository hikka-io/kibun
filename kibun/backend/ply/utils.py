from playwright._impl._errors import TimeoutError as PlyTimeoutError
from kibun.backend.ply.response import process_response
from playwright._impl._errors import Error as PlyError
from playwright.async_api import async_playwright
from kibun import constants


async def get_playwright():
    return await async_playwright().start()


async def get_browser_ply(playwright, headless: bool = True):
    browser = await playwright.firefox.launch(
        headless=headless,
        firefox_user_prefs={
            "permissions.default.image": 2,
        },
    )

    return browser


async def get_context_ply(
    browser,
    proxy: str | None = None,
    enable_js: bool = False,
    user_agent="Mozilla/5.0 (Windows NT 10.0; rv:102.0) Gecko/20100101 Firefox/102.0",
):
    context = await browser.new_context(
        user_agent=user_agent,
        java_script_enabled=enable_js,
        ignore_https_errors=True,
        proxy={"server": proxy},
    )

    return context


async def make_request_ply(
    context,
    url,
    timeout=10000,
    error_markers=[],
):
    try:
        page = await context.new_page()

        r = await page.goto(url, timeout=timeout)

        content, status = await process_response(r, error_markers)

        await page.close()

        return content, status

    except (PlyTimeoutError, PlyError):
        return None, constants.NETWORK_ERROR
