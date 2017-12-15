#!/usr/bin/python3
import cgi   # used to handle parameters from html form sent via post method
import cgitb   
cgitb.enable() 
form=cgi.FieldStorage()
start=form.getvalue('ds')  # put the form entry named as 'ds' to variable start
fin=form.getvalue('df')    # put the form entry named as 'df' to variable fin
import mysql.connector     
dbconn= mysql.connector.connect(host='4x.xx.1xx.2xx',port='3306',database='rxxxema',user='root',password='Jxxo')  # connect mysql db
cursor=dbconn.cursor()
query='''select source,period,signup ,donor, avg_donation  
from acqusition where acq_date between '{}' and '{}' '''.format(start,fin)  
cursor.execute(query)  # execute query
report=cursor.fetchall()  # put query result to python variable report
print('Content-Type: text/html') # print headers
print()                             
print ('<table border="1"><tr><th>_source_</th><th>period</th><th>_signup_</th><th>_donor_</th><th>avg_donation</th></tr>')   # print table
print ('<tbody>')
for field in report:
    source = field[0]
    period = field[1]
    signup = field[2]
    donor =  field[3]
    avg_donation = field[4]
    print ('<tr><td>' + str(source) + '</td><td>' + str(period) + '</td><td>' + str(signup) + '</td><td>' + str(donor) + '</td><td>' + str(avg_donation) + '</td></tr>')
print ('</tbody>')
print ('</table>')
cursor.close()
dbconn.close()





