#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 16:32:01 2021

@author: chasebrown
"""

from os import listdir, chdir, rename, mkdir
from os.path import isfile, join
import tarfile
import zipfile
from timeit import default_timer as timer
import shutil
from multiprocessing import Process
from os import path
import datetime


def makeString(integer):
    string = str(integer)
    if len(string) == 1:
        string = "0" + string
    return string

def getDataAudit():
    workingDirectory = "/Volumes/My Data/Time Series Data/Twitter Data/"

    start_date = datetime.date(2006, 1, 1)
    end_date = datetime.date(2025, 12, 31)
    delta = datetime.timedelta(days=1)
    
    found = {}
    missing = {}
    while start_date <= end_date:
        year = makeString(start_date.year)
        month = makeString(start_date.month)
        day = makeString(start_date.day)
        dateString = year + '-' + month + '-' + day
        found.update({dateString: []})
        missing.update({dateString: []})
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
                        missing[dateString].append(hour + ':' + minute)
            else:
                for minute in range(0,60):
                    minute = makeString(minute)
                    missing[dateString].append(hour + ':' + minute)
        start_date += delta
    return found, missing

def getCompressed(mypath, workingDirectory):
    chdir(workingDirectory)
    folders = [f for f in listdir(mypath) if not isfile(join(mypath, f))]
    zipFiles = []
    for folder in folders:
        newPath = mypath + folder + '/'
        files = [f for f in listdir(newPath) if isfile(join(newPath, f))]
        for file in files:
            if '.zip' in file or '.tar' in file:
                try:
                    noEnding = file.split('.')[-2]
                    day = noEnding.split('_')[-1]
                    month = noEnding.split('_')[-2]
                    year = noEnding.split('_')[-3]
                    zipFiles.append({'path': newPath+file, 'filename':file, 'year':year, 'month':month, 'day':day})
                except:
                    try:
                        noEnding = file.split('.')[-2]
                        day = noEnding.split('-')[-1]
                        month = noEnding.split('-')[-2]
                        year = noEnding.split('-')[-3]
                        zipFiles.append({'path': newPath+file, 'filename':file, 'year':year, 'month':month, 'day':day})
                    except:
                        print(file)
                        zipFiles.append({'path': newPath+file, 'filename':file, 'year':'0', 'month':'0', 'day':'0'})
    files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    if len(files) > 0:        
        for file in files:
            if '.zip' in file or '.tar' in file:
                try:
                    noEnding = file.split('.')[-2]
                    day = noEnding.split('_')[-1]
                    month = noEnding.split('_')[-2]
                    year = noEnding.split('_')[-3]
                    zipFiles.append({'path': mypath+file, 'filename':file, 'year':year, 'month':month, 'day':day})
                except:
                    try:
                        noEnding = file.split('.')[-2]
                        day = noEnding.split('-')[-1]
                        month = noEnding.split('-')[-2]
                        year = noEnding.split('-')[-3]
                        zipFiles.append({'path': mypath+file, 'filename':file, 'year':year, 'month':month, 'day':day})
                    except:
                        print(file)
                        zipFiles.append({'path': mypath+file, 'filename':file, 'year':'0', 'month':'0', 'day':'0'})
    return zipFiles

def writeLogs(message, workerNumber):
    workingDirectory = '/Volumes/My Data/Time Series Data/Twitter Data/logs/'
    logs = open(workingDirectory + 'workerNumber' + str(workerNumber) + '.txt', 'a')
    logs.write(message + '\n')
    logs.close()
    

def unZipDays(workingDirectory, zipFiles, workerNumber):
    for file in zipFiles:
        trash = 'temp/'
        writeLogs("Starting file: " + file["filename"], workerNumber)
        start = timer()
        empty = False
        if file['filename'].endswith("zip"):
            writeLogs('In Zip', workerNumber)
            try:
                with zipfile.ZipFile(file['path'],"r") as zip_ref:
                    zip_ref.extractall(workingDirectory + trash + str(workerNumber))
                writeLogs('File Unzipped', workerNumber)
                jsons = []
                currentPath = workingDirectory + trash +  str(workerNumber) + '/'
                directories = [f for f in listdir(currentPath) if not isfile(join(currentPath, f))]
                deletePath = workingDirectory + trash + str(workerNumber) + '/'
                while len(jsons) == 0:
                    directories = [f for f in listdir(currentPath) if not isfile(join(currentPath, f))]
                    writeLogs("In Loop", workerNumber)
                    jsons = [f for f in listdir(currentPath) if isfile(join(currentPath, f))]
                    if not len(directories) == 0:
                        currentPath += directories[0] + '/'
                        chdir(currentPath)
                    elif len(jsons) == 0:
                        empty = True
                        break
                if not empty:
                    writeLogs("Moving Files", workerNumber)
                    rename('/'.join(currentPath.split('/')[:-2]),workingDirectory + file['year'] + "/" + file['month'] + "/" + file['day'])
                writeLogs("Deleting Files", workerNumber)
                shutil.rmtree(deletePath)
            except Exception as e:
                writeLogs("Bad Zip", workerNumber)
                writeLogs(str(e), workerNumber)
        elif file['filename'].endswith("tar"):
            writeLogs("In Tar", workerNumber)
            try:
                mkdir(workingDirectory + trash + str(workerNumber) + '/')
            except:
                pass
            chdir(workingDirectory + trash + str(workerNumber))
            try:
                tar = tarfile.open(file['path'], "r:")
                tar.extractall()
                tar.close()
                writeLogs('File Unzipped', workerNumber)
                jsons = []
                currentPath = workingDirectory + trash + str(workerNumber) + '/'
                while len(jsons) == 0:
                    directories = [f for f in listdir(currentPath) if not isfile(join(currentPath, f))]
                    jsons = [f for f in listdir(currentPath) if isfile(join(currentPath, f))]
                    if not len(directories) == 0:
                        writeLogs("In Loop", workerNumber)
                        currentPath += directories[0] + '/'
                        chdir(currentPath)
                    elif len(jsons) == 0:
                        empty = True
                        break
                if not empty:
                    writeLogs("Moving Files", workerNumber)
                    rename('/'.join(currentPath.split('/')[:-2]),workingDirectory + file['year'] + "/" + file['month'] + "/" + file['day'])
                deletePath = workingDirectory + trash + str(workerNumber) + '/'
                writeLogs("Deleting Files", workerNumber)
                shutil.rmtree(deletePath)
            except Exception as e:
                writeLogs("Bad Tar", workerNumber)
                writeLogs(str(e), workerNumber)
        end = timer()
        writeLogs("That last one took: " + str(end-start), workerNumber)
        
#Runs body in parallel cores
def runBlocks(cores, zipFiles, workingDirectory):
    listOfProcesses = []
    
    for i in range(0, cores):
        start = int(i*(len(zipFiles)/cores))
        end = int((i+1)*(len(zipFiles)/cores))
        process = Process(target=unZipDays, args=(workingDirectory, zipFiles[start:end], i))
        process.start()
        listOfProcesses.append(process)
    
    for process in listOfProcesses:
        process.join()

#Main Method
def main():
    cores = 11
    mypath = "/Volumes/My Data/Time Series Data/Torrent Download/archiveteam-twitter-stream-2020-12/"
    workingDirectory = "/Volumes/My Data/Time Series Data/Twitter Data/"
    print('Getting Audit')
    found, missing = getDataAudit()
    print("Got Audit")
    filteredFiles = []
    print("Getting Data")
    zipFiles = getCompressed(mypath, workingDirectory)
    for i in zipFiles:
        try:
            if (len(missing[i['year'] + '-' + i['month'] + '-' + i['day']])==1440):
                filteredFiles.append(i)
            else:
                print('Not using File: ' + i['filename'])
        except:
            print('Fake File: ' + i['filename'])
    print("Got Data")
    print("Starting Processes")
    runBlocks(cores, filteredFiles, workingDirectory)
    print("Finished")
if __name__ == '__main__':
    main()

            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
