#!/usr/bin/python3

from apscheduler.schedulers.blocking import BlockingScheduler   # python_scheduler
from datetime import date
import logging


logging.basicConfig(level=logging.DEBUG)
sched = BlockingScheduler()


def react_enrichment_job():
    import mysql.connector
    dbconn= mysql.connector.connect(host='host_IP',database='cxxi',user='root',password='Jxxxo')  #connect mysql db and get data
    cursor=dbconn.cursor()
    query=cursor.execute('''select id, tel,email from Persontable ''')
    personlist=cursor.fetchall()
    
    
    # create attachment file
    import os
    import csv
    from datetime import datetime

    file_path='Path/Reports/'+str(datetime.now().date())+' list.csv'    
    fp=open(file_path, 'w',encoding='utf-8',newline='')
    attach_file=csv.writer(fp)
    attach_file.writerow(["id","tel","email"])
    attach_file.writerows(personlist)
    fp.close()
    dbconn.close()
 
    
    # attach the file and send
    import smtplib
    
    from email import encoders
    from email.mime.base import MIMEBase
    from email.mime.multipart import MIMEMultipart
    
    msg=MIMEMultipart()
    msg['Subject']='list'+str(datetime.now().date())
    msg['To']='bxxan@xxxace.org'
    msg['From']='ddxxxi@gxxxe.org'
    fp=open(file_path,'rb')
    attachment=MIMEBase('application',"octet-stream")
    attachment.set_payload(fp.read())
    encoders.encode_base64(attachment)
    attachment.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file_path)
    msg.attach(attachment)
    s=smtplib.SMTP('smtp.gmail.com',587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login('ddxxxi@gxxxe.org','psswrd')
    composed=msg.as_string()
    s.sendmail('ddxxxi@gxxxe.org','bxxan@xxxace.org',composed)
    s.close()


sched.add_job(react_enrichment_job,'cron',day_of_week='mon',hour=12,minute=22)  # schedule task for every monday at 12:22
sched.start()

	

