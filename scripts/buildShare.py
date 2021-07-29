#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 18:24:32 2021

@author: chasebrown
"""
import os
import csv


for i in ['names', 'tickers', 'sectors']:
    files = os.listdir("/Volumes/My Data/Time Series Data/Twitter Data/sentimentFiles/" + i + "/")
    for file in files:
        if not file[0] == '.':
            final = open('/Volumes/My Data/Time Series Data/Twitter Data/sentimentFiles/share/' + i + '/' + file.replace("'", ''), 'w', newline='', encoding='ISO-8859-1')
            final.write(','.join(["Datetime",
                             "id_str",
                             "Symbols",
                             "Company Names",
                             "Sectors",
                             "Happy", 
                             "Angry", 
                             "Surprise", 
                             "Sad", 
                             "Fear", 
                             "Sentiment",
                             "Sentiment Score"]) + "\n")
            with open('/Volumes/My Data/Time Series Data/Twitter Data/sentimentFiles/' + i + '/' + file, 'r', newline='', encoding='ISO-8859-1') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    if row["Datetime"].count('-')==2 and row["Datetime"].count(':')==1:
                        final.write(','.join(['"' + str(row["Datetime"])+ '"', 
                                 '"' + str(row["id_str"])+ '"', 
                                 '"' + str(row["Symbols"])+ '"', 
                                 '"' + str(row["Company Names"])+ '"', 
                                 '"' + str(row["Sectors"])+ '"', 
                                 str(row["Happy"]), 
                                 str(row["Angry"]), 
                                 str(row["Surprise"]), 
                                 str(row["Sad"]), 
                                 str(row["Fear"]), 
                                 str(row["Sentiment"]),
                                 str(row["Sentiment Score"])]) + "\n")
            final.close()