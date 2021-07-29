#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 22:58:35 2021

@author: chasebrown
"""


import mysql.connector as connector
import yfinance as yf
from cryptocmd import CmcScraper
import json
import datetime


#Read in and return stock data
def getStockData():
    stockData = []
    with open('/Volumes/My Data/Time Series Data/Twitter Data/stockInformation.json') as jsonFile:
        stockData = json.load(jsonFile)
    return stockData

mydb = connector.connect(
      host="localhost",
      user="root",
      password="password", 
      database="twitter"
    )
reader = mydb.cursor()

mydb2 = connector.connect(
      host="localhost",
      user="root",
      password="password", 
      database="twitter"
    )
writer = mydb2.cursor()


namechange = {'Symbol': 'tickers', 'CompanyName': 'names', 'Sector': 'sectors'}
data = getStockData()
for item in data:
    i='Symbol'
    sql = """SELECT datetime, happy, angry, surprise, sad, fear, sentiment, sentimentScore
        FROM tweetSentiment WHERE """ + namechange[i] + """ LIKE '%""" + item[i].replace(' ', '').replace('&','').replace('-','') + """%' 
        ORDER BY datetime ASC;"""
    reader.execute(sql)
    try:
        writer.execute("""CREATE TABLE """ + item[i].replace(' ', '').replace('&','').replace('-','') + """_stockSentimentDayAfter(    
                          datetime VARCHAR(255) NOT NULL,
                          open FLOAT, 
                          high FLOAT, 
                          low FLOAT, 
                          close FLOAT, 
                          percentChange FLOAT,
                          percentChangeABS FLOAT,
                          volume BIGINT,   
                          tweetVolume BIGINT,
                          happy FLOAT, 
                          angry FLOAT, 
                          surprise FLOAT, 
                          sad FLOAT, 
                          fear FLOAT, 
                          sentimentScore FLOAT, 
                          PRIMARY KEY ( datetime ));""")
        mydb2.commit()
    except:
        pass
    df = yf.download(item['Symbol'],'2019-05-03','2021-01-06')
    if df.empty:
        try:
            scraper = CmcScraper(item['Symbol'], "05-03-2019", "01-06-2021")
            df = scraper.get_dataframe()
            df = df.set_index('Date')
        except:
            print("No data for ", item['Symbol'])
    try:
        for day in df.iterrows():
                    sql = "INSERT INTO " + item[i].replace(' ', '').replace('&','').replace('-','') + "_stockSentimentDayAfter (datetime, open, high, low, close, percentChange, percentChangeABS, volume) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                    val = (str(day[0]), 
                           float(day[1]['Open']), 
                           float(day[1]['High']), 
                           float(day[1]['Low']), 
                           float(day[1]['Close']),
                           (float(day[1]['Close']) - float(day[1]['Open']))/float(day[1]['Open']),
                           abs(float(day[1]['Close']) - float(day[1]['Open']))/float(day[1]['Open']),
                           int(day[1]['Volume']))
                    writer.execute(sql, val)
        mydb2.commit()
    except:
        pass
    
    sql = "INSERT INTO " + item[i].replace(' ', '').replace('&','').replace('-','') + "_stockSentimentDayAfter (datetime, tweetVolume, happy, angry, surprise, sad, fear, sentimentScore) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)  ON DUPLICATE KEY UPDATE tweetVolume=%s, happy=%s, angry=%s, surprise=%s, sad=%s, fear=%s, sentimentScore=%s"
    last = ''
    positive = 0
    negative = 0
    happy = 0
    angry = 0
    surprise = 0
    sad = 0
    fear = 0
    count = 0
    checkUnique = ""
    for x in reader:
        if (not x[0].split(" ")[0] == last) and count>0:
            year,month,day = last.split('-')
            d = datetime.date(int(year), int(month), int(day))
            d = d - datetime.timedelta(days=1)
            val = (str(str(d) + " 00:00:00"), 
                 str(count), 
                 str(happy/count), 
                 str(angry/count), 
                 str(surprise/count), 
                 str(sad/count), 
                 str(fear/count), 
                 str(positive/count) if positive/count >= .5 else str(1 - negative/count),
                 str(count), 
                 str(happy/count), 
                 str(angry/count), 
                 str(surprise/count), 
                 str(sad/count), 
                 str(fear/count), 
                 str(positive/count) if positive/count >= .5 else str(negative/count))
            writer.execute(sql, val)
            mydb2.commit()
            positive = 0
            negative = 0
            count = 0
            happy = 0
            angry = 0
            surprise = 0
            sad = 0
            fear = 0
        happy += x[1]
        angry += x[2]
        surprise += x[3]
        sad += x[4]
        fear += x[5]
        
        if x[6] == "POSITIVE":
            positive += float(x[7])
            negative += 1 - float(x[7])
        else:
            positive += 1 - float(x[7])
            negative += float(x[7])
        count += 1
        last = x[0].split(" ")[0]

def clearAll():
    data = getStockData()
    mydb = connector.connect(
      host="localhost",
      user="root",
      password="password", 
      database="twitter"
    )
    writer = mydb.cursor()
    mydb2 = connector.connect(
      host="localhost",
      user="root",
      password="password", 
      database="twitter"
    )
    reader = mydb2.cursor()
    reader.execute("SHOW TABLES;")
    for table in reader:
        if '_stockSentimentDay' in table[0]:
            writer.execute("DROP TABLE " + table[0] + ";")
            mydb.commit()
    writer.close()
    reader.close()
    mydb.close()
    mydb2.close()
#clearAll()




            
            
            
            
            
            
            
            