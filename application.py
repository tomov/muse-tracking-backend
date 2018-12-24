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

def select(query):
    conn = mysql.connection
    cur = conn.cursor()
    cur.execute(query) 
    rv = cur.fetchall()
    return rv

def insert_eeg(table, subject_id, timestamp, utimestamp, eeg1, eeg2, eeg3, eeg4, aux1, aux2):
    query = '''INSERT INTO %s (subject_id, timestamp, utimestamp, eeg1, eeg2, eeg3, eeg4, aux1, aux2) VALUES (%d, from_unixtime(%d), %d, %f, %f, %f, %f, %f, %f)''' % (table, subject_id, timestamp, utimestamp, eeg1, eeg2, eeg3, eeg4, aux1, aux2)
    rv = insert(query)
    return rv

def insert_motion(table, subject_id, timestamp, utimestamp, x, y, z):
    query = '''INSERT INTO %s (subject_id, timestamp, utimestamp, x, y, z) VALUES (%d, from_unixtime(%d), %d, %f, %f, %f)''' % (table, subject_id, timestamp, utimestamp, x, y, z)
    rv = insert(query)
    return rv

def insert_artifact(table, subject_id, timestamp, utimestamp, headband, blink, jaw):
    query = '''INSERT INTO %s (subject_id, timestamp, utimestamp, headband, blink, jaw) VALUES (%d, from_unixtime(%d), %d, %f, %f, %f)''' % (table, subject_id, timestamp, utimestamp, headband, blink, jaw)
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
            insert_str = '''INSERT INTO %s (subject_id, timestamp, utimestamp, x, y, z) VALUES ''' % (table)
            rows_str = rows_str + ''', (%d, from_unixtime(%d), %d, %f, %f, %f)''' % (subject_id, timestamp, utimestamp, x, y, z)
            #rv = insert_motion(table, subject_id, timestamp, utimestamp, x, y, z)

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


# extract rolling average from signal s1 with timestamps t1
# using rolling window size w1
# and correspondingly for signal s2 but after a time lag of lag
#
# s3 is the hsi scores for s1, with timestamps t3, "flanking" window of s1 (w1) by w3 on each side
#
# s = signal
# t = timestamps
# w = window size
#
def extract_for_comparison(s1, t1, w1, lag, s2, t2, w2, s3, t3, w3):
    l1 = 0 # first index within current rolling window
    r1 = 1 # 1 + last index within current rolling window
    l2 = 0
    r2 = 1
    l3 = 0
    r3 = 1
    assert(len(s1) == len(t1))
    assert(len(s2) == len(t2))
    assert(len(s3) == len(t3))

    s1_win = s1[0] # sum of s1 within rolling window
    s2_win = s2[0]
    s3_win = s3[0]

    ret1 = []
    ret2 = []
    ret3 = []

    while True:

        # expand rolling window of signal 1 until we span an interval w1 (but not larger)
        #
        while r1 < len(s1) and t1[r1] - t1[l1] <= w1:
            s1_win += s1[r1]
            r1 += 1

        # shift rolling window of signal 2 until it's at least lag away from window of signal 1
        #
        while l2 + 1 < len(s2) and t2[l2] - t1[r1 - 1] < lag:
            s2_win -= s2[l2]
            l2 += 1

        # if we can't shift rolling window 2 any more -> break
        #
        if l2 + 1 >= len(s2) and t2[l2] - t1[r1 - 1] < lag:
            break

        # expand rolling window of signal 2 until we span an interval w2 (but not larger)
        #
        while r2 < len(s2) and t2[r2] - t2[l2] <= w2:
            s2_win += s2[r2]
            r2 += 1

        # shift rolling window of s3 to w3 before window of s1 
        #
        while l3 + 1 < len(s3) and t3[l3] < t1[l1] - w3:
            s3_win -= s3[l3]
            l3 += 1

        # expand rolling window of s3 to w3 after window of s1
        #
        while r3 < len(s3) and t3[r3] <= t1[r1 - 1] + w3:
            s3_win += s3[r3]
            r3 += 1

        # if conditions are satisfied, add data points
        #
        if t1[r1 - 1] - t1[l1] <= w1 and t2[r2 - 1] - t2[l2] <= w2 and t2[l2] - t1[r1 - 1] >= lag and l3 < r3:
            s1_avg = s1_win / (r1 - l1)
            s2_avg = s2_win / (r2 - l2)
            s3_avg = s3_win / (r3 - l3)
            if s3_avg <= 2: # avg HSI should be better than 2
                ret1.append(s1_avg)
                ret2.append(s2_avg)
                ret3.append(s3_avg)
        #        print '                add', (r1 - l1), '  ', (r2 - l2), ' ', (r3 - l3)

        #print l1, r1, l2, r2, l3, r3, '  -> ', t1[r1 - 1] - t1[l1], t2[l2] - t1[r1 - 1], t2[r2 - 1] - t2[l2], t3[r3 - 1] - t3[l3], '   -- ', t3[l3], '[', t1[l1], t1[r1], ']', t3[r3]

        # shift over rolling window of signal 1 
        #
        s1_win -= s1[l1]
        l1 += 1


    return ret1, ret2, ret3


@application.route('/query_test')
def query_test():
    rv = select('''SELECT eeg1, utimestamp / 1000 FROM theta LIMIT 10000''')
    s1 = []
    t1 = []
    for row in rv:
        s1.append(row[0])
        t1.append(row[1])
    #w1 = 250
    w1 = 500

    rv = select('''SELECT SQRT(POW(x, 2) + POW(y, 2) + POW(z, 2)), utimestamp / 1000  FROM accelerometer LIMIT 10000''')
    s2 = []
    t2 = []
    for row in rv:
        s2.append(row[0])
        t2.append(row[1])
    #w2 = 250
    w2 = 500

    rv = select('''SELECT eeg1, utimestamp / 1000 FROM hsi LIMIT 10000''')
    s3 = []
    t3 = []
    for row in rv:
        s3.append(row[0])
        t3.append(row[1])
    w3 = 500

    lag = 0
    ret1, ret2, ret3 = extract_for_comparison(s1, t1, w1, lag, s2, t2, w2, s3, t3, w3)
    return str(len(ret1))


@application.route('/viz')
def viz():
    return ''


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
