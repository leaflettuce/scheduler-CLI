#used to create, remove, and update shifts
import os
from pymongo import MongoClient
import operator
import time
from pprint import pprint

#########
###add fake id 1138 (check if it has it first!)
######### #


client = MongoClient('localhost', 27017)


#testing

def run_shifts(dbToUse):

    db = client[dbToUse]


    class Shift:

        def __init__(self):

            #ask user for day, pos, and shift
            pos = raw_input('\nNew shift\'s position? : ').lower()
            day = raw_input('\nDay of shift? : ').lower()
            print('\n --Use military time below!--\n')
            shift_start = int(raw_input('Shift\'s start hour? : '))
            shift_end = int(raw_input('\nShift\'s end hour? : '))

            self.pos = pos
            self.day = day
            self.shift = '[{}, {}]'.format(shift_start, shift_end)


        def add_shift(self):

            if 'shifts' in db.collection_names():
                shift_ids = list(db.shifts.find())
                shift_id = (int(sorted(shift_ids, key = operator.itemgetter('_id'), reverse = True)[0]['_id']) + 1)

            else:
                shift_id = 1


            db.shifts.insert({'_id' : shift_id,
                              'day' : self.day,
                              'position' : self.pos,
                              'shift' : self.shift})

        def update_shifts(self):

            pass
            #add update function

    def remove_shift():

        r_day = raw_input('\nWhat day of the week is shift to remove?: ').lower()

        r_shift = raw_input('What shift to remove? : \n Enter with \', \' in between times. '
                                'example: (start, end)\n shift: ')
        r_shift_update = '[{}]'.format(r_shift)

        r_pos = raw_input('What position it this shift for?: ').lower()

        db.shifts.remove({'day' : r_day, 'shift' : r_shift_update, 'position' : r_pos})


    while True:
        what = raw_input('''
        Shift Editer
        ------------------
        l) - list shifts
        a) - add shift
        r) - remove shift
        q) - quit shift editor \n\nEnter an option: ''').lower()

        if what == 'q':
            time.sleep(1)
            break

        if what == 'l':
            list_shifts(db)
            time.sleep(2)
            continue

        if what == 'a':
            nshift = Shift()

            nshift.add_shift()
            which_one = 'added'

        if what == 'r':

            remove_shift()
            which_one = 'removed'

        else:
            print 'Invalid entry.. Try again'

        if which_one:
            print '\n' +'***********'*2

            if which_one == 'added':
                print('Successfully added shift')

            if which_one == 'removed':
                print('Successfully removed shift')

            print '***********'*2
            time.sleep(2)

def list_shifts(db):
    pprint(list(db.shifts.find({},{'_id' : 0,'position':1, 'day' : 1, 'shift' : 1})))