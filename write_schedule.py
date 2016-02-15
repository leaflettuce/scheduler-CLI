from pymongo import MongoClient
from operator import itemgetter


client = MongoClient('localhost', 27017)


def compare_shifts(employee_name, shift_id, db):
    ##returns true of false if employee can accept specific shift
    shifts = db.shifts
    employees = db.employees

    day_time = list(shifts.find({'_id' : shift_id}))

    shift_times = str(day_time[0]['shift'])\
                                .replace('[','').replace(']','')\
                                .replace(' ','').split(',')

    shift_start_time = shift_times[0]

    shift_end_time = shift_times[1]

    shift_day =  day_time[0]['day']

    emp = list(employees.find({'name' : employee_name}))

    days_avail = []
    for i in range(0, len(emp[0]['shifts'])):
        for k,v in emp[0]['shifts'][i].iteritems():
            days_avail.append(k)


    #Compare availability to position, day, and hour of shift
    if emp[0]['position'] == day_time[0]['position']:
        if shift_day in days_avail:
            #[True for k,v in emp[0]['shifts'][i].iteritems() if shift_start_time >= v[0] and shift_end_time <= v[1]]
            for i in range(0,len(emp[0]['shifts'])):
                for k,v in emp[0]['shifts'][i].iteritems():
                    if k == shift_day:
                        if int(shift_start_time) >= v[0]and int(shift_end_time) <= v[1]:
                            return True
                        else: return False
        else: return False
    else: return False


def return_compared_list(shift_list, employee_list, db):
        ##compare all employees and shifts
    avail_list = []

    for shift in shift_list:
        if shift['_id'] == 1138: continue

        for employee in employee_list:
            remove = 0
            if 'week_shifts' in employee.keys():
                for item in employee['week_shifts']:
                    if shift['day'] == item[0]: remove = 1

            if remove == 1:
                continue

            avail_list.append([employee['name'],shift['_id'], compare_shifts(employee['name'], shift['_id'], db), shift['day']])

    return avail_list


def compare_per_loop(shifts_left, employ_temp, final, employee_checker, db):

    shifts = db.shifts

    for comparison in return_compared_list(shifts_left, employ_temp, db):
        if comparison[2]:

            if len(employ_temp) <= 0: break

            for persona in employ_temp:
                get_out = True

                if persona['current'] >= persona['max']:
                    break

                if 'week_shifts' in persona.keys():
                    for shi in persona['week_shifts']:
                        if shi[0] == comparison[3]:
                            break

                if comparison[0] in persona.values():

                    for shif in shifts_left:
                        if comparison[1] in shif.values(): get_out = False

                    if get_out: break

                    current_hours = map(int, list(shifts.find({'_id' : comparison[1]}))[0]['shift'].replace(' ','')\
                                                    .replace('[','').replace(']','').split(','))

                    temp_dict = persona

                    if 'shifts' in temp_dict.keys():
                        del temp_dict['shifts']

                    if 'week_shifts' in temp_dict.keys():
                        temp_dict['week_shifts'].append([list(shifts.find({'_id' : comparison[1]}))[0]['day'],
                                        list(shifts.find({'_id' : comparison[1]}))[0]['shift']])
                    else:
                        temp_dict['week_shifts'] = [[list(shifts.find({'_id' : comparison[1]}))[0]['day'],
                                        list(shifts.find({'_id' : comparison[1]}))[0]['shift']]]

                    check_score = 0
                    if len(final) == 0:
                        temp_dict['current'] = current_hours[1] -current_hours[0]
                        final.append(temp_dict)

                        for e in employ_temp:
                            if e['name'] == temp_dict['name']:
                                employ_temp.remove(e)

                        for s in shifts_left:
                            if s['_id'] == comparison[1]:
                                temp_dict['shift_id'] = comparison[1]
                                shifts_left.remove(s)

                        break

                    else:
                        for check in final:
                            if check['name'] == temp_dict['name']:
                                check['week_shifts'] = temp_dict['week_shifts']
                                check['current'] += current_hours[1] -current_hours[0]

                                check_score = 1

                                for e in employ_temp:
                                    if e['name'] == temp_dict['name']:
                                        employ_temp.remove(e)

                                for s in shifts_left:
                                    if s['_id'] == comparison[1]:
                                        temp_dict['shift_id'] = comparison[1]
                                        shifts_left.remove(s)

                                break

                        if check_score == 0:
                            temp_dict['current'] = current_hours[1] -current_hours[0]
                            final.append(temp_dict)

                            for e in employ_temp:
                                if e['name'] == temp_dict['name']:
                                    employ_temp.remove(e)

                            for s in shifts_left:
                                if s['_id'] == comparison[1]:
                                    temp_dict['shift_id'] = comparison[1]
                                    shifts_left.remove(s)
                            break

    if len(shifts_left) == 0:

        return shifts_left, employ_temp, final, False

    else:
        for person in final:
            employ_temp.append(person)

            for x in range(0, len(employ_temp)):
                employ_temp[x]['from_min'] = float((employ_temp[x]['min'])-
                                                         float(employ_temp[x]['current']))

                # if employ_temp[x]['from_min'] >= 0.9:
                #     for e in employee_checker:
                #         if e['name'] == employ_temp[x]['name']:
                #             employee_checker.remove(e)
                #     del employ_temp[x]

            employ_temp = sorted(employ_temp, key=(itemgetter('from_min')), reverse = True)

    return shifts_left, employ_temp, final, employee_checker


def apply_schedule(employ_temp, db):

        #initialize shifts left to schedule
    shifts_left = list(db.shifts.find())
    final = []
        #initialize temp employee list
    for employee in employ_temp:
        employee['current'] = 0
        employee['mean'] = (employee['min'] + employee['max']) / 2


        #initialize final schedule dict   ...... {empname:, shifts:[day, hour], current:, min:, mean:, max:}

    employee_checker = list(db.employees.find())

    while True:

        if len(shifts_left) <= 1 or len(employee_checker) <= 0: break

        shifts_left, employ_temp, final, employee_checker = compare_per_loop(shifts_left, employ_temp, final, employee_checker, db)

    return final
