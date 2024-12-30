import pytest_asyncio
from playwright.async_api import async_playwright

async def browser():
        p = await async_playwright().start()
        browser = await p.firefox.launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox','--disable-gpu','--single-process'])
        yield browser

@pytest_asyncio.fixture(scope="function")
async def browser_indirect():
    return browser()
