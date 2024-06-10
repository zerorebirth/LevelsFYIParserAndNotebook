#LevelsFYIScraper.py 

#Function: to scrape for companies worth applying to from levels.fyi

#Input variables:

#s: URL of first page of companies that user wants to scrape
#parser: type of parser that user wants to use (ex: html.parser, html5lib, etc.)
#offset: used to determine next page of companies that should be recorded (check levels.fyi url on page 2 
                                                                           of your search to see this)
#max_offset: the very last page's offset + 1
#offset_increment: the increment between page offsets (third page offset - second page offset, 
                                                       if only two pages then any integer works)
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
