# This is my Twitter-Scrapping project

## Importing required libraries
```python
import streamlit as st
from pymongo import MongoClient
import snscrape.modules.twitter as sntwitter
import pandas as pd
import datetime
import json
```
# Creating page  by using [streamlit](https://docs.streamlit.io/library/api-reference)configuration with the project name

```python
st.set_page_config(
        page_title="Twitter Scrapping",
)
st.header = "Twitter Scraping"
```
# Adding title to the web page

```python
st.title('Twitter Scrapping')
```
# To cache the output of a function ,so that it only needs to be executed once we use command called

```python
@st. experimental_singleton 
```

# Initializing connection with mongodb

```python
@st.experimental_singleton
def init_connection():
    return MongoClient('localhost', 27017)
client = init_connection()
```

# Passing the arguments for scrapping data from twitter
```python
def collect_twitter_data(search_keys,start_date_str,end_date_str,search_count):
    try:
```

# Creating list to store the retreived data

```python
tweets_list = []
```

# Retreiving data from twitter by using ```TwitterSearchScrapper```[snscrape library](https://medium.com/dataseries/how-to-scrape-millions-of-tweets-using-snscrape-195ee3594721) and append the data to tweetslist

```python
for i, tweet in enumerate(sntwitter.TwitterSearchScraper("{keyword} since:{end_date} until:{start_date}".format(keyword=search_keys,start_date=start_date_str,end_date=end_date_str)).get_items()):
            if i > search_count:
                break
            tweets_list.append(
                [tweet.date, tweet.id, tweet.url, tweet.content, tweet.replyCount, tweet.retweetCount, tweet.lang,
                 tweet.source, tweet.likeCount])
```
# If we want to see the tweets_list

```python
print(tweets_list)
```
# Creating Dataframe of  from tweets list
```python
tweets_df = pd.DataFrame(tweets_list,
                                 columns=['DateTime', 'User_ID', 'URL', 'Tweet_content', 'Reply_count', 'Retweet_count',
                                          'language', 'source', 'like_count'])
```
#  Mongodb stores data in document formatso we will convert data into document format[mongodb](https://docs.google.com/document/d/1inK3CTUDMcaNuPEN5aX_RD4ttKF2ogY_/edit)

```python
 data = tweets_df.to_dict(orient='record')
        return data,tweets_df
    except Exception as e:
        raise Exception(str(e))

def download_records(st):
    data = json.dumps(st,default=str)
    return data
```
# To upload the data to mongodb database `DW35` and creating collection name as `uploadsof scrapefromtwitter` and storing documents into collection
```python
def upload_data(data):
    try:
        if data:
            db = client['DW35']

            # Creating 'Scrapefromtwitter' collection in 'DW35' database
            collection = db['UploadsOfScrapefromtwitter']
            # Inserting documents into collection
            collection.insert_one(data)
    except Exception as e:
        raise Exception(str(e))
def get_csv_data(df):
    return df.to_csv(index=False).encode("utf-8")
```
# Creating button by using streamlit for taking input from user i.e.name of keyword in the app
```python
search_keywords = st.text_input("Search")
try:
    search_count = st.text_input("Count") or 10
    if search_count:
        search_count = int(search_count)
except Exception as e:
    search_count = 10
start_date = datetime.date.today()
endd_date_str = start_date.strftime("%Y-%m-%d")
end_date = start_date - datetime.timedelta(days=100)
start_date_str = end_date.strftime("%Y-%m-%d")
```
# Creating buttons using streamlit for take the input dates range from start date to end date
```python
start_date_inp = st.date_input("Start Date").strftime("%Y-%m-%d") or start_date_str
endd_date_inp = st.date_input("End Date").strftime("%Y-%m-%d") or endd_date_str
```
# Displaying data which satisfies all the conditions
```python
if search_keywords:
    items,tweets_df = collect_twitter_data(search_keywords, endd_date_inp, start_date_inp,search_count)
    for item in items:
        st.write(item)
    start_date = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    data = {search_keywords + start_date :items}
```

