#!/usr/bin/env python
# coding: utf-8

# # Parsing PDFs Homework
# 
# With the power of pdfminer, pytesseract, Camelot, and Tika, let's analyze some documents!
# 
# > If at any point you think, **"I'm close enough, I'd just edit the rest of it in Excel"**: that's fine! Just make a note of it.
# 
# ## A trick to use again and again
# 
# ### Approach 1
# 
# Before we get started: when you want to take the first row of your data and set it as the header, use this trick.

# In[1]:


import pandas as pd


# In[2]:


df = pd.DataFrame([
    [ 'fruit name', 'likes' ],
    [ 'apple', 15 ],
    [ 'carrot', 3 ],
    [ 'sweet potato', 45 ],
    [ 'peach', 12 ],
])
df


# In[3]:


# Set the first column as the columns
df.columns = df.loc[0]

# Drop the first row
df = df.drop(0)

df


# 🚀 Done!
# 
# ### Approach 2
# 
# Another alternative is to use `.rename` on your columns and just filter out the columns you aren't interested in. This can be useful if the column name shows up multiple times in your data for some reason or another.

# In[5]:


# Starting with the same-ish data...
df = pd.DataFrame([
    [ 'fruit name', 'likes' ],
    [ 'apple', 15 ],
    [ 'carrot', 3 ],
    [ 'fruit name', 'likes' ],
    [ 'sweet potato', 45 ],
    [ 'peach', 12 ],
])
df


# In[6]:


df = df.rename(columns={
    0: 'fruit name',
    1: 'likes'
})
df = df[df['fruit name'] != 'fruit name']
df


# 🚀 Done!
# 
# ### Useful tips about coordinates
# 
# If you want to grab only a section of the page [Kull](https://jsoma.github.io/kull/#/) might be helpful in finding the coordinates.
# 
# > **Alternatively** run `%matplotlib notebook` in a cell. Afterwards, every time you use something like `camelot.plot(tables[0]).show()` it will get you nice zoomable, hoverable versions that include `x` and `y` coordinates as you move your mouse.
# 
# Coordinates are given as `"left_x,top_y,right_x,bottom_y"` with `(0,0)` being in the bottom left-hand corner.
# 
# Note that all coordinates are strings, for some reason. It won't be `[1, 2, 3, 4]` it will be `['1,2,3,4']`
# 
# # Camelot questions
# 
# The largest part of this assignment is **mostly Camelot work**. As tabular data is usually the most typical data you'll be working with, it's what I'm giving you!
# 
# It will probably be helpful to read through [Camelot's advanced usage tips](https://camelot-py.readthedocs.io/en/master/user/advanced.html), along with the notebook I posted in the homework assignment.
# 
# ## Prison Inmates
# 
# Working from [InmateList.pdf](InmateList.pdf), save a CSV file that includes every inmate.
# 
# * Make sure your rows are *all data*, and you don't have any people named "Inmate Name."
# 

# In[4]:


import camelot


# In[78]:


tables = camelot.read_pdf("InmateList.pdf", flavor="stream")
tables


# In[79]:


tables[0].df.head()


# In[80]:


tables = camelot.read_pdf("InmateList.pdf", flavor="stream", pages="all")
tables[15].df.tail()


# In[16]:


import pandas as pd


# In[83]:


dfs = [table.df for table in tables]
df = pd.concat(dfs, ignore_index=True)
df.tail()
df.shape


# In[87]:


df.columns = df.loc[2]
df
# Will clean up the column names in spreadsheet


# In[88]:


df = df[df['Inmate Name'] != 'Inmate Name']


# In[89]:


df.shape


# In[92]:


df = df[df['Facility'] != "Erie County Sheriff's Office"]
df.shape


# In[94]:


df = df[df['Facility'] != "Inmate Roster"]
df.shape


# In[96]:


df = df[df['ICN #'] != "Created On:"]
df.shape


# In[98]:


df.tail()


# In[103]:


df = df.reset_index(drop=True)
df


# In[104]:


df.to_csv("InmateList.csv", index=False)
# To remove rows 260 and 261 from the table and move some rows for "facility" and "dates" to the right columns


# ## WHO resolutions
# 
# Using [A74_R13-en.pdf](A74_R13-en.pdf), what ten member countries are given the highest assessments?
# 
# * You might need to have two separate queries, and combine the results: that last page is pretty awful!
# * Always rename your columns
# * Double-check that your sorting looks right......
# * You can still get the answer even without perfectly clean data

# In[226]:


