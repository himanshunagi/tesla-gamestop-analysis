#!/usr/bin/env python
# coding: utf-8

# In[2]:


import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# In[3]:


def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data.Date, infer_datetime_format=True), y=stock_data.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data.Date, infer_datetime_format=True), y=revenue_data.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()


# In[7]:


tesla_data = yf.Ticker('TSLA')


# In[8]:


tesla_data.info


# In[9]:


tesla_data = tesla.history(period="max")


# In[10]:


tesla_data.reset_index(inplace=True)
tesla_data.head()


# In[11]:


url = 'https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue'
html_data = requests.get(url).text


# In[12]:


soup = BeautifulSoup(html_data,"html5lib")


# In[13]:


tesla_revenue = pd.DataFrame(columns=['Date', 'Revenue'])

for table in soup.find_all('table'):
    if 'Tesla Quarterly Revenue' in table.find('th').text:
        rows = table.find_all('tr')
        
        for row in rows:
            cols = row.find_all('td')
            
            if cols:
                date = cols[0].text
                revenue = cols[1].text.replace(',', '').replace('$', '')

                tesla_revenue = pd.concat([tesla_revenue, pd.DataFrame({"Date": [date], "Revenue": [revenue]})], ignore_index=True)


# In[14]:


tesla_revenue


# In[15]:


tesla_revenue = tesla_revenue[tesla_revenue['Revenue'].astype(bool)]


# In[16]:


tesla_revenue.tail()


# In[17]:


gme = yf.Ticker('GME')


# In[18]:


gme_data = gme.history(period='max')


# In[19]:


gme_data.reset_index(inplace=True)
gme_data.head()


# In[20]:


url = 'https://www.macrotrends.net/stocks/charts/GME/gamestop/revenue'
html_data = requests.get(url).text


# In[21]:


soup = BeautifulSoup(html_data,"html5lib")


# In[22]:


import pandas as pd

gme_revenue = pd.DataFrame(columns=['Date', 'Revenue'])

for table in soup.find_all('table'):
    if 'GameStop Quarterly Revenue' in table.find('th').text:
        rows = table.find_all('tr')
        
        for row in rows:
            cols = row.find_all('td')
            
            if cols:
                date = cols[0].text
                revenue = cols[1].text.replace(',', '').replace('$', '')

                gme_revenue = pd.concat([gme_revenue, pd.DataFrame({"Date": [date], "Revenue": [revenue]})], ignore_index=True)


# In[23]:


gme_revenue.tail()


# In[24]:


make_graph(tesla_data[['Date','Close']], tesla_revenue, 'Tesla')


# In[25]:


make_graph(gme_data[['Date','Close']], gme_revenue, 'GameStop')


# In[ ]:




