#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 18 15:55:57 2021

@author: chasebrown
"""

import mysql.connector
import csv
import yfinance as yf
import datetime


mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="password", 
      database="twitter"
    )
reader = mydb.cursor()

mydb2 = mysql.connector.connect(
      host="localhost",
      user="root",
      password="password", 
      database="twitter"
    )
writer = mydb2.cursor()

reader.execute("SELECT DISTINCT tickers from tweetSentimentCurrent;")
stocks = []
for i in reader:
    stocks.append(i[0])

for stock in stocks:
    sql = """SELECT *
            FROM tweetSentimentCurrent WHERE tickers='""" + stock + """' 
            ORDER BY datetime ASC;"""
    reader.execute(sql)
    try:
        writer.execute("""create table """ + stock + """_hourlySentiment(    
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
    except Exception as e:
        print(stock + "_hourlySentiment", e)
    df = yf.download(stock,interval = '30m', start = '2021-04-06',end = '2021-04-24')
    try:
        for day in df.iterrows():
            dateTime = '-'.join(str(day[0]).split('-')[:-1])
            if(dateTime.split(':')[-2]) == '00':
                sql = "INSERT INTO " + stock + "_hourlySentiment (datetime, open, high, low, close, percentChange, percentChangeABS, volume) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                val = (dateTime, 
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
    sql = "INSERT INTO " + stock + "_hourlySentiment (datetime, tweetVolume, happy, angry, surprise, sad, fear, sentimentScore) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)  ON DUPLICATE KEY UPDATE tweetVolume=%s, happy=%s, angry=%s, surprise=%s, sad=%s, fear=%s, sentimentScore=%s"
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
        x = x[1:]
        if (not x[0].split(":")[-3] == last) and count>0:
            d = x[0].split(":")[-3]
            val = (str(str(d) + ":00:00"), 
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
        happy += x[2]
        angry += x[3]
        surprise += x[4]
        sad += x[5]
        fear += x[6]
        
        if x[7] == "POSITIVE":
            positive += float(x[8])
            negative += 1 - float(x[8])
        else:
            positive += 1 - float(x[8])
            negative += float(x[8])
        count += 1
        last = x[0].split(":")[-3]
    
def clearAll():
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
        if '_hourlySentiment' in table[0]:
            writer.execute("DROP TABLE " + table[0] + ";")
            mydb.commit()
    writer.close()
    reader.close()
    mydb.close()
    mydb2.close()
#clearAll()

