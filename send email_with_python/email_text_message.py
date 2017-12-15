#!/usr/bin/python3

import smtplib
import os


sender='sender@mail.com'
sentto='seontto@mail.com'
subject='hello'
text_message=""" blah blah ... seeyou bye """


message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (sender, ", ".join(sentto), subject, text_message)
s=smtplib.SMTP('smtp.gmail.com',587)
s.ehlo()
s.starttls() 
s.login(sender,'sender_passwrd')	
s.sendmail(sender,sentto ,message)	
s.close()	

cursor.close()
dbconn.close()	

	

	
