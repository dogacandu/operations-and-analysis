#.py file at /var/www/bridge

#!/usr/bin/python3
from flask import Flask
app = Flask(__name__)
@app.route('/fb', methods =['POST'])
def deliver():
	from flask import request,Response
	raw=request.get_json()
	
	if 'email' in raw:
		email=raw['email']
	else:
		email=''
	if 'phone_number' in raw:
		phone_number=raw['phone_number']
	else:
		phone_number=''
	if 'full_name' in raw:
		full_name=raw['full_name']
	else:
		full_name=''
	if 'email_ok' in raw:
		email_ok=raw['email_ok']
	else:
		email_ok=''
	if 'gp_campaign' in raw:
		gp_campaign=raw['gp_campaign']
	else:
		gp_campaign=''
	if 'campaign_id' in raw:
		campaign_id=raw['campaign_id']
	else:
		campaign_id=''
	if 'adset_id' in raw:
		adset_id=raw['adset_id']
	else:
		adset_id=''
	if 'ad_id' in raw:
		ad_id=raw['ad_id']
	else:
		ad_id=''
	if 'dob' in raw:
		dob=raw['dob']
	else:
		dob=''
	if 'city' in raw:
		city=raw['city']
	else:
		city=''


	import mysql.connector
	from datetime import datetime 
	dbconn= mysql.connector.connect(host='hostIP',port='3306',database='dbname',user='root',password='passwrd')
	cursor=dbconn.cursor()
	query="""insert into bridge (email,phone_number,full_name,email_ok,gp_campaign,campaign_id,adset_id,ad_id,dob,city,signing_time) 
values ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')""".format(email,phone_number,full_name,email_ok,gp_campaign,campaign_id,adset_id,ad_id,dob,city,datetime.now())
	cursor.execute(query)
	dbconn.commit()
	dbconn.close()
	return Response("{}",status=200,mimetype='application/json')


if __name__ == '__main__':
	app.run()







#addition to configuration file at /etc/apache2/sites-enabled
	
WSGIDaemonProcess bridge user=user group=user threads=5 home=/var/www/bridge/
WSGIScriptAlias /bridge /var/www/bridge/bridge.wsgi
	
	
<Directory /var/www/bridge>
 WSGIProcessGroup bridge
 WSGIApplicationGroup %{GLOBAL}
 Require all granted
</Directory>




#.wsgi file at /var/www/bridge

#!/usr/bin/python3
import sys
sys.path.insert(0,'/var/www/bridge')
from bridge import app as application