tables = camelot.read_pdf("A74_R13-en.pdf", flavor="stream", pages="all")
tables 


# In[227]:


dfs = [table.df for table in tables]
df = pd.concat(dfs, ignore_index=True)
df.shape


# In[228]:


df.head()


# In[229]:


df.tail()


# In[230]:


# redo with two queries 
tables_1 = camelot.read_pdf("A74_R13-en.pdf", flavor="stream", pages="1-5")
tables_2 = camelot.read_pdf("A74_R13-en.pdf", flavor="stream", pages="6")


# In[281]:


dfs = [table.df for table in tables_1]
df = pd.concat(dfs, ignore_index=True)
df


# In[282]:


df = df.rename(columns={
    0: 'Members',
    1: 'WHO scale'
})


# In[283]:


df = df[df['Members'] != 'Members and']
df = df[df['Members'] != 'Associate Members']
df = df[df['WHO scale'] != '%']
df = df[df['Members'] != 'Democratic People’s Republic of']
df = df[df['Members'] != 'United Kingdom of Great Britain and']
df.rename(index={'Northern Ireland':'UK'},inplace=True)
df.shape


# In[256]:


# Tried cleaning the rows with places that say"not a member of the United Nations" using regex but didn't make it work. 
# But these places' WHO scale values are all very low so will ignore them. 
# Will similarly ignore the 2 countries on last page with low values


# In[289]:


# Top 10 countries with highest assessments

df=df.sort_values('WHO scale', ascending = False)
df.head(10)


# ## The Avengers
# 
# Using [THE_AVENGERS.pdf](THE_AVENGERS.pdf), approximately how many lines does Captain America have as compared to Thor and Iron Man?
# 
# * Character names only: we're only counting `IRON MAN` as Iron Man, not `TONY`.
# * Your new best friend might be `\n`
# * Look up `.count` for strings

# In[291]:


from pdfminer.high_level import extract_text
text = extract_text('THE_AVENGERS.pdf')


# In[293]:


print(text)


# In[303]:


# No. of lines for Captain America
text.count("\nCAPTAIN AMERICA")


# In[304]:


# No. of lines for Thor
text.count("\nTHOR")


# In[305]:


# No. of lines for Iron Man
text.count("\nIRON MAN")


# ## COVID data
# 
# Using [covidweekly2721.pdf](covidweekly2721.pdf), what's the total number of tests performed in Minnesota? Use the Laboratory Test Rates by County of Residence chart.
# 
# * You COULD pull both tables separately OR you could pull them both at once and split them in pandas.
# * Remember you can do things like `df[['name','age']]` to ask for multiple columns

# In[414]:


tables = camelot.read_pdf("covidweekly2721.pdf", pages="6")
tables 


# In[415]:


df = tables[1].df
df


# In[416]:


df.columns = df.loc[0]


# In[417]:


df = df.drop(0)


# In[418]:


df


# In[383]:


# I'll just save the above df to csv to merge the same columns together. 
# Spent a day looking for ways to split this damn table in the middle but didn't manage to find the right codes. Using Kull to get the table by coordinates gave a messier output.


# ## Theme Parks
# 
# Using [2019-Theme-Index-web-1.pdf](2019-Theme-Index-web-1.pdf), save a CSV of the top 10 theme park groups worldwide.
# 
# * You can clean the results or you can restrict the area the table is pulled from, up to you

# In[419]:


table = camelot.read_pdf('2019-Theme-Index-web-1.pdf', pages="11", flavor='stream', table_areas=['26,469,380,280'])
table[0].df.head(13)


# In[421]:


df = table[0].df.head(13)
df


# In[426]:


df = df.rename(columns={
    0: 'rank',
    1: 'group_name',
    2: 'percent-change',
    3: 'attendance_2019',
    4: 'attendance_2020'
})

df.to_csv("theme_park.csv", index=False)


# ## Hunting licenses
# 
# Using [US_Fish_and_Wildlife_Service_2021.pdf](US_Fish_and_Wildlife_Service_2021.pdf) and [a CSV of state populations](http://goodcsv.com/geography/us-states-territories/), find the states with the highest per-capita hunting license holders.

# In[610]:


tables = camelot.read_pdf("US_Fish_and_Wildlife_Service_2021.pdf")
tables[0].df
df1 = tables[0].df


# In[611]:


df1.columns = df1.loc[0]
df1.head()


# In[612]:


df1 = df1.drop(0)


# In[613]:


df1.head()


# In[614]:


# add encoding='latin1' to load the second file
df2 = pd.read_csv("us-states-territories.csv", encoding='latin1') 


