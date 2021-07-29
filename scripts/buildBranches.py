#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 18:41:41 2021

@author: chasebrown
"""
from os import chdir, mkdir


mypath = "/Volumes/My Data/Stocks/"
workingDirectory = "/Volumes/My Data/Time Series Data/Twitter Data/"
chdir(workingDirectory)
days = {'01':31, '02':28, '03':31, '04':30, '05':31, '06':30, '07':31, '08':31, '09':30, '10':31, '11':30, '12':31}
for year in range(2006,2026):
    intYear = year
    year = str(year)
    chdir(workingDirectory)
    mkdir(year)
    for month in range(1,13):
        month = str(month)
        if len(month) == 1:
            month = ("0"+month)
        chdir(workingDirectory + year)
        mkdir(month)
        if intYear%4 == 0 and month=='02':
            for day in range(1, days[month]+2):
                day = str(day)
                if len(day) == 1:
                    day = ("0"+day)
                chdir(workingDirectory + year + "/" + month)
                mkdir(day)
        else:
            for day in range(1, days[month]+1):
                day = str(day)
                if len(day) == 1:
                    day = ("0"+day)
                chdir(workingDirectory + year + "/" + month)
                mkdir(day)
            
