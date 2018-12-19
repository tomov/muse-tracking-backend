### To run locally:

clone repo

    export RDS_HOSTNAME=127.0.0.1
    export RDS_USERNAME=root
    export RDS_PASSWORD=password
    export RDS_PORT=3306

    sudo pip install virtualenv
    virtualenv virt 
    source virt/bin/activate
    pip install -r requirements.txt

Make sure you have MySQL running locally on port 3306 or remotely on Amazon RDS (change exports above accordingly).

Also create a database `db`.

    python application.py

### To deploy on Amazon Elastic Beanstalk:

TODO

