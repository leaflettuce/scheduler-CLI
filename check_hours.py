#check managers and associates for enough hours to fill schedule

def manager_checker(shifts, emps):

    man_week_shift_hours = 0
    man_week_emp_hours = 0

    #for managers
    for shift in shifts:
        if shift['position'] == 'manager':
            time = shift['shift'].replace('[','').replace(']','').replace(' ','').split(',')
            man_week_shift_hours += int(time[1]) - int(time[0])

    for emp in emps:
        if emp['position'] == 'manager':
            man_week_emp_hours += (int(emp['max']) + int(emp['min'])) / 2

    if man_week_shift_hours > man_week_emp_hours:
        return False
    else:
        return True


def associate_checker(shifts, emps):

    asso_week_shift_hours = 0
    asso_week_emp_hours = 0

    #for managers
    for shift in shifts:
        if shift['position'] == 'associate':
            time = shift['shift'].replace('[','').replace(']','').replace(' ','').split(',')
            asso_week_shift_hours += int(time[1]) - int(time[0])

    for emp in emps:
        if emp['position'] == 'associate':
            asso_week_emp_hours += (int(emp['max']) + int(emp['min'])) / 2

    if asso_week_shift_hours > asso_week_emp_hours:
        return False

    else:
        return True


if __name__ == "__main__":
    manager_checker()
    associate_checker()

