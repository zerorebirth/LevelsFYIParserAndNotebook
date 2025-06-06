This reference notebook is meant to help you use the Levels.fyi parser.

The parser in question, uses Playwright to open up a headless browser asynchronously, which is then navigated to the desired levels.fyi url. Following this, the hiring companies on the site are scraped using the BeautifulSoup and Requests (REST API) libraries.

The data is then allocated to a stack (array), and then printed out to the terminal.

As you may have guessed, the program is meant to be run from the terminal. However, the functions can be extracted and run from anywhere, if needed.

Inputs:

The sample input in order to run the parser looks like this:

pytest --s "https://www.levels.fyi/jobs/location/new-york-usa?locationSlug=united-states&searchText=software+engineer&jobId=99222064430228166" --parser html.parser --offset 5 --max_offset 196 --offset_increment 5 --s2 "https://www.levels.fyi/jobs/location/new-york-usa?locationSlug=united-states&offset=" --s3 "&searchText=software+engineer&jobId=99222064430228166" --continue_program 0 test_LevelsFYIScraper.py

Let me explain each part:

pytest: This is the python library needed to execute this program

--s: This is a parameter meant to be input on the command line.

Any time you see double dashes, it refers to a parameter that will be used in the program.

In this case, s refers to the first url of your job search on Levels.fyi.

What follows after the s is the full url. 

You must type both the parameter (--s, in this case)
and the parameter's value (the full url) for the program to function correctly.

If you want to change the url used, copy the url from your search and replace the url proceeding after s.

--parser: This refers to the parser used to parse the website. html.parser is used by default, and follows --parser.

XML parser is not recommended for use.

--offset: this refers to the offset within the url of the first page of your job search.

The 5 proceeding it is the offset I found in my own job search, and is used as a sample for the sample input.

--max_offset: This refers to the last url's offset + 1.

The 196 proceeding it is the offset 195 plus one, leading to 196. This is also a sample from my last job search.

--offset_increment: This is the offset from the third page of your job search minus the offset from the second page
of your job search. For example, let's say the offset from the third page was 30, and the offset from the second
page was 25. The offset_increment would then be 30 - 25, which is 5.

The value for the offset in the sample input happens to be 5, by coincidence.

--s2: This refers to the portion of the url of the second page of your job search up to and including "offset=".

If you are confused, take a look at the url of the second page of your job search, find the "offset=", and copy
every part of the url up to and including the "offset=". Then paste it in place of the sample input for s2.

The sample input is from my search, once again.

--s3: This refers to the remainder of the url that s2's value was taken from.

So, copy and paste every part of the url after, but not including, "offset=".

I'm going to assume that you know the sample input has information from my job search, since I've written that many
times by now.

--continue_program: This is the last parameter. It refers to if you, the user, want the program to run to completion
or stop after three attempts. Enter in 0 to stop after three attempts, or 1 to continue until completion.

Finally, the last input is simply the program name, test_LevelsFYIScraper.py. This is important,
since the program will not run unless you input the name.

That's it for the input. However, make sure you install the proper libraries needed for the program's execution.

Here are a list of pip installs, that will allow you to do so using the command line.

pip install -U pytest
pip install pluggy
pip install asyncio
pip install pytest-base-url
pip install playwright

In addition, here are the pip installs for the .py file (make sure to run on command line as well).

pip install requests
pip install beautifulsoup4

Feel free to push a request in case you feel something is wrong about the program.

Thanks!

-zerorebirth
