This readme is meant to help you use the Levels.fyi parser.

The sample input in order to run the parser looks like this:

pytest --s "https://www.levels.fyi/jobs?locationSlug=united-states&searchText=software+engineer" --max_offset 196 test_LevelsFYIScraper.py

Let me explain each part:

pytest: This is the python library needed to execute this program.

--s: This is a parameter meant to be input on the command line.

Any time you see double dashes, it refers to a parameter that will be used in the program.

In this case, s refers to the first url of your job search on Levels.fyi.

What follows after the s is the full url. 

You must type both the parameter (--s, in this case)
and the parameter's value (the full url) for the program to function correctly.

If you want to change the url used, copy the url from your search and replace the url proceeding after s.

--max_offset: This refers to ((number of pages to scrape)*5)+1.

So, if you want to scrape 15 pages, the number would be 76, since:

(15*5)+1 = 76

Finally, the last input is simply the program name, test_LevelsFYIScraper.py. This is important,
since the program will not run unless you input the name.

That's it for the input. However, make sure you install the proper libraries needed for the program's execution.

Here are a list of install commands, to be used with the command line.

pip install -U pytest
pip install pytest-base-url
pip install playwright
pip install pytest-asyncio
pip install asyncio
pip install pluggy
pip install anyio
pip install typeguard
playwright install

Feel free to push a request in case you feel something is wrong about the program.

Thanks!

-zerorebirth
