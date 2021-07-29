#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 21:44:35 2021

@author: chasebrown
"""


from os import path
import datetime
import mysql.connector
import pandas as pd
import plotly.graph_objects as go
from plotly.offline import download_plotlyjs, init_notebook_mode,  plot
import plotly.express as px


mydb = mysql.connector.connect(
  host="localhost",
  user="admin",
  password="", 
  database="twitter"
)

mycursor = mydb.cursor()



def makeString(integer):
    string = str(integer)
    if len(string) == 1:
        string = "0" + string
    return string

def getData():
    workingDirectory = "/Volumes/My Data/Time Series Data/Twitter Data/"
    
    start_date = datetime.date(2020, 1, 1)
    end_date = datetime.date(2021, 12, 31)
    delta = datetime.timedelta(days=1)
    
    found = {}
    while start_date <= end_date:
        year = makeString(start_date.year)
        month = makeString(start_date.month)
        day = makeString(start_date.day)
        dateString = year + '-' + month + '-' + day
        found.update({dateString: []})
        for hour in range(0,24):
            hour = makeString(hour)
            currentPath = workingDirectory + year + "/" + month + "/" + day + "/" + hour
            if path.isdir(currentPath):
                for minute in range(0,60):
                    minute = makeString(minute)
                    currentPath = workingDirectory + year + "/" + month + "/" + day + "/" + hour + "/" + minute + '.json.bz2'
                    if path.exists(currentPath):
                        found[dateString].append(hour + ':' + minute)
            else:
                for minute in range(0,60):
                    minute = makeString(minute)
        start_date += delta
    return found

found = getData()

plotData = {'Date':[], 'percentFound':[]}
for i in found.keys():
    plotData["Date"].append(i)
    plotData["percentFound"].append(len(found[i])/1440)

df = pd.DataFrame(plotData)
# Create figure
fig = go.Figure()

fig = px.scatter(df, x="Date", y="percentFound", color="percentFound")

# Set title

fig.update_traces(marker=dict(size=12,
                              line=dict(width=2,
                                        color='DarkSlateGrey')),
                  selector=dict(mode='markers'))

# Add range slider
fig.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label="1m",
                     step="month",
                     stepmode="backward"),
                dict(count=6,
                     label="6m",
                     step="month",
                     stepmode="backward"),
                dict(count=1,
                     label="YTD",
                     step="year",
                     stepmode="todate"),
                dict(count=1,
                     label="1y",
                     step="year",
                     stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(
            visible=True
        ),
        type="date"
    )
)
plot(fig)