# In[615]:


df2.head()
df2.describe()


# In[616]:


# Wonder why this code doesn't work in merging the two data sets 
# keeps getting keyError for "State". Only the DC row is merged
df1.merge(df2, left_on='State', right_on='Abbreviation')


# In[617]:


# try merging again by deleting the first column "Type"
df2 = df2.drop(['Type'], axis=1)


# In[618]:


df2.head(10)


# In[619]:


merged = df1.join(df2, lsuffix='State', rsuffix='Abbreviation')
# Why doin join work but not merge???


# In[620]:


merged.head()


# In[621]:


merged = merged.rename(columns={
    "Paid Hunting License \nHolders*": "license_holders",
    "Population (2019)": "population"
})


# In[645]:


# the states with the highest per capita hunting licence holders
# sort values after dividing the number of "Paid hunting licence holders" by "Population (2019)"
# realise division doesn't work because the numbers are in string
# realise the string cannot be converted to integer because of thousand separators
# so saving the file first and reopen with thousands=","

hunting = merged.to_csv("hunting.csv", index=False)


# In[649]:


hunting = pd.read_csv("hunting.csv", thousands=',')
hunting.head()


# In[653]:


hunting["license_holders"].astype(int)


# In[655]:


hunting["population"].astype(float)


# In[658]:


hunting["per_capita"] = hunting["license_holders"]/hunting["population"] *100000


# In[659]:


hunting["per_capita"]


# In[662]:


sorted = hunting.sort_values(by="per_capita", ascending=False)


# In[666]:


# Top 10 states with highest number of hunting licence holders per 100,000 people
sorted[['Name','per_capita']].head(10)


# # Not-Camelot questions
# 
# You can answer these without using Camelot.

# ## Federal rules on assault weapons
# 
# Download all of the PDFs from the Bureau of Alcohol, Tobacco, Firearms and Explosives's [Rules and Regulations Library](https://www.atf.gov/rules-and-regulations/rules-and-regulations-library). Filter for a list of all PDFs that contain the word `assault weapon` or `assault rifle`.
# 
# > If you're having trouble scraping, maybe someone will be kind enough to drop a list of PDF urls in Slack?

# In[749]:


import requests
from bs4 import BeautifulSoup

response = requests.get("https://www.atf.gov/rules-and-regulations/rules-and-regulations-library")
doc = BeautifulSoup(response.text)


# In[750]:


links = doc.select("a[href$='download']")


# In[751]:


# just scraping the first page of the website

urls = []
for link in links:
    url = "https://www.atf.gov" + link['href']
    urls.append(url)
urls


# In[773]:


# hey! join together all of these urls
# by putting a new line between each of them
file_content = '\n'.join(urls)

# Write all of that content to a file
with open("urls.txt", "w") as f:
    f.write(file_content)


# In[777]:


file_content


# In[ ]:


# not sure how to proceed


# ## New immigration judge training materials
# 
# Extract the text from [this 2020 guide for new immigration judges](2020-training-materials-2a-201-300.pdf) and save it as a file called `training-material.txt`.
# 
# > I took this PDF from [a FOIA request](https://www.muckrock.com/foi/united-states-of-america-10/most-recent-new-immigration-judge-training-materials-120125/#comms) – but the unfortunate thing is *I actually had to remove the OCR layer to make it part of this assignment*. By default everything that goes through Muckrock gets all of the text detected!

# In[693]:


get_ipython().system('pip install pytesseract')
import pytesseract


# In[694]:


pip install --upgrade pip


# In[696]:


# This doesn't work 
# text = pytesseract.image_to_string('2020-training-materials-2a-201-300.pdf')


# In[698]:


# !brew install --cask adoptopenjdk


# In[699]:


# !pip install tika


# In[700]:


import tika
from tika import parser


# In[701]:


# also doesn't work
# parsed = parser.from_file("2020-training-materials-2a-201-300.pdf")
# parsed.keys()
# parsed["content"]
# stext = print(parsed["content"])


# In[705]:


get_ipython().system('pip install pdfplumber')
import pdfplumber


# In[711]:


# also doesn't work

# a single page
# with pdfplumber.open(r'2020-training-materials-2a-201-300.pdf') as pdf:
    first_page = pdf.pages[-0]
    print(first_page.extract_text())
    
# for every page
# with pdfplumber.open(r'test.pdf') as pdf:
#     for pages in pdf.pages:
#         print(pages.extract_text())


# In[712]:


get_ipython().system('pip install opencv-python')


# In[ ]:




