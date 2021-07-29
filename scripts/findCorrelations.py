#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 17:30:16 2021

@author: chasebrown
"""

# generate related variables
from scipy.stats import pearsonr
from scipy.stats import spearmanr
import mysql.connector
import csv
import pandas as pd


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
iterator = mydb2.cursor()
       
data = {}
tables = []
reader.execute("SHOW TABLES;")
for table in reader:
    tables.append(table)
    if (not 'Before' in table[0]) and (not 'After' in table[0]):
        tables.append(table)
    

sums = {}
for tag in data.keys():
    for key1 in data[tag].keys()[1:8]:
        for key2 in data[tag].keys()[8:]:
            if not key1 == key2:
                try:
                    corr, _ = pearsonr(data[tag][key1].dropna(), data[tag][key2].dropna())
                    corr2, _ = spearmanr(data[tag][key1].dropna(), data[tag][key2].dropna())
                    if not str(corr2) == 'nan' and not str(corr) == 'nan':
                        if not key1 + ':' + key2 in sums.keys():
                            sums.update({key1 + ':' + key2:{'Pearson':corr, 'Spearman':corr2, 'Count':1}})
                        else:
                            sums[key1 + ':' + key2]['Pearson'] += corr
                            sums[key1 + ':' + key2]['Spearman'] += corr2
                            sums[key1 + ':' + key2]['Count'] += 1
                except Exception as e:
                    pass
                
averages = {}          
for i in sums.keys():
    averages.update({i: {'Pearson':sums[i]['Pearson']/sums[i]['Count'], 'Spearman':sums[i]['Spearman']/sums[i]['Count']}})
    
for i in averages.keys():
    print(i,',',averages[i]['Pearson'], ',', averages[i]['Spearman'])


individuals = {}
for tag in data.keys():
    for key1 in data[tag].keys()[1:8]:
        for key2 in data[tag].keys()[8:]:
            if not key1 == key2:
                try:
                    corr, _ = pearsonr(data[tag][key1].dropna(), data[tag][key2].dropna())
                    corr2, _ = spearmanr(data[tag][key1].dropna(), data[tag][key2].dropna())
                    individuals.update({tag + ':' + key1 + ':' + key2 :{'Pearson':corr, 'Spearman':corr2, 'datasize':len(data[tag][key1].dropna())}})
                except Exception as e:
                    pass

file = open('/Volumes/My Data/Time Series Data/Twitter Data/stockCorrelations.csv', 'w')
for i in individuals.keys():
    strength = 'None'
    if abs(individuals[i]['Pearson']) > .7 or abs(individuals[i]['Spearman']) > .7:
        strength = 'Strong'
    elif abs(individuals[i]['Pearson']) > .4 or abs(individuals[i]['Spearman']) > .4:
        strength = 'Medium'
    elif abs(individuals[i]['Pearson']) > 0 or abs(individuals[i]['Spearman']) > 0:
        strength = 'Weak'
    file.write(','.join([str(i),str(individuals[i]['Pearson']),str(individuals[i]['Spearman']), strength, str(individuals[i]['datasize']) + '\n']))
file.close()
