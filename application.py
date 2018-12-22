#!venv/bin/python
import os
from flask import Flask, request
from flask_mysqldb import MySQL

# created following https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-flask.html
#

# print a nice greeting.
def say_hello(username = "World"):
    return '<p>Hello %s!</p>\n' % username

# some bits of text for the page.
header_text = '''
    <html>\n<head> <title>EB Flask Test</title> </head>\n<body>'''
instructions = '''
    <p><em>Hint</em>: This is a RESTful web service! Append a username
    to the URL (for example: <code>/Thelonious</code>) to say hello to
    someone specific.</p>\n'''
home_link = '<p><a href="/">Back</a></p>\n'
footer_text = '</body>\n</html>'

# EB looks for an 'application' callable by default.
application = Flask(__name__)

# configure database
# see https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/using-features.managing.db.html
# and https://flask-mysqldb.readthedocs.io/en/latest/#flask_mysqldb.MySQL
# to connect, make sure to add My IP to the security group TCP rules for the security group for the db
#    in elastic beanstalk manager https://us-east-2.console.aws.amazon.com/elasticbeanstalk/home?region=us-east-2#/applications
#    (make sure correct region)
#    click flask-env environment -> Configuration -> Database -> click on the link
#     then click on db, look for Security group tab -> click on security group & add new rule
#
#DATABASE_URL = 'mysql://root@127.0.0.1:3307/db?charset=utf8&init_command=set%%20character%%20set%%20utf8' # for local testing
DB_URL = os.environ['RDS_HOSTNAME']
DB_PORT = os.environ['RDS_PORT']
DB_USER = os.environ['RDS_USERNAME']
DB_PASS = os.environ['RDS_PASSWORD']
application.config['MYSQL_HOST'] = DB_URL
application.config['MYSQL_USER'] = DB_USER
application.config['MYSQL_PASSWORD'] = DB_PASS
application.config['MYSQL_PORT'] = int(DB_PORT)
application.config['MYSQL_DB'] = 'muse' 

# mysql connector
mysql = MySQL(application)

# add a rule for the index page.
#application.add_url_rule('/', 'index', (lambda: header_text +
#    say_hello() + instructions + footer_text))

# add a rule when the page is accessed with a name appended to the site
# URL.
#application.add_url_rule('/<username>', 'hello', (lambda username:
#    header_text + say_hello(username) + home_link + footer_text))

def insert(query):
    conn = mysql.connection
    cur = conn.cursor()
    cur.execute(query) 
    rv = cur.fetchall()
    conn.commit()
    return str(rv)

def insert_eeg(table, subject_id, timestamp, utimestamp, eeg1, eeg2, eeg3, eeg4, aux1, aux2):
    query = '''INSERT INTO %s (subject_id, timestamp, utimestamp, eeg1, eeg2, eeg3, eeg4, aux1, aux2) VALUES (%d, from_unixtime(%d), %d, %f, %f, %f, %f, %f, %f)''' % (table, subject_id, timestamp, utimestamp, eeg1, eeg2, eeg3, eeg4, aux1, aux2)
    rv = insert(query)
    return rv

def insert_motion(table, subject_id, timestamp, utimestamp, x, y, z, fb, ud, lr):
    query = '''INSERT INTO %s (subject_id, timestamp, utimestamp, x, y, z, fb, ud, lr) VALUES (%d, from_unixtime(%d), %d, %f, %f, %f, %f, %f, %f)''' % (table, subject_id, timestamp, utimestamp, x, y, z, fb, ud, lr)
    rv = insert(query)
    return rv

def insert_artifact(table, subject_id, timestamp, utimestamp, headband, blink, jaw):
    query = '''INSERT INTO %s (subject_id, timestamp, utimestamp, headband, blink, jaw) VALUES (%d, from_unixtime(%d), %d, %f, %f, %f)''' % (table, subject_id, timestamp, utimestamp, headband, blink, jaw)
    rv = insert(query)
    return rv

def insert_acceleration(table, subject_id, timestamp, utimestamp, x, y, z):
    query = '''INSERT INTO %s (subject_id, timestamp, utimestamp, x, y, z) VALUES (%d, from_unixtime(%d), %d, %f, %f, %f)''' % (table, subject_id, timestamp, utimestamp, x, y, z)
    rv = insert(query)
    return rv

