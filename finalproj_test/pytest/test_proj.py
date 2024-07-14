from playwright.sync_api import sync_playwright
import time

def test_01():
    

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("http://localhost:35000")
        
        
        
        username=page.locator('//input[@id="username"]')
        password=page.locator('//input[@id="password"]')
        login_btn=page.locator('//button[@type="submit"]')

        food=page.locator('//input[@id="food"]')
        transcription= page.locator('//input[@id="transportation"]')
        housing= page.locator('//input[@id="housing"]')
        utilities= page.locator('//input[@id="utilities"]')
        entertainment= page.locator('//input[@id="entertainment"]')
        others= page.locator('//input[@id="others"]')
        calculate= page.locator('//input[@value="Calculate"]')


        totalExpenses= page.locator('//div[@id="totalExpenses"]/h2')

       
        username.type('lior')
        password.type('1206')
        login_btn.click()
        
        
        def calc_dns(_food,_transcription,_housing,_utilities,_entertainment,_others):
            food.type(_food)
            transcription.type(_transcription)
            housing.type(_housing)
            utilities.type(_utilities)
            entertainment.type(_entertainment)
            others.type(_others)
            calculate.click()
            
        calc_dns('50','60','70','150','56','7800')
        
        totalExpenses_split= totalExpenses.inner_text().split("$")[1]
        
        
        assert totalExpenses_split == '8186.00'