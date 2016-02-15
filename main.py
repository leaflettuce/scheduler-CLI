#### initialize db name and call options
from pymongo import MongoClient
from run import initialize_collection
from employee import run
from shifts import run_shifts
from clean_week import clean
from viualize import visualize
import sys


client = MongoClient('localhost', 27017)


def start_up():

    print '''

####################
EMPLOYEE SCHEDULER
####################
    '''
    print '''(Please enter company name to
call or create a database to work with!)\n'''
    dbToUse = str(raw_input('What is the database name?: '))

    while True:

        print '\n*********************'
        print 'Using {} database!'.format(dbToUse)
        print '*********************'

        print '''\n\tMAIN
    ------------------
    (e) - employee editor
    (s) - shift editor
    (w) - write a schedule
    (p) - print a schedule
    (c) - change database
    (q) - quit\n'''

        option = raw_input('What would you like to do?: '.lower())

        if option == 'q':
            sys.exit('Goodbye.')

        if option == 'e':
            run(dbToUse)

        if option == 'p':
            week_name = raw_input('What is the week name you would like to view?: ')
            clean(dbToUse, week_name)
            visualize(dbToUse, week_name)

        if option == 's':
            run_shifts(dbToUse)

        if option =='w':
            initialize_collection(dbToUse)

        if option == 'c':
            print '''\n(Please enter company name to
call or create a database to work with!)\n'''

            dbToUse = str(raw_input('What is the database name?: '))


start_up()