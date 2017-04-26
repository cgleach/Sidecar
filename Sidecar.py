# Python project to analysis dummy dataset for Sidecar; goal is to ascertain high level trends
# and key buiness insights

import pandas as pd
import numpy as np
import math as math
import plotly
import plotly.plotly as py
from plotly.graph_objs import *

plotly.tools.set_config_file(world_readable=True, sharing='public')  # set plotly parameters for graphing

# define initial variables
x = 0
y = 0
CPC = []
CTR = []
svquartile = []
quartilelookup = []

# define functions to calculate cost per click and click through; functions allow for error handling
def CPC_calc(costAd, Adclicks):
    try:
        return float(costAd) / float(Adclicks)
    except ZeroDivisionError:
        return np.nan


def CTR_calc(Adclicks, Adimpressions):
    try:
        return int(Adclicks) / int(Adimpressions)
    except ZeroDivisionError:
        return np.nan


df = pd.read_csv("sidecar_product_analyst_challenge_data.csv", parse_dates=['date'])
df['DayWeek'] = df['date'].dt.weekday_name

#calculates CPC and CTR using previously defined functions before adding to original dataframe
while x < len(df):
    CPC.append(CPC_calc(df.ix[x, 'cost'], df.ix[x, 'clicks']))
    CTR.append(CTR_calc(df.ix[x, 'clicks'], df.ix[x, 'impressions']))
    x = x + 1

df['CPC'] = CPC
df['CTR'] = CTR

#Creates new dataframes groupecd by site
Aggdf = df.groupby('site_id').sum().reset_index()
Avgdf = df.groupby('site_id').mean().reset_index()
Avgdf['weightedcr']= Aggdf['channel_orders']/Aggdf['clicks']

#Creates new dataframes grouped by site and weekday
Daywkagg = df.groupby(['site_id', 'DayWeek']).sum().reset_index()
Daywkavg = df.groupby(['site_id', 'DayWeek']).mean().reset_index()
Daywkavg['weightedCR'] = Daywkagg['channel_orders'] / Daywkagg['clicks']

# avg site views   25%=1452    50%=4763    75%=15603   from print(Avgdf.describe())
while y < len(Avgdf):                         #Creates list of quartile rankings before adding to dataframe
    if Avgdf.ix[y, 'site_views'] < 1452:
        svquartile.append(1)
        y = y + 1
    elif Avgdf.ix[y, 'site_views'] < 4763:
        svquartile.append(2)
        y = y + 1
    elif Avgdf.ix[y, 'site_views'] < 15603:
        svquartile.append(3)
        y = y + 1
    else:
        svquartile.append(4)
        y = y + 1

Avgdf['quartilerank'] = svquartile

# Creates scatter plot showing conversion rate by site view quartiles
Plot = Scatter(
    x=Avgdf['quartilerank'],
    y=Avgdf['weightedcr'],
    mode='markers',

)

trace = [Plot]

py.iplot(trace, filename='crxquartile')

print('finished')