#used to create, remove, and update employees
import os
from pymongo import MongoClient
import operator
import time
from pprint import pprint

#########
###add fake id 1138 (check if it has it first!)
#########


client = MongoClient('localhost', 27017)


#testing

def run(dbToUse):

    db = client[dbToUse]


    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

    hours = []
    for _ in range(7):
        hours.append((6, 22))


    class Employee:

        def __init__(self, name, limited = False):

            #ask user for pos, min, and max
            pos = raw_input('\n{}\'s position? :'.format(name)).lower()
            min = int(raw_input('\n{}\'s minimum weekly hours? :'.format(name)))
            max = int(raw_input('\n{}\'s maximum weekly hours? :'.format(name)))
            #if limited, allows input of availability
            availability = []
            if limited:
                limited_avail = raw_input('\nEnter availability. \n(example: \'day-start-end,etc\')\n :').split(',')
                for day in limited_avail:
                    day_split = day.split('-')
                    availability.append({day_split[0]:(int(day_split[1]),
                                                      int(day_split[2]))})

            else:
                for x in range(0,7):
                    availability.append({days[x]:hours[x]})


            self.name = name
            self.pos = pos
            self.min = min
            self.max = max
            self.limited = limited
            self.avail = availability


        def add_employee(self):

            if 'employees' in db.collection_names():
                employee_ids = list(db.employees.find())
                employee_id = int(sorted(employee_ids, key = operator.itemgetter('_id'), reverse = True)[0]['_id']) + 1
            else:
                employee_id = 1


            db.employees.insert({'_id' : employee_id,
                                 'name' : self.name,
                                 'position' : self.pos,
                                 'shifts' : self.avail,
                                 'limited' : self.limited,
                                 'min' : self.min,
                                 'max' : self.max})


        def remove_employee(self):

            db.employees.remove({'name' : self.name})


        def update_employee(self):

            pass
            #add update function

    while True:
        what = raw_input('''
        Employee Roster Editer
        ----------------------
        l) - list employees
        c) - check an employee's availability
        a) - add employee
        r) - remove employee
        u) - update employee
        q) - quit employee editor \n\nEnter an option: ''').lower()

        if what == 'q':
            time.sleep(1)
            break

        if what == 'l':
            list_employees(db)
            time.sleep(2)
            continue

        if what == 'c':
            name_to_see = raw_input('Who do you want to look at?: ')
            pprint(list(db.employees.find({'name' : name_to_see}, {'_id':0,'name':1,'position':1,'min':1,'max':1,'shifts':1})))
            time.sleep(5)
            continue

        if what == 'a':
            emp = raw_input('\nEmployee\'s name? :')
            if raw_input('\nAny limited availability? \nstandard availability is (6am-10pm) every day.\nYn : ').lower() == 'y':
                limit = True
            else:
                limit = False

            if limit:
                nemp = Employee(emp, limited=True)
            else:
                nemp = Employee(emp)

            nemp.add_employee()
            which_one = 'added'

        if what == 'r':
            emp = raw_input('\nEmployee\'s name? :')
            db.employees.remove({'name' : emp})
            which_one = 'removed'

        if what == 'u':
            emp = raw_input('\nEmployee\'s name? :')
            change = raw_input('Change position, min, max, or shifts?').lower()

            if change == 'shifts':
                change_to = []
                limited_avail = raw_input('\nEnter availability. \n(example: \'day-start-end,etc\')\n :').split(',')
                for day in limited_avail:
                    day_split = day.split('-')
                    change_to.append({day_split[0]:(int(day_split[1]),
                                                      int(day_split[2]))})

            else:
                change_to = raw_input('New input?: ')
                if change == 'min' or change == 'max':
                    change_to = int(change_to)

            db.employees.update({'name' : emp}, {'$set' : {change : change_to}})
            which_one = 'updated'

        if which_one:
            print '\n' +'***********'*2
            print('{} {} successfully!'.format(emp, which_one))
            print '***********'*2
            time.sleep(2)


def list_employees(db):
    pprint(list(db.employees.find({},{'_id' : 0,'name' : 1, 'position' : 1})))