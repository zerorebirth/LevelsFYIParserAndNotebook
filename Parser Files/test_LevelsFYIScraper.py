#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#LevelsFYIScraper.py 

#Function: to scrape for companies worth applying to from levels.fyi

#Input variables:

#s: URL of first page of companies that user wants to scrape
#parser: type of parser that user wants to use (ex: html.parser, html5lib, etc.)
#offset: used to determine next page of companies that should be recorded
#(check levels.fyi url on page 2 of your search to see this)
#max_offset: the very last page's offset + 1
#offset_increment: the increment between page offsets
#(third page offset - second page offset, if only two pages are searched,
#then any integer works)
#s2: the first half of the url for the companies starting from page 2,
#determined by taking offsets and merging with url
#s3: the second half of the url for the companies starting from page 2,
#determined by taking offsets and merging with url 
#continue_program: boolean (true or false) that stops program after 3 attempts if false,
#continues otherwise
#stack: companies the user wants to record are added to this stack

#Output variable:

#stack: list of company names that user wants

#Instructions:

#All arguments except the offsets and continue_program must be python strings.
#Offsets and continue_program must be integers.
#When running in terminal, after typing in the name of the .py file, enter in:

#The first url to be scraped,
#parser type,
#offset from second url,
#offset from the very last url + 1,
#offset increment (third url offset - second url offset,
#if only two pages then any integer works),
#the second page url up to and including 'offset=',
#the rest of the second page url,
#and 0 if you only want to attempt the program three times (1 otherwise).

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
import sys
import requests
import asyncio
import pytest
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

@pytest.mark.asyncio
async def test_main(capsys):

    #if less or greater than 19 inputs, throw error
    
    if len(sys.argv) != 19:
        with capsys.disabled():
            print("\nERROR: Total arguments do not equal 19 for this program." +
                  "Closing.\nCheck reference notebook in Github repository for" +
                  "proper formatting. Exiting.")
            return 1
    
    #input variables are gotten from terminal command line
    s = sys.argv[2]
    parser = sys.argv[4]
    offset, max_offset, offset_increment = sys.argv[6], sys.argv[8], sys.argv[10]
    s2 = sys.argv[12]
    s3 = sys.argv[14]
    continue_program = sys.argv[16]

    #if integer variables are not in proper format, throw error.
    
    try:
        offset = int(offset)
        max_offset = int(max_offset)
        offset_increment = int(offset_increment)
        continue_program = int(continue_program)
    except:
        with capsys.disabled():
            print("\nERROR: One or more of the offsets and/or the continue_program" +
                  "variable are not integers.\nCheck reference notebook in Github" +
                  "repository for proper formatting. Exiting.")
            return 1
    
    stack = parseFirstPage(s, parser) #parse first url
    
    #if parse failed, throw error.
    
    if stack == 1:
        with capsys.disabled():
            print("\nERROR: First was not a valid url,\n" +
                  "and/or parser was not a valid parser." +
                  "\nCheck reference notebook in Github repository for proper" +
                  "formatting. Exiting.")
            return 1
            
    p = await async_playwright().start()
    browser = await p.firefox.launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox','--disable-gpu','--single-process'])

    stack = await parseRemainingPages(offset, max_offset, offset_increment, s2, parser, stack, s3, browser, continue_program, capsys) #parse remaining urls
    
    #if parse failed, throw error.
    
    if stack == 1:
        with capsys.disabled():
            if not continue_program:
                return 1
            print("\nERROR: Second url was not a valid url." +
                  "\nIn addition, offsets and/or chrome paths may be incorrect." +
                  "\nCheck reference notebook in Github repository for proper" +
                  "formatting. Exiting.")
            return 1

    #print companies obtained
    with capsys.disabled():
        print(stack)
        
    await browser.close() #close browser
    await p.stop() #close playwright
        
    return 0 #program exits successfully

    raise Exception("program failed") #exception in case program fails

def parseFirstPage(s, parser):

    #attempt to run function
    try:
        r = requests.get(s) #get html content from s

        #parse the html content from s with user-selected parser
        soup = BeautifulSoup(r.content, parser)

        #get companies from parsed html
        stack = [soup.select('h2')[i].next for i in range(len(soup.select('h2')))]
        
        return stack #return companies from first page
    except:
        #error occurred with s and/or parser, return 1
        return 1

@pytest.mark.asyncio
async def parseRemainingPages(offset, max_offset, offset_increment, s2, parser, stack, s3, browser, continue_program, capsys):

    counter = 1 #number of attempts to obtain company names    

    failure = False #flag for continuing program

    page = await browser.new_page() #new browser page
    
    #loop program while active
    while 1:
        
        try: #try to run function

            #list of urls to be searched
            vals = [s2+str(i)+s3 for i in range(offset, max_offset, offset_increment)]

            for i in range(0, len(vals)): #for each url
                #go to url and wait for h2 elements to load
                await page.goto(vals[i])
                await page.wait_for_selector('h2')

                #parse the html of the webpage
                soup = BeautifulSoup(await page.content(), parser)

                #get all company names through h2 elements
                companies = [i.text for i in soup.find_all('h2')]

                #remove the last element, as it is not a company name
                companies.pop()

                #add company names to list
                stack+=companies

            #exit with all companies
            break

        #exception thrown if website fails
        except Exception as e:

            #print failed attempt number
            with capsys.disabled():
                print(f"\nAttempt {counter} failed...")

                #quit program after three attempts if continue_program = 0 (false)
                if counter==3 and not continue_program:
                    print("\nUser does not wish to continue after 3 attempts. Exiting.")
                    failure = True
                    break

            #increment number of attempts
            counter+=1
            
            continue #move to next attempt

    #check flag for continuing program and exit if flag is on
    if failure:
        return 1

    #otherwise, confirm successful attempt
    with capsys.disabled():
        print(f"\nAttempt {counter} succeeded!\n")

    #return company list
    return stack