# Creating button to download the data in json format
```python
st.download_button(label="Download Json",data=download_records(items),file_name="sample.json")
```
# Creating button to download the data in the csv format
```python
st.download_button("Download CSV",get_csv_data(tweets_df),"sample.csv","text/csv",key="download0-csv")
```
# Creating button to the data upload the retreived data to database mongodb
```python
st.button(label="Upload",on_click=upload_data(data))
```

# All the above code is displayed once

```python
# importing required packages
import streamlit as st
from pymongo import MongoClient
import snscrape.modules.twitter as sntwitter
import pandas as pd
import datetime
import json

# creating page configuration
st.set_page_config(
        page_title="Twitter Scrapping",
)
st.header = "Twitter Scraping"

# Adding title to the app
st.title('Twitter Scrapping')

# Initialize connection with mongoDB
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
    return MongoClient('localhost', 27017)


client = init_connection()

# Passing the arguments for scraping i.e. name of key ,staring date ,ending date and number of records
def collect_twitter_data(search_keys,start_date_str,end_date_str,search_count):
    try:
        # Creating list to appendtweet data
        tweets_list = []
        for i, tweet in enumerate(sntwitter.TwitterSearchScraper("{keyword} since:{end_date} until:{start_date}".format       (keyword=search_keys,start_date=start_date_str,end_date=end_date_str)).get_items()):
            if i > search_count:
                break
            tweets_list.append(
                [tweet.date, tweet.id, tweet.url, tweet.content, tweet.replyCount, tweet.retweetCount, tweet.lang,
                 tweet.source, tweet.likeCount])

        # To see the tweets_list
        # print(tweets_list)

        # Creating dataframe from tweets list above
        tweets_df = pd.DataFrame(tweets_list,
                                 columns=['DateTime', 'User_ID', 'URL', 'Tweet_content', 'Reply_count', 'Retweet_count',
                                          'language', 'source', 'like_count'])
        data = tweets_df.to_dict(orient='record')
        return data,tweets_df
    except Exception as e:
        raise Exception(str(e))

def download_records(st):
    data = json.dumps(st,default=str)
    return data

def upload_data(data):
    try:
        if data:
            db = client['DW35']

            # Creating 'Scrapefromtwitter' collection in 'DW35' database
            collection = db['UploadsOfScrapefromtwitter']
            # Inserting documents into collection
            collection.insert_one(data)
    except Exception as e:
        raise Exception(str(e))

def get_csv_data(df):
    return df.to_csv(index=False).encode("utf-8")

# Creating search button
search_keywords = st.text_input("Search")
try:
    search_count = st.text_input("Count") or 10
    if search_count:
        search_count = int(search_count)
except Exception as e:
    search_count = 10
start_date = datetime.date.today()
endd_date_str = start_date.strftime("%Y-%m-%d")
end_date = start_date - datetime.timedelta(days=100)
start_date_str = end_date.strftime("%Y-%m-%d")

# Creating buttons for to take starting date,ending date
start_date_inp = st.date_input("Start Date").strftime("%Y-%m-%d") or start_date_str
endd_date_inp = st.date_input("End Date").strftime("%Y-%m-%d") or endd_date_str


# scrapping  data from twitter
if search_keywords:
    items,tweets_df = collect_twitter_data(search_keywords, endd_date_inp, start_date_inp,search_count)
    for item in items:
        st.write(item)
    start_date = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    data = {search_keywords + start_date :items}
    # Creating button to download the data in json format
    st.download_button(label="Download Json",data=download_records(items),file_name="sample.json")
    # Creating button to download the data in csv format
    st.download_button("Download CSV",get_csv_data(tweets_df),"sample.csv","text/csv",key="download0-csv")
    # Creating button to upload the data retrieved from twitter to mongodb database
    st.button(label="Upload",on_click=upload_data(data))
```
#  **To run the app**
- create the `.py` file on on your IDE and store the above code on the file and save it.Lets say example we save `project.py` file saved in desktop
- open the `commandprompt`. command prompt intiatially opens `C:\Users\Admin>`but our document stored in desktop.
- So in order to create path for file write command `cd desktop` it will create path for desktop`C:\Users\Admin\Desktop>`
- Then run the file by using `streamlit run` command i.e. `streamlit run project.py`, it will takes you to the app
#  Or
- you can directly run in run in teminal by writing the command `streamlit run <filepath><filename>`