#!/usr/bin/python3
# -*- coding: utf-8 -*-

from apscheduler.schedulers.blocking import BlockingScheduler  # python scheduler
import logging
import mysql.connector          # driver to connect mysql  
import psycopg2                 # driver to connect postgresql
import sys
import codecs

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())     # helps to avoid character and unicode errors

logging.basicConfig(level=logging.DEBUG)                        # activate logging 
sched = BlockingScheduler()

def leadtransfer():
	# Find the last inserted id and put it to a python variable
	dbconn= mysql.connector.connect(host='4x.xx.xxx.xx3',database='xxxx',port='3306', user='root',password='Jxxxo')
	cursor=dbconn.cursor()
	cursor.execute(""" select max(Source_ID) from lxxxs """)    
	maxid=cursor.fetchall()
	maxid=int(maxid[0][0])
	dbconn.close()
	
	# Connect to postgresql db in a remote server fetch the data to a python variable
	conn=psycopg2.connect("dbname='xxxa' user='xxxxx' host='1xx.xx.xxx.x8' password='0xxxxx7'")
	conn.autocommit= True
	cur=conn.cursor()
	query="""  SELECT signups.id,signers.email,signers.first_name,signers.last_name,signers.phone_number,signers.date_of_birth,
    case when signups.extra LIKE '%leadsbridge%' then concat('lc_',campaigns.name) else campaigns.name end ,signups.updated_at,signers.city,
    signers.phone_ok,signers.email_ok,signers.sms_ok,SPLIT_PART(SPLIT_PART(signups.source,'utm_source',2),'"',3) as utm_campaign,signups.source,
    SPLIT_PART(SPLIT_PART(signups.source,'utm_campaign',2),'"',3) as utm_campaign,case when left(signups.source,5) like '%b%' then 'Y' else ' ' end as cpn,now() 
    from signups join signers on signups.signer_id=signers.id join campaigns  on signups.campaign_id=campaigns.id 
    where signups.id >'[0]' """.format(maxid)
	cursor.execute(query)
    report=cur.fetchall()
    conn.close()
	
	# insert the data to mysql table in another remote server
	dbconn= mysql.connector.connect(host='4x.xx.xxx.xx3',database='xxxx',port='3306', user='root',password='Jxxxo')
	cursor=dbconn.cursor()
	for row in report:
		query='''insert into leads (Source_ID,email,first_name,last_name,phone_number,date_of_birth,campaign,signing_time,city,phone_ok,email_ok,sms_ok,utm_source,
	    source,utm_campaign,cpn,created_time) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
        cursor.execute(query,[row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16]])
        dbconn.commit()
	dbconn.close()	

sched.add_job(leadtransfer,'cron',day_of_week='*',hour=6,minute=45, misfire_grace_time=600,coalesce=True)    # schedule the task
sched.start()
	

	
