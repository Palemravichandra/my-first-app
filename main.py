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

#adding title to the app
st.title(':violet[Twitter Scrapping]')

# Initialize connection with mongoDB
# Uses st.experimental_singleton to only run once.
@st.cache_resource
#def init_connection():
    #return MongoClient('localhost', 27017)


#client = init_connection()

# Passing the arguments for scraping i.e. name of key ,staring date ,ending date and number of records
def collect_twitter_data(search_keys,start_date_str,end_date_str,search_count):
# Creating list to appendtweet data
    tweets_list = []

 # Using TwitterSearchScrapper to scrape data and append tweets to list
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper("{keyword} since:{end_date} until:{start_date}".format(keyword=search_keys,start_date=start_date_str,end_date=end_date_str)).get_items()):
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
    #data = tweets_df.to_dict(orient='records')
    return tweets_df

def upload_data(search_key):
    client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
    df=collect_twitter_data(search_keywords, endd_date_inp, start_date_inp,search_count)
# creating database DW35
    db = client['Twitterscrapping']
# Creating 'Scrapefromtwitter' collection in 'DW35' database
    time_stamp=datetime.datetime.now()
    collection = db[f"{search_keywords} {time_stamp}"]
# converting dataframe to json files
    data = df.to_dict(orient='records')
    # Inserting documents into collection
    #collection.insert_one(data)
    collection.insert_one({"index": f"{search_keywords} {start_date}", "data": data})

# Creating search buttoons
search_keywords = st.text_input("Search")
search_count = st.text_input("Count")
if search_count:
    search_count = int(search_count)
start_date = datetime.date.today()
endd_date_str = start_date.strftime("%Y-%m-%d")
end_date = start_date - datetime.timedelta(days=100)
start_date_str = end_date.strftime("%Y-%m-%d")

# Creating
start_date_inp = st.date_input("Start Date").strftime("%Y-%m-%d") or start_date_str
endd_date_inp = st.date_input("End Date").strftime("%Y-%m-%d") or endd_date_str


# scrapping  data from twitter
search_button = st.button('Search')
if search_button:
    tweets_df = collect_twitter_data(search_keywords, endd_date_inp, start_date_inp,search_count)
    st.subheader(':violet[first 10 records will be displayed here]')
    st.dataframe(tweets_df.iloc[0:10])

submit_button=st.button('Upload to MONGODB')
if submit_button:
    upload_data(search_keywords)
    st.success(f'{search_keywords} data is successfully uploaded to MongoDB')

tweets_df=collect_twitter_data(search_keywords, endd_date_inp, start_date_inp,search_count)
download = st.selectbox('Want to download the File :', ['No','Yes'])
if download=='Yes':
    choice = st.radio('Select file format:', ['CSV', 'JSON'],horizontal=True)
    if choice == 'CSV':
        st.download_button(
               label="Download CSV",
                file_name=f"{search_keywords}.csv",
                mime="text/csv",
                data=tweets_df.to_csv()
            )
        st.success('CSV file is downloading .......')
    else:
         st.download_button(
                label="Download JSON",
                file_name=f"{search_keywords}.json",
                mime="application/json",
                data=tweets_df.to_json()
            )
         st.success('Json file downloading ......')
else:
    st.subheader(':violet[Have a good day and Thanks for visiting]')

    
