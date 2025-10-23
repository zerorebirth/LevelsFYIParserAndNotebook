#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#LevelsFYIScraper.py 

#Function: to scrape for companies worth applying to from levels.fyi

#Input variables:

#s: URL of first page of job search on Levels.fyi
#max_offset: ((Number of pages to scrape)*5)+1

#Output variable:

#stack: list of company names that user wants

#Instructions:

#Simply run: 
 
#pytest --s s --max_offset max_offset

#In the terminal, where the 2nd s is the url and the 2nd max_offset is the max_offset.

#Refer to the reference notebook in case you are confused.

#Time complexity: O(n*m), where n is the number of urls the user wants to scrape
#                         and m is the number of companies per url

#Space complexity: O(m), where m is the number of companies per url

#################################################################################
# Date modified              Modifier             What was modified             #
# 06/09/2024                 Eram Kabir           Initial Development           #
# 10/30/2024                 Eram Kabir           Optimized speed of program    #
# 12/29/2024                 Eram Kabir           Optimized/simplified program  #
#################################################################################

#libraries
import os
import sys
import pytest
from playwright.async_api import async_playwright

@pytest.mark.asyncio
async def test_main(capsys):

    #if less or greater than 6 inputs, throw error
    if len(sys.argv) != 6:
        with capsys.disabled():
            print('\nERROR: Total arguments do not equal 5 for this program.' +
                  'Closing.\nCheck reference notebook in Github repository for' +
                  'proper formatting. Exiting.')
            return 1

    #input variables are gotten from terminal command line
    s = sys.argv[2]
    max_offset = sys.argv[4]
    offset = 5
    offset_increment = 5
    #if any input is not in proper format, throw error
    try:
        max_offset = int(max_offset)
    except:
        with capsys.disabled():
            print('\nERROR: Invalid offset entered. Please enter an integer next time.')
            return 1
        
    if not isinstance(s, str):
        with capsys.disabled():
            print('\nERROR: Invalid url entered. Please enter a string next time.')
            return 1
    
    #start asynchronous playwright
    p = await async_playwright().start()
    
    #launch browser in background
    browser = await p.chromium.launch(headless=False)
    stack = await parseFirstPage(s, browser, capsys) #parse first url
    
    #if parse failed, throw corresponding error
    
    if stack == 2:
        with capsys.disabled():
            print('\nERROR: Invalid url entered. Enter the url of the first page of your search.\nEx: "https://www.levels.fyi/jobs?locationSlug=united-states&searchText=software+engineer"')
            return 1
        
    if stack == 1:
        with capsys.disabled():
            print('\nERROR: Bot-filter screen was detected. Try running the program again, either now or later.')
            return 1
    
    #parse remaining urls
    stack = await parseRemainingPages(s, offset, max_offset, offset_increment, stack, browser, capsys)
    
    #if parse failed, throw error.
    
    if stack == 1:
        with capsys.disabled():
            print('\nERROR: Bot-filter screen was detected. Try running the program again, either now or later.')
            return 1

    #print companies obtained
    with capsys.disabled():
        print(stack)
        
    await browser.close() #close browser
    await p.stop() #close playwright
        
    return 0 #program exits successfully

