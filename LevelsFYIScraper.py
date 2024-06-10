#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#LevelsFYIScraper.py 

#Function: to scrape for companies worth applying to from levels.fyi

#Input variables:

#s: URL of first page of companies that user wants to scrape
#parser: type of parser that user wants to use (ex: html.parser, html5lib, etc.)
#offset: used to determine next page of companies that should be recorded (check levels.fyi url on page 2 
#                                                                          of your search to see this)
#max_offset: the very last page's offset + 1
#offset_increment: the increment between page offsets (third page offset - second page offset, 
#                                                      if only two pages then any integer works)
#s2: the urls for the companies starting from page 2, determined by taking offsets from vals variable
#stack: companies the user wants to record are added to this stack

#Output variable:

#stack: list of company names that user wants

#Instructions:

#All arguments except the offsets must be python strings or f-strings.
#Offsets must be integers.
#When running in terminal, after typing in the name of the .py file, enter in:

#The first url to be scraped,
#parser type,
#offset from second url,
#offset from the very last url + 1,
#offset increment (third url offset - second url offset, if only two pages then any integer works),
#and the second page url with 'offset={vals[i]}' and f in front of the first quotation mark.

#Refer to the reference notebook in case you are confused.

#Time complexity: O(n*m), where n is the number of urls the user wants to scrape
#                         and m is the number of companies per url

#Space complexity: O(m), where m is the number of companies per url

#################################################################################
# Date modified              Modifier             What was modified             #
# 06/09/2024                 Eram Kabir           Initial Development           #
#################################################################################

#libraries
import sys
import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

def main():
    
    #input variables are gotten from terminal command line
    
    s = sys.argv[1]
    parser = sys.argv[2]
    offset, max_offset, offset_increment = sys.argv[3], sys.argv[4], sys.argv[5]
    s2 = sys.argv[6]
    
    #if variables are not in proper format, throw error.
    
    if type(s) != str:
        print("\nERROR: First url is not a string. Try again.")
        return 1
    
    if type(parser) != str:
        print("\nERROR: Parser is not a string. Try again.")
        return 1
    
    if type(offset) != int or type(max_offset) != int or type(offset_increment) != int:
        print("\nERROR: One or more of the offsets are not integers. Try again.")
        return 1
    
    if type(s2) != str:
        print("\nERROR: Second url is not a string. Try again.")
        return 1
    
    #if less or greater than 7 inputs, throw error
    
    if len(sys.argv) != 7:
        print("\nERROR: Total arguments do not equal 7 for this program. Closing.")
        return 1
    
    stack = parseFirstPage(s, parser) #parse first url
    
    #if parse failed, throw error and reason for error.
    
    if stack == 1:
        print("\nERROR: First url was not a valid url,\nand/or parser was not a valid parser." +
              "\nCheck reference notebook in Github repository for proper formatting. Exiting.")
        return 1
    
    stack = parseRemainingPages(offset, max_offset, offset_increment, s2, parser, stack) #parse remaining urls
    
    #if parse failed, throw error and reason for error.
    
    if stack == 1:
        print("\nERROR: Second url was not a valid url,\nand/or parser was not a valid parser." +
              "\nIn addition, offsets may be incorrect." +
              "\nCheck reference notebook in Github repository for proper formatting. Exiting.")
        return 1
    
    print(stack) #print out all companies
    
    return 0 #program exits successfully

def parseFirstPage(s, parser):
    try: #try to run function
        r = requests.get(s) #get html content from s
        soup = BeautifulSoup(r.content, parser) #parse the html content from s with parser
        stack = [soup.select('h2')[i].next for i in range(len(soup.select('h2')))] #get companies from s
        return stack #return companies from first page
    except:
        #error occurred with s and/or parser, return 1
        return 1

def parseRemainingPages(offset, max_offset, offset_increment, s2, parser, stack):
    
    try: #try to run function
        
        vals = [str(i) for i in range(offset, max_offset, offset_increment)] #list of offsets (used to construct s2)

        for i in range(0, len(vals)): #for each url
            driver = webdriver.Chrome() #type of driver to use to open website (chrome, in this case)
            driver.get(s2) #open website
            r = driver.page_source #get html from open website
            soup = BeautifulSoup(r, parser) #parse html from open website
            for j in range(0, len(soup.select('h2'))): #for each company on the open website:
        
                #if the company is not in the stack already, and is not "Company Details" 
                #                                            and does not have "levels.fyi",
                #                                            add it to the stack
                
                if soup.select('h2')[j].next not in stack and soup.select('h2')[j].next != "Company Details" and "levels.fyi" not in soup.select('h2')[j].next:
                    stack.append(soup.select('h2')[j].next)
    except:
        #error occurred with s, offsets and/or parser, return 1
        return 1
    
if __name__ == "__main__":
    then = time.perf_counter() #record time at t = 0s
    main() #run program
    print("Request finished in " + str(time.perf_counter() - then) + " seconds.") #determine length of program run

