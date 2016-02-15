from pymongo import MongoClient
import write_schedule
import check_hours
import time


client = MongoClient('localhost', 27017)


def initialize_collection(dbToUse):

    db = client[dbToUse]

    #create list of shifts and empoyees
    shifts = list(db['shifts'].find())


    print '''\n###################
Automated scheduler
###################\n'''

    ###initialize
    col_name = str(raw_input('What week is this for? \n(EX: \'02.31.2015\' or \'week_one\')\n\n week: '))
    # db.createCollection(col_name)
    # collection = db.getCollection(col_name)

    vacation = raw_input('\nIs anyone on vacation or otherwise unavaiable this week? \n(Yn) : ')
    emp_list = list(db.employees.find())


    #persons on vacation or unavailable check

    if vacation == 'y':
        names_missing = raw_input('\nEnter name(s).. \nif multiple please separate with (,) \nNO SPACES: ')
        if ',' in names_missing:
            names_missing = names_missing.split(',')


        first_emp_list = emp_list
        ####Remove invalid employees from collection
        for person in first_emp_list:

            if isinstance(names_missing, list):
                for name in names_missing:
                    if name in person.values():
                        emp_list = [x for x in emp_list if x['name'] != name]

            else:
                if names_missing in person.values():
                    emp_list = [x for x in emp_list if x['name'] != names_missing]


        ###CHECK FOR EMP TO SHIFT HOURS

    do_it = 0
    for emp in emp_list:
        if 'manager' in emp.values():
            do_it = 1
    if do_it == 1:
        man = check_hours.manager_checker(shifts, emp_list)
    else:
        man = False

    do_it = 0
    for emp in emp_list:
        if 'associate' in emp.values():
            do_it = 1
    if do_it == 1:
        asso = check_hours.associate_checker(shifts, emp_list)
    else:
        asso = False

    if not man or not asso:
        print '\n**************************************************************'
        print 'There is not enough availability on your roster for amount of shifts.'

        if not man and not asso:
            print 'Need more Manager AND Associate positions!  try again with more'

        elif man and not asso:
            print 'Please add more Associate Positions and try again.'

        elif asso and not man:
            print 'Please add more Manager Positions and try again.'

        print '****************************************************************'
        time.sleep(2)
        return

    #write schedule to list
    else:
        append_list = write_schedule.apply_schedule(emp_list, db)

    for document in append_list:
        db[col_name].insert(document)


    print '\n\n###################################'
    print '{} schedule created successfully!'.format(col_name)
    print '####################################\n'
    time.sleep(2)
    return