@pytest.mark.asyncio
async def parseFirstPage(s, browser, capsys):

    stored_session = "levels_state.json" #path for storing validated session

    if os.path.exists(stored_session): #if valid session

        #start context with validated session
        context = await browser.new_context(storage_state=stored_session) 

    else: #otherwise

        #start new context
        context = await browser.new_context()

    page = await context.new_page() #get new page

    #string to get all companies from page
    extract_js = '''
    () => Array.from(document.querySelectorAll("h2[class*='companyName']"))
            .map(e => e.innerText.replace(/\\u200c/g,'').trim())
    '''

    timeout_limit = 1000 #timeouts for awaited page operations

    bot_detected = False #determines if bot screen was detected

    stack = [] #list to hold companies
        
    try: #try to run function
        seen = set() #keep track of already seen companies
        ordered = [] #keep track of companies

        await page.goto(s) #go to the url page

        #check if url leads to Levels.fyi job search page, return error code if not
        try:
            await page.wait_for_selector('input[placeholder*="Search by title, keyword or company"]', timeout=timeout_limit)
        except Exception:
            return 2
        
        #check if Levels.fyi opened with intro popup, and bypass if so
        #otherwise, do nothing
        try:
            await page.wait_for_selector('button:has-text("Continue")', timeout=timeout_limit)
            await page.click('button:has-text("Continue")', timeout=timeout_limit)
            await page.wait_for_timeout(500)  # give page a moment to refresh
        except Exception:
            pass
        
        #checks if bot screen was detected
        try:
            await page.click("button:has-text('Begin')", timeout=timeout_limit)
            bot_detected = True
        except:
            pass

        #asks user to complete captcha if bot screen was detected (once every program run
        #from terminal)
        if bot_detected:
            with capsys.disabled():
                print("Bot detected — manual intervention required.")
                print("Solve the challenge in the open browser page, then press any button in the terminal.")
                input()
                await context.storage_state(path=stored_session)
                bot_detected = False

        #wait for company names to pop up
        await page.wait_for_selector('h2[class*="companyName"]')
        
        #try to extract company names, return empty list if unsuccessful
        try:
            current = await page.evaluate(extract_js)
        except Exception:
            current = []
        
        #add company names to set and ordered list, while skipping any empty names
        for name in current:
            if not name:
                continue
            if name not in seen:
                seen.add(name)
                ordered.append(name)
        
        stack+=ordered #add company names to stack

    #exception thrown if bot screen appears and user does not solve it
    except Exception as e:
        with capsys.disabled():
            print(e)
        return 1

    await page.close() #close page

    #return company stack
    return stack


@pytest.mark.asyncio
async def parseRemainingPages(s, offset, max_offset, offset_increment, stack, browser, capsys):

    stored_session = "levels_state.json" #path for storing validated session

    if os.path.exists(stored_session): #if valid session

        #start context with validated session
        context = await browser.new_context(storage_state=stored_session) 

    else: #otherwise

        #start new context
        context = await browser.new_context()

    page = await context.new_page() #start new page

    #string to get all companies from page
    extract_js = '''
    () => Array.from(document.querySelectorAll("h2[class*='companyName']"))
            .map(e => e.innerText.replace(/\\u200c/g,'').trim())
    '''

    timeout_limit = 1000 #timeouts for awaited page operations

    bot_detected = False #determines if bot screen was detected

    #list of urls to parse
    vals = [s+'&offset='+str(i) for i in range(offset, max_offset, offset_increment)]
    
    try: #try to run function
        seen = set() #keep track of already seen companies
        ordered = [] #keep track of companies

        for i in range(0, len(vals)): #for each url
            
            await page.goto(vals[i]) #go to the url page
            
            #check if Levels.fyi opened with intro popup, and bypass if so
            #otherwise, do nothing
            try:
                await page.wait_for_selector('button:has-text("Continue")', timeout=timeout_limit)
                await page.click('button:has-text("Continue")', timeout=timeout_limit)
                await page.wait_for_timeout(500)  # give page a moment to refresh
            except Exception:
                pass
            
            #checks if bot screen was detected, does nothing if not
            try:
                await page.click("button:has-text('Begin')", timeout=timeout_limit)
                bot_detected = True
            except:
                pass

            #asks user to complete captcha if bot screen was detected (once every program run
            #from terminal)
            if bot_detected:
                with capsys.disabled():
                    print("Bot detected — manual intervention required.")
                    print("Solve the challenge in the open browser page, then press any button in the terminal.")
                    input()
                    await context.storage_state(path=stored_session)
                    bot_detected = False

            #wait for company names to pop up
            await page.wait_for_selector('h2[class*="companyName"]')
            
            #try to extract company names, return empty list if unsuccessful
            try:
                current = await page.evaluate(extract_js)
            except Exception:
                current = []
            
            #add company names to set and ordered list, while skipping any empty names
            for name in current:
                if not name:
                    continue
                if name not in seen:
                    seen.add(name)
                    ordered.append(name)

        
        stack+=ordered #add company names to stack

    #exception thrown if bot screen appears
    except Exception as e:
        with capsys.disabled():
            print(e)
        return 1

    await page.close() #close page

    #return company stack
    return stack
