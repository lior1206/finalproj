import pytest
from playwright.sync_api import sync_playwright

# @pytest.fixture(scope="function")
# def chromium_browser():
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False)
#         yield browser
#         browser.close()