#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 18:13:45 2021

@author: chasebrown
"""

from os import path
import datetime
import mysql.connector as connector

mydb = connector.connect(
  host="localhost",
  user="root",
  password="password", 
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
    
    start_date = datetime.date(2018, 1, 1)
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
workingDirectory = "/Volumes/My Data/Time Series Data/Twitter Data/"
sql = "INSERT INTO minuteFiles (datetime, path, beenAnalyzed) VALUES (%s, %s, %s)"
for key in found.keys():
    YYYY, MM, DD = key.split('-')
    for minute in found[key]:
        HH, mm = minute.split(':')
        val = (key + ' ' + minute, workingDirectory + YYYY + '/' + MM + '/' + DD + '/' + HH + '/' + mm + '.json.bz2', 0)
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "record inserted.")
    
