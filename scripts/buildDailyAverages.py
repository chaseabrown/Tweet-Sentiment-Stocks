#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 22:58:35 2021

@author: chasebrown
"""


import mysql.connector
import csv

#Read in and return stock data
def getStockData():
    stockData = []
    titles = ['Symbol', 'CompanyName', 'Sector', 'cap']
    with open('/Volumes/My Data/Time Series Data/Twitter Data/stockInformation.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                stockData.append(dict(zip(titles, row)))
                line_count += 1
    return stockData

mydb = mysql.connector.connect(
      host="localhost",
      user="admin",
      password="", 
      database="twitter"
    )
reader = mydb.cursor()

mydb2 = mysql.connector.connect(
      host="localhost",
      user="admin",
      password="", 
      database="twitter"
    )
writer = mydb2.cursor()

namechange = {'Symbol': 'tickers', 'CompanyName': 'names', 'Sector': 'sectors'}
data = getStockData()
for item in data:
    for i in ['Symbol', 'CompanyName', 'Sector']:
        sql = """SELECT datetime, happy, angry, surprise, sad, fear, sentiment, sentimentScore
            FROM tweetSentiment WHERE """ + namechange[i] + """ LIKE '%""" + item[i].replace(' ', '').replace('&','').replace('-','') + """%' 
            ORDER BY datetime ASC;"""
        reader.execute(sql)
        try:
            writer.execute("""create table """ + item[i].replace(' ', '').replace('&','').replace('-','') + """_dailySentiment(    
                              eventID INT NOT NULL AUTO_INCREMENT,    
                              datetime TEXT NOT NULL, 
                              tweetVolume TEXT NOT NULL,
                              happy FLOAT, 
                              angry FLOAT, 
                              surprise FLOAT, 
                              sad FLOAT, 
                              fear FLOAT, 
                              sentiment VARCHAR(100) NOT NULL, 
                              sentimentScore FLOAT NOT NULL, 
                              PRIMARY KEY ( eventID ));""")
            mydb2.commit()
        except Exception as e:
            print(item[i].replace(' ', '') + "dailySentiment", e)
        sql = "INSERT INTO " + item[i].replace(' ', '').replace('&','').replace('-','') + "_dailySentiment (datetime, tweetVolume, happy, angry, surprise, sad, fear, sentiment, sentimentScore) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
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
                val = (str(last + " 00:00:00"), 
                     str(count), 
                     str(happy/count), 
                     str(angry/count), 
                     str(surprise/count), 
                     str(sad/count), 
                     str(fear/count), 
                     str(1 if positive/count >= .5 else 0), 
                     str(positive/count) if positive/count >= .5 else str(negative/count))
                writer.execute(sql, val)
                mydb2.commit()
                print(writer.rowcount, "record inserted.")
                print(item[i], last)
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
                positive += x[7]
                negative += 1 - x[7]
            else:
                positive += 1 - x[7]
                negative += x[7]
            count += 1
            last = x[0].split(" ")[0]

def clearAll():
    data = getStockData()
    mydb2 = mysql.connector.connect(
      host="localhost",
      user="admin",
      password="", 
      database="twitter"
    )
    writer = mydb2.cursor()
    for item in data:
        for i in ['Symbol', 'CompanyName', 'Sector']:
            try:
                writer.execute("""drop table """ + item[i].replace(' ', '').replace('&','').replace('-','') + """_dailySentiment;""")
                mydb2.commit()
            except Exception as e:
                print(item, e)
#clearAll()




            
            
            
            
            
            
            
            