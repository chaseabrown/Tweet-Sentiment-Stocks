#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 13:47:14 2021

@author: chasebrown
"""

#Import the modules
import text2emotion as te
import flair
from multiprocessing import Process
import bz2
import json
import os
from langdetect import detect
import mysql.connector as connector
from os import listdir
from os.path import isfile, join
import csv



sentiment_model = flair.models.TextClassifier.load('en-sentiment')

#Change date ints into proper string (ie 9 returns '09')
def makeString(integer):
    string = str(integer)
    if len(string) == 1:
        string = "0" + string
    return string

#Returns positive vs negative score
def getSentiment(tweet):
    sentence = flair.data.Sentence(tweet)
    sentiment_model.predict(sentence)
    score = (sentence.labels[0].score)  # numerical score 0-1
    sentiment = (sentence.labels[0].value)  # 'POSITIVE' or 'NEGATIVE'
    return {'score': score, 'sentiment': sentiment}

#Runs Sentiment And Emotion Analysis and calls storeData function
def runAnalysis(workerNumber, tweets, dateTime):
    mydb = connector.connect(
      host="localhost",
      user="root",
      password="password", 
      database="twitter"
    )
    mycursor = mydb.cursor()
    mydb2 = connector.connect(
      host="localhost",
      user="root",
      password="password", 
      database="twitter"
    )
    mycursor2 = mydb2.cursor()
    for tweet in tweets:
        try:
            if detect(tweet['tweet']['text']) == 'en':
                #Time to run function = ~ 0.120420975 seconds per tweet
                tweet.update({"Emotions":te.get_emotion(tweet['tweet']['text'])})
                #Time to run function = ~ 0.091710396 seconds per tweet
                tweet.update({"Sentiment":getSentiment(tweet['tweet']['text'])})
                #Time to run function = ~ 0.000201158 seconds per tweet
                sql = "INSERT IGNORE INTO tweetSentiment (datetime, tweetID, tickers, happy, angry, surprise, sad, fear, sentiment, sentimentScore) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                val = (dateTime, str(tweet['tweet']['id_str']), 
                             str(tweet['symbols']), 
                             str(tweet['Emotions']['Happy']), 
                             str(tweet['Emotions']['Angry']), 
                             str(tweet['Emotions']['Surprise']), 
                             str(tweet['Emotions']['Sad']), 
                             str(tweet['Emotions']['Fear']), 
                             str(tweet['Sentiment']['sentiment']),
                             str(tweet['Sentiment']['score']))
                mycursor.execute(sql, val)
        except Exception as e:
            print(e)
    mydb.commit()
    mycursor2.execute("UPDATE minuteFiles SET beenAnalyzed = 1 WHERE datetime='" + dateTime + "';")
    mydb2.commit()
    mycursor2.close()
    mydb2.close()
    mycursor.close()
    mydb.close()
              
#Returns times found in range from tweet dataset
def getFileData(mycursor):
    found = []
    mycursor.execute("SELECT datetime, path FROM minuteFiles WHERE beenAnalyzed=0;")
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
                print("Json Failed to Unpack: " + str(e))
        tweetFile.close()
        os.remove(newfilepath)
    except Exception as e:
         print((filename + ' failed.\n' + str(e)))
    return tweetData

#Returns json data from only topical tweets
def getTopicalTweets(filename, topics):
    tweets = readMinuteFiles(filename)
    topicalTweets = []
    for tweet in tweets:
        temp = {'tweet': tweet, 'symbols': []}
        for topic in topics:
            try:
                if "$" + topic['Symbol'] + " " in tweet['text'] or "#" + topic['Symbol'] + " " in tweet['text']:
                    temp['symbols'].append(topic['Symbol'])
            except:
                pass
        try:
            if not (len(temp['symbols']) == 0):
                topicalTweets.append(temp)
        except:
            pass
    return topicalTweets

#Read in and return stock data
def getStockData():
    stockData = []    
    
    with open('/Volumes/My Data/Time Series Data/Twitter Data/stockInformation.json') as jsonFile:
        stockData = json.load(jsonFile)
    return stockData

#Process to be run in parallel
def workerTask(zipFiles, topics, workerNumber):
    for file in zipFiles:
        tweets = getTopicalTweets(file['file'], topics[0])
        runAnalysis(workerNumber, tweets, file['datetime'])
            
#Runs body in i parallel fragements
def runBlocks(cores, zipFiles, topics):
    listOfProcesses = []
    for i in range(0, cores):
        start = int(i*(len(zipFiles)/cores))
        end = int((i+1)*(len(zipFiles)/cores))
        process = Process(target=workerTask, args=(zipFiles[start:end], topics, str(i)))
        process.start()
        listOfProcesses.append(process)
    
    for process in listOfProcesses:
        process.join()
            
        
        
#Runs Sentiment And Emotion Analysis and calls storeData function
def runAnalysisCurrent(tweets, workerNumber):
    mydb = connector.connect(
      host="localhost",
      user="root",
      password="password", 
      database="twitter"
    )
    for tweet in tweets:
        try:
            mycursor = mydb.cursor(buffered=True)
            if detect(tweet['Tweet']) == 'en':
                #Time to run function = ~ 0.120420975 seconds per tweet
                tweet.update({"Emotions":te.get_emotion(tweet['Tweet'])})
                #Time to run function = ~ 0.091710396 seconds per tweet
                tweet.update({"Sentiment":getSentiment(tweet['Tweet'])})
                #Time to run function = ~ 0.000201158 seconds per tweet
                sql = "INSERT INTO tweetSentimentCurrent (datetime, tickers, happy, angry, surprise, sad, fear, sentiment, sentimentScore) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                val = (tweet['Date'] + " " + tweet['Time'], 
                             str(tweet['Stock_Ticker']), 
                             str(tweet['Emotions']['Happy']), 
                             str(tweet['Emotions']['Angry']), 
                             str(tweet['Emotions']['Surprise']), 
                             str(tweet['Emotions']['Sad']), 
                             str(tweet['Emotions']['Fear']), 
                             str(tweet['Sentiment']['sentiment']),
                             str(tweet['Sentiment']['score']))
                mycursor.execute(sql, val)
                mydb.commit()
                mycursor.close()
        except Exception as e:
            print(e)
    mydb.close()    


def analyzeCurrentData(cores, tweets):
    listOfProcesses = []
    for i in range(0, cores):
        start = int(i*(len(tweets)/cores))
        end = int((i+1)*(len(tweets)/cores))
        process = Process(target=runAnalysisCurrent, args=(tweets[start:end], i))
        process.start()
        listOfProcesses.append(process)
    
    for process in listOfProcesses:
        process.join()



#Main Method
def main():
    mypath = "/Volumes/My Data/Time Series Data/Twitter Data/currentTweets/"
    files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    goodFiles = [f for f in files if not f[0] == '.']
    
    tweets = []
    for file in goodFiles:
        with open(mypath + file, newline='', encoding='utf-8', errors='replace') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            try:
                keys = {}
                for row in reader:
                    if row[0] == '':
                        row[0] = 'ID'
                        keys = row
                    else:
                        temp = dict(zip(keys, row))
                        tweets.append(temp)
            except csv.Error as e:
                print('file %s, line %d: %s' % (csvfile, reader.line_num, e))
            
    cores = 8
    analyzeCurrentData(cores, tweets)
    
    """print('Connecting To Database')
    mydb = connector.connect(
      host="localhost",
      user="root",
      password="password", 
      database="twitter"
    )
    mycursor = mydb.cursor()
    print('Connected To Database')
        
    cores = 8
    print('Getting Audit')
    zipFiles = getFileData(mycursor)
    print("Got Audit")
    
    print("Getting Stocks")
    stockData = getStockData()
    print("Got Stocks")
    
    
    mycursor.close()
    mydb.close()
    
    runBlocks(cores, zipFiles, stockData)"""
    
    
if __name__ == '__main__':
    main()

    
