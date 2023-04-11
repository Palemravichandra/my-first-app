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
- Creating application by using [streamlit](https://docs.streamlit.io/library/api-reference)
- scrape the twitter data using snscrape module
# if we want to upload the data to mongodb 
- create connection with mongodb using pymongo
- create the database and create collection name as searchkey with datetimestamp
- mongodb stores data in the form of JSON so convert the data into json format
- store the json data into the collection
# if we want to download the data
- select the option yes in text box
- then it will displays the formats CSV,JSON format Radio buttons
- select the format and click on download button and download the data
#  **To run the app**
- create the `.py` file on on your IDE and store the above code on the file and save it.Lets say example we save `project.py` file saved in desktop
- open the `commandprompt`. command prompt intiatially opens `C:\Users\Admin>`but our document stored in desktop.
- So in order to create path for file write command `cd desktop` it will create path for desktop`C:\Users\Admin\Desktop>`
- Then run the file by using `streamlit run` command i.e. `streamlit run project.py`, it will takes you to the app
#  Or
- you can directly run in run in teminal by writing the command `streamlit run <filepath><filename>`
