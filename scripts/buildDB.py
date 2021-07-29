#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 16:17:17 2021

@author: chasebrown
"""
import os
import csv
import mysql.connector

mydb = mysql.connector.connect(
      host="localhost",
      user="admin",
      password="", 
      database="twitter"
    )
mycursor = mydb.cursor()

mydb2 = mysql.connector.connect(
      host="localhost",
      user="admin",
      password="", 
      database="twitter"
    )
mycursor2 = mydb2.cursor()


for i in ['names', 'tickers', 'sectors']:
    files = os.listdir("/Volumes/My Data/Time Series Data/Twitter Data/sentimentFiles/" + i + "/")
    for file in files:
        if not file[0] == '.':
            with open('/Volumes/My Data/Time Series Data/Twitter Data/sentimentFiles/' + i + '/' + file, 'r', newline='', encoding='ISO-8859-1') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    if row["Datetime"].count('-')==2 and row["Datetime"].count(':')==1:
                        sql = "INSERT IGNORE INTO tweetSentiment (datetime, tweetID, tickers, names, sectors, happy, angry, surprise, sad, fear, sentiment, sentimentScore) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                        val = (str(row["Datetime"]),
                               str(row['id_str']), 
                               str(row['Symbols']), 
                               str(row['Company Names']), 
                               str(row['Sectors']), 
                               str(row["Happy"]), 
                               str(row["Angry"]), 
                               str(row["Surprise"]), 
                               str(row["Sad"]), 
                               str(row["Fear"]), 
                               str(row["Sentiment"]),
                               str(row["Sentiment Score"]))
                        mycursor.execute(sql, val)
                        mydb.commit()

