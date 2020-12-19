# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from IPython import get_ipython

# %% [markdown]
# **The purpose of this analysis is strictly to focus on the 2008 Financial Crisis. We will deep dive into exploratory analysis to see what major banks failed first and which ones survived. We will also take a look at some intersting grpahing techniques related to finance.**

# %%
#importing in all necessary modules
try:
    from pandas_datareader import data, wb
    import pandas as pd
    import numpy as np
    import datetime
    import seaborn as sns
    import pandas_datareader.data as web
    get_ipython().run_line_magic('matplotlib', 'inline')
    print("Imported!")
except: 
    print("Not imported")


# %%
#creating datetime variables for reference
start = datetime.datetime(2006, 1, 1)
end = datetime.datetime(2018, 1, 1)


# %%
#Referencing the 'Stooq.com' datareader API. Docs --> "https://pandas-datareader.readthedocs.io/en/latest/readers/stooq.html"

import pandas_datareader.data as web
BofA = web.DataReader('BAC', 'stooq', start, end)

Citi = web.DataReader('C', 'stooq', start, end)

Goldman = web.DataReader('GS', 'stooq', start, end)

JpMorgan = web.DataReader('JPM', 'stooq', start, end)

MorganS = web.DataReader('MS', 'stooq', start, end)

WellsF = web.DataReader('WFC', 'stooq', start, end)


# %%
tickers = ['BAC', 'C', 'GS', 'JPM', 'MS', 'WFC']


# %%
bank_stocks = pd.concat([BofA, Citi, Goldman, JpMorgan, MorganS, WellsF], axis=1, keys=tickers)


# %%
#sorting data from oldest to newest dates
bank_stocks = bank_stocks.sort_index(ascending=True)
bank_stocks.head()


# %%
#Creating a multilayered dataframe
bank_stocks.columns.names = ['Bank Ticker','Stock Info']


# %%
bank_stocks.head()


# %%
#for tick in tickers:
    #print(tick, bank_stocks[tick]['Close'].max())
    
#XS to cross splice data sets    
bank_stocks.xs(key='Close', axis=1, level='Stock Info').max()


# %%
#Capturing the returns of each ticker
returns = pd.DataFrame()


# %%
for tick in tickers: 
    returns[tick+' Return'] = bank_stocks[tick]['Close'].pct_change()
returns.head()


# %%
#returns a pair plot of our return dataframe at index 1
#May take a few minutes depending on size of data
sns.pairplot(returns[1:])


# %%
#shows lowest returns from start to end
returns.idxmin()


# %%
#shows Highest returns from start to end
returns.idxmax()


# %%
#Highest volatility of stocks
(returns.std().idxmax)


# %%
#returns volatility from certain time frame
returns.loc['2015-01-01':'2015-12-31'].std()


# %%
sns.distplot(returns.loc['2015-01-01':'2015-12-31']['MS Return'],color= 'green', bins=50)


# %%
sns.distplot(returns.loc['2015-01-01':'2015-12-31']['C Return'], bins = 50, color = 'red', label='Returns of Citi')


# %%
#importing modules necessary for graphing
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')
get_ipython().run_line_magic('matplotlib', 'inline')

# Optional Plotly Method Imports
import plotly
import cufflinks as cf
cf.go_offline()


# %%
for tick in tickers:
    bank_stocks[tick]['Close'].plot(label=tick, figsize=(16,6))
plt.legend()


# %%
bank_stocks.xs(key='Close', axis=1, level='Stock Info').iplot()


# %%
#Correlation heatmap of banks
sns.heatmap(bank_stocks.xs(key='Close', axis=1, level='Stock Info').corr(),annot=True)


# %%
#cluster mapping the banks together
sns.clustermap(bank_stocks.xs(key='Close', axis=1, level='Stock Info').corr(),annot=True)


# %%
#interactive version of heatmap
close_corr = (bank_stocks.xs(key='Close', axis=1, level='Stock Info').corr())
close_corr.iplot(kind='heatmap', colorscale = 'rdylbu')


# %%
#shows candle stick representation of data
BAC_15 = BofA[['Open', 'High', 'Low', 'Close']].loc[BofA.index[2900:3020].sort_values(ascending=True)]
BAC_15.iplot(kind = 'candle')


# %%
#Simple Moving Average (SME) plot for closes fo 12, 21, and 55 days
MorganS['Close'].loc[MorganS.index[600:900].sort_values(ascending=True)].ta_plot(study='sma', periods = [12,21,55])


# %%
#displays SME but will bollinger bands
MorganS['Close'].loc[MorganS.index[600:900].sort_values(ascending=True)].ta_plot(study='boll')