def insert_location(table, subject_id, timestamp, utimestamp, latitude, longitude, altitude):
    query = '''INSERT INTO %s (subject_id, timestamp, utimestamp, latitude, longitude, altitude) VALUES (%d, from_unixtime(%d), %d, %f, %f, %f)''' % (table, subject_id, timestamp, utimestamp, latitude, longitude, altitude)
    rv = insert(query)
    return rv


@application.route('/log', methods=['POST'])
def log():
    data = request.get_data()
    print data

    data = request.get_json()
    print data

    table = data['table']
    subject_id = int(data['subject_id']) # int to prevent SQL injections

    rows_str = ''
    rv = ''

    for row in data['rows']:

        utimestamp = int(row['timestamp']) # in microseconds
        timestamp = int(utimestamp / 1e6)

        # do it manually to prevent SQL injections TODO sanitize properly
        if table == 'raw' or table == 'alpha' or table == 'beta' or table == 'delta' or table == 'theta' or table == 'gamma' or table == 'good' or table == 'hsi':
            eeg1 = float(row['eeg1'])
            eeg2 = float(row['eeg2'])
            eeg3 = float(row['eeg3'])
            eeg4 = float(row['eeg4'])
            aux1 = float(row['aux1'])
            aux2 = float(row['aux2'])
            insert_str = '''INSERT INTO %s (subject_id, timestamp, utimestamp, eeg1, eeg2, eeg3, eeg4, aux1, aux2) VALUES ''' % (table)
            rows_str = rows_str + ''', (%d, from_unixtime(%d), %d, %f, %f, %f, %f, %f, %f)''' % (subject_id, timestamp, utimestamp, eeg1, eeg2, eeg3, eeg4, aux1, aux2)
            #rv = insert_eeg(table, subject_id, timestamp, utimestamp, eeg1, eeg2, eeg3, eeg4, aux1, aux2)

        elif table == 'accelerometer' or table == 'gyro':
            x = float(row['x'])
            y = float(row['y'])
            z = float(row['z'])
            fb = float(row['fb'])
            ud = float(row['ud'])
            lr = float(row['lr'])
            insert_str = '''INSERT INTO %s (subject_id, timestamp, utimestamp, x, y, z, fb, ud, lr) VALUES ''' % (table)
            rows_str = rows_str + ''', (%d, from_unixtime(%d), %d, %f, %f, %f, %f, %f, %f)''' % (subject_id, timestamp, utimestamp, x, y, z, fb, ud, lr)
            #rv = insert_motion(table, subject_id, timestamp, utimestamp, x, y, z, fb, ud, lr)

        elif table == 'artifact':
            headband = float(row['headband'])
            blink = float(row['blink'])
            jaw = float(row['jaw'])
            insert_str = '''INSERT INTO %s (subject_id, timestamp, utimestamp, headband, blink, jaw) VALUES ''' % (table)
            rows_str = rows_str + ''', (%d, from_unixtime(%d), %d, %f, %f, %f)''' % (subject_id, timestamp, utimestamp, headband, blink, jaw)
            #rv = insert_artifact(table, subject_id, timestamp, utimestamp, headband, blink, jaw)

        elif table == 'acceleration':
            x = float(row['x'])
            y = float(row['y'])
            z = float(row['z'])
            insert_str = '''INSERT INTO %s (subject_id, timestamp, utimestamp, x, y, z) VALUES ''' % (table)
            rows_str = rows_str + ''', (%d, from_unixtime(%d), %d, %f, %f, %f)''' % (subject_id, timestamp, utimestamp, x, y, z)

        elif table == 'location':
            latitude = float(row['latitude'])
            longitude = float(row['longitude'])
            altitude = float(row['altitude'])
            insert_str = '''INSERT INTO %s (subject_id, timestamp, utimestamp, latitude, longitude, altitude) VALUES ''' % (table)
            rows_str = rows_str + ''', (%d, from_unixtime(%d), %d, %f, %f, %f)''' % (subject_id, timestamp, utimestamp, latitude, longitude, altitude)


    if rows_str:
        rows_str = rows_str[2:]
        query = insert_str + rows_str
        print query
        rv = insert(query)
   
    # return 'hiiiiii ' + str(data) + '\n\n\n\n\n' + str(rv)
    return 'OK'

# TODO use TCP sockets --> https://realpython.com/python-sockets/#echo-server

@application.route('/test')
def test():
    cur = mysql.connection.cursor()
    #cur.execute('''SELECT user, host FROM mysql.user''')
    cur.execute('''SELECT * from test''')
    rv = cur.fetchall()
    return str(rv)

@application.route('/')
def index():
    return 'Hi'

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
