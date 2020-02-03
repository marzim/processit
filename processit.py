from pathlib import Path
from datetime import datetime
import re
import csv
import sys
import os
import argparse
import pandas as pd
from pandas import ExcelWriter

linesInsertDelta = []
linesFinishInsert = []
finalLines = []
xfiles = []

def readFile(filename):
    if filename == '.':
        filename == 'SelfscanEnginePlugin.log'
    print(datetime.now().strftime('%H:%M:%S') + " reading " + filename + "...")
    with open(filename,'r') as reader:
        for line in reader.readlines():
            if line != '':
                x = re.split("\s", line)                
                if x and "InsertDelta" in x[5]:
                    linesInsertDelta.append(line)                    
                elif 'OnlineProcessor' in x[8] and 'request' in x[10]:
                    linesFinishInsert.append(line)
                elif x and "Finished" in x[7] and "InsertDelta" in x[8]:
                    linesFinishInsert.append(line)                                     
    print(datetime.now().strftime('%H:%M:%S') + " done reading " + filename + "...")       
    
def getfile(self, filename):
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    for f in files:
        if filename.lower() == f.lower():
            return f    

def mergeLines():
    print(datetime.now().strftime('%H:%M:%S') + " merging data...")
    for s in linesInsertDelta:
        x = re.split("\s", s)
        xlist = re.split("\(", x[5])
        transId = ''
        xval = re.split("\,", xlist[1])[0]
        transId = xval[1:] if xval.startswith('-') else xval        
        threadId = x[3]     
        itemCode = re.split("\)", x[8])[0]           
        getFinishLine(transId, threadId, itemCode)
    print(datetime.now().strftime('%H:%M:%S') + " done merging data...")

def getFinishLine(transId, threadId, itemCode):
    getperoundtrip = 1
    for s in linesFinishInsert:
        x = re.split("\s", s)                
        if "Finished" in x[7] and "InsertDelta" in x[8]:
            xlist = re.split("\(", x[8])
            xtransid = ''
            xval = re.split("\)", xlist[1])[0]
            xtransid = xval[1:] if xval.startswith('-') else xval
            
            if transId == xtransid and threadId == x[3]:
                line = x[0] + ' ' + x[1] + ',Central Server Roundtrip,' + threadId + ',' + transId + ',' + itemCode + ',' + x[10]              
                finalLines.append(line)   
                getperoundtrip = 1; 
                break
        elif 'OnlineProcessor' in x[8] and threadId == x[3] and getperoundtrip == 1:
            line = x[0] + ' ' + x[1] + ',Price Engine Roundtrip,' + threadId + ', , ,' + x[12] 
            finalLines.append(line)    
            getperoundtrip = 0
        

def createCSV():
    xdate = datetime.now().strftime('%m%d%Y-%H%M%S')
    print(datetime.now().strftime('%H:%M:%S') + " creating csv file...")
    xfile = xdate+"-result.csv"
    with open(xfile, 'w', newline='') as myfile:
        wr = csv.writer(myfile, delimiter=',')
        wr.writerow(['Time','Label','Thread Id','Transaction Id','Item code','Duration (ms)'])
        wr.writerows([x.split(',') for x in finalLines])
        print(datetime.now().strftime('%H:%M:%S') + " done creating csv file " + xfile)

def dir_path(path):
    if os.path.isdir(path) or os.path.isfile(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"readable_dir:{path} is not a valid path")

def parse_mode(mode):
    if mode == 'selfscan' or mode == 'pf':
        return mode
    else:
        raise argparse.ArgumentTypeError(f"parse mode:{mode} is not recognized")
        
def parseargs():
    parser = argparse.ArgumentParser(description='Process command line arguments.')
    parser.add_argument('-mode', type=parse_mode)
    parser.add_argument('-path', type=dir_path)

    args = parser.parse_args()
    if args.mode != None and args.path != None:
        print(args.mode + ' ' + args.path)
    
    if args.mode == None:
        print('Need to provide mode[-mode selfscan/pf] to process')
        sys.exit(0)

    if args.path == None:
        print('Path is empty therefore it process file within the current directory...')
        args.path = '.'
    
    if args.mode == 'selfscan':
        readFile(args.path)
        mergeLines()    
        createCSV()   
    elif args.mode == 'pf':
        processperfdata(getfiles(args.path))
        

def getfiles(path):
    files = []
    for file in os.listdir(path):
        current = os.path.join(path, file)
        if os.path.isfile(current):
            base = os.path.basename(current)
            filename, ext = os.path.splitext(base)
            if ext == '.csv':
                files.append(current)
    
    return files

def processperfdata(files):
    xdate = datetime.now().strftime('%m%d%Y-%H%M%S')
    xfile = xdate +'-TestReport.xlsx'
    print(datetime.now().strftime('%H:%M:%S') + " creating excel file...")
    writer = ExcelWriter(xfile)
    for file in files:
        base = os.path.basename(file)
        filename, ext = os.path.splitext(base)
        tempresult = pd.read_csv(file, delimiter=',')
        result = tempresult.iloc[:, 0:40]
        result.to_excel(writer, filename, encoding='utf-8', index=False)                
    writer.save()        
    print(datetime.now().strftime('%H:%M:%S') + " done creating excel file " + xfile)
        
        
if __name__ == "__main__":
    parseargs()
    #xfiles = sys.argv[1:]
    #for filename in xfiles:        
    #readFile('')
    #mergeLines()    
    #createCSV()    
            
        
        
        




            
