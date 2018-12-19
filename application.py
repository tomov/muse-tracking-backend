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

@application.route('/log', methods=['POST'])
def log():
    data = request.get_data()
    print data

    data = request.get_json()
    print data

    return 'hiiiiii' + str(data)

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
