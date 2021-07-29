#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 12 22:24:06 2021

@author: chasebrown
"""


import mysql.connector as connector
import json

mydb = connector.connect(
      host="localhost",
      user="root",
      password="password", 
      database="twitter"
    )
reader = mydb.cursor(buffered=True)

mydb2 = connector.connect(
      host="localhost",
      user="root",
      password="password", 
      database="twitter"
    )
iterator = mydb2.cursor(buffered=True)

reader.execute("SHOW TABLES;")
for table in reader:
    if '_hourlySentiment' in table[0]:
        try:
            file = open('/Volumes/My Data/Time Series Data/Twitter Data/sentimentFiles/share/withStockDataCurrent/'+ table[0] + ".csv", 'w', newline='', encoding='ISO-8859-1')
            file.write(','.join(["Datetime",
                                    "Open",
                                    "High",
                                    "Low",
                                    "Close",
                                    "Percent Change",
                                    "Percent Change ABS",
                                    "Stock Volume",
                                    "Tweet Volume",
                                    "Happy", 
                                    "Angry", 
                                    "Surprise", 
                                    "Sad", 
                                    "Fear", 
                                    "Sentiment Score"]) + "\n")
            sql = "SELECT * FROM " + table[0] + ";"
            iterator.execute(sql)
            for line in iterator:
                file.write(','.join([str(line[0]),
                                    str(line[1]),
                                    str(line[2]),
                                    str(line[3]),
                                    str(line[4]),
                                    str(line[5]),
                                    str(line[6]),
                                    str(line[7]),
                                    str(line[8]),
                                    str(line[9]),
                                    str(line[10]),
                                    str(line[11]),
                                    str(line[12]),
                                    str(line[13]),
                                    str(line[14])]) + "\n")
            file.close()
        except Exception as e:
            print(table, e)
