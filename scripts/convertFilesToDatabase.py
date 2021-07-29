#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 13:47:14 2021

@author: chasebrown
"""

#Import the modules
from multiprocessing import Process
import bz2
import json
import os
from langdetect import detect
import mysql.connector



#Change date ints into proper string (ie 9 returns '09')
def makeString(integer):
    string = str(integer)
    if len(string) == 1:
        string = "0" + string
    return string


#Runs Sentiment And Emotion Analysis and calls storeData function
def storeTweets(tweets, dateTime):
    mydb = mysql.connector.connect(
      host="localhost",
      user="admin",
      password="", 
      database="twitter"
    )
    mycursor = mydb.cursor()
    try:
        mycursor.execute("""create table """ + dateTime.split(' ')[0].replace(' ', '_').replace('-','_') + """_tweets(    
                          tweetID VARCHAR(255) NOT NULL,    
                          datetime TEXT NOT NULL, 
                          text TEXT,
                          hashtags TEXT,
                          symbols TEXT, 
                          favorite_count INT, 
                          quote_count INT, 
                          reply_count INT, 
                          lang TEXT, 
                          geo TEXT, 
                          PRIMARY KEY ( tweetID ));""")
        mydb.commit()
    except:
        pass
    for tweet in tweets:
        try:
            sql = "INSERT IGNORE INTO " + dateTime.split(' ')[0].replace(' ', '_').replace('-','_') + "_tweets (tweetID, datetime, text, hashtags, symbols, favorite_count, quote_count, reply_count, lang, geo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (str(tweet['id']), 
                         str(dateTime), 
                         str(tweet['text']), 
                         str(tweet['entities']['hashtags']), 
                         str(tweet['entities']['symbols']), 
                         str(tweet['favorite_count']), 
                         str(tweet['quote_count']), 
                         str(tweet['reply_count']), 
                         str(tweet['lang']), 
                         str(tweet['geo']))
            mycursor.execute(sql, val)
        except Exception as e: 
            pass
    mydb.commit()
    print(dateTime)
    
    mycursor.close()
    mydb.close()
              
#Returns times found in range from tweet dataset
def getFileData(mycursor):
    found = []
    mycursor.execute("SELECT datetime, path FROM minuteFiles;")
    for x in mycursor:
        found.append({'datetime':x[0],'file':x[1]})
    return found

#Returns json data from minute file
def readMinuteFiles(filename):
    tweetData = []
    try:
        filepath = filename
        newfilepath = filename.replace(".json.bz2", ".json")
        with open(newfilepath, 'wb') as new_file, bz2.BZ2File(filepath, 'rb') as file:
            for data in iter(lambda : file.read(100 * 1024), b''):
                new_file.write(data)
    
        tweetFile = open(newfilepath, 'r')
        
        text = ''
        for line in tweetFile:
            text += line
        items = text.split('\n')
        
        for item in items:
            try:
                tweetData.append(json.loads(item))
            except Exception as e:
                pass
        tweetFile.close()
        os.remove(newfilepath)
    except Exception as e:
         print((filename + ' failed.\n' + str(e)))
    return tweetData

#Process to be run in parallel
def workerTask(zipFiles):
    for file in zipFiles:
        tweets = readMinuteFiles(file['file'])
        storeTweets(tweets, file['datetime'])
            
#Runs body in i parallel fragements
def runBlocks(cores, zipFiles):
    days = {}
    for item in zipFiles:
        if not item['datetime'].split(' ')[0] in days:
            days.update({item['datetime'].split(' ')[0]:[item]})
        else:
            days[item['datetime'].split(' ')[0]].append(item)
        listOfProcesses = []
        for i in range(0, cores):
            start = int(i*(len(zipFiles)/cores))
            end = int((i+1)*(len(zipFiles)/cores))
            process = Process(target=workerTask, args=([zipFiles[start:end]]))
            process.start()
            listOfProcesses.append(process)
        
        for process in listOfProcesses:
            process.join()

def clearAll():
    mydb = mysql.connector.connect(
      host="localhost",
      user="admin",
      password="", 
      database="twitter"
    )
    iterator = mydb.cursor()
    
    mydb2 = mysql.connector.connect(
      host="localhost",
      user="admin",
      password="", 
      database="twitter"
    )
    writer = mydb2.cursor()
    iterator.execute("SHOW TABLES;")
    for i in iterator:
        if '_tweets' in i:
            try:
                writer.execute("drop table " + i + ";")
                mydb2.commit()
            except Exception as e:
                print(i, e)    
    
#clearAll()


#Main Method
def main():
    print('Connecting To Database')
    mydb = mysql.connector.connect(
      host="localhost",
      user="admin",
      password="", 
      database="twitter"
    )
    mycursor = mydb.cursor()
    print('Connected To Database')
        
    cores = 8
    print('Getting Audit')
    zipFiles = getFileData(mycursor)
    print("Got Audit")
    
    mycursor.close()
    mydb.close()
    
    runBlocks(cores, zipFiles)
    
    
if __name__ == '__main__':
    main()

    
