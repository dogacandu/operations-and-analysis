#!/usr/bin/python3
import urllib.request    # for secure ftp connection one has to import pysftp 
import xlrd              # used to convert xlsx to csv 
import csv               # for csv operations 
import mysql.connector   



yesterday_file='20170709_TRANID_STATUS.xlsx'
yesterday_csvfile='20170709_TRANID_STATUS.csv'
urllib.request.urlretrieve('ftp://username:passwd@ftphost/ftpdirectory/'+yesterday_file,'C:/Users/.../reports/'+yesterday_file)   # get the excel file via ftp and save it to a specified location in your server
wb = xlrd.open_workbook('C:/Users/../reports/'+yesterday_file)  # open the excel file
sh = wb.sheet_by_name('Sheet2')  # name the sheet u want to use
my_csv_file = open('C:/Users/.../reports/'+yesterday_csvfile, 'w',encoding='utf-8',newline='')  # open the csv file
wr = csv.writer(my_csv_file, quoting=csv.QUOTE_ALL)  # write the excel data to csv file
for rownum in range(sh.nrows):
        wr.writerow(sh.row_values(rownum))	
my_csv_file.close()  
path_to_csvfile='C:/Users/../reports/'+yesterday_csvfile
dbconn= mysql.connector.connect(host='localhost',database='rxxxa',user='root',password='Jxxxo')  # connect mysql
cursor=dbconn.cursor()
query=('''LOAD DATA INFILE %s INTO TABLE rxxxa.callcenter_data FIELDS TERMINATED BY ','    
ENCLOSED BY '"' LINES TERMINATED BY '\r\n' IGNORE 1 ROWS ''')       
cursor.execute(query,[path_to_csvfile])                    # load csv file into a mysql table
dbconn.commit()                                            # commit 
cursor.close() 
dbconn.close()
