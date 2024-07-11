from playwright.sync_api import sync_playwright
from datetime import time

def test_01():
    

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("http://localhost:35000")
        
        
        
        username=page.locator('//input[@id="username"]')
        password=page.locator('//input[@id="password"]')
        login_btn=page.locator('//button[@type="submit"]')
       
        username.type('lior')
        password.type('lior1206')
        login_btn.click()
        time.sleep(5)
        
        
