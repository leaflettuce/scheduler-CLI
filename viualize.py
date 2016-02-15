from prettytable import PrettyTable
import csv
import os




def visualize(dbToUse, week_name):

    day_order = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']

    make_ordered_csv(dbToUse, week_name, day_order)
    make_table(dbToUse, week_name, day_order)
    make_plots(dbToUse, week_name)


def make_ordered_csv(dbToUse, week_name, day_order):

    ordered_rows = organize_by_days(dbToUse, day_order, week_name)

    writer, file = create_csv_file(dbToUse, week_name)

    writer.writerow(['day','shift','name','position','min','max','current'])
    for item in ordered_rows:
        writer.writerow(item)

    file.close()


def make_table(dbToUse, week_name, day_order):

    reader, file = open_ordered_csv(dbToUse, week_name)

    header = ['employee']
    for day in day_order:
        header.append(day)
    header.append('total hours') ##
    x = PrettyTable(header)

    names = {}
    reader.next()
    for row in reader:
        if row[2] not in names:
            names[row[2]] = {row[0] : row[1]}
        else:
            names[row[2]][row[0]] = row[1]

    write_this = {}
    for k,v in names.iteritems():

        name = k
        for k,v in names[k].iteritems():
            day = k
            shift = v

            if name not in write_this:
                write_this[name] = [[day, shift.replace('[','').replace(']','').replace(',',' -')]]
            else:
                write_this[name].append([day, shift.replace('[','').replace(']','').replace(',',' -')])


    total_shift_hours = 0
    for k,v in write_this.iteritems():
        shifts = ['name', 'monday', 'tuesday', 'wednesday', 'thursday' ,'friday' ,'saturday', 'sunday', 'total']
        shifts[0] = k
        total = 0
        for i in range(0,len(v)):
                for index, shift in enumerate(shifts):
                    if v[i][0] == shifts[index]:
                        shifts[index] = v[i][1]
                        total += int(v[i][1].split(' - ')[1]) - int(v[i][1].split(' - ')[0])
                        total_shift_hours += int(v[i][1].split(' - ')[1]) - int(v[i][1].split(' - ')[0])
        shifts[8] = total

        for index, shift in enumerate(shifts):
            for d in ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']:
                if shifts[index] == d:
                    shifts[index] = ''

        x.add_row(shifts)


    x.hrules = True
    data = x.get_string()

    y = PrettyTable()
    y.add_row(['Total Hours This Week', total_shift_hours])
    y.header = False
    y_data = y.get_string()

    path = os.path.dirname(os.path.abspath(__file__)) + '/visuals/'

    name_of_file = dbToUse + '-' + week_name

    completeName = os.path.join(path, name_of_file+".txt")

    with open(completeName, 'w') as f:
        f.write('\n ' + dbToUse.title() + ' - ' + week_name.title() + ' Employee Schedule\n----------------------------\n\n')
        f.write(data)
        f.write('\n\n')
        f.write(y_data)

    file.close()


def make_plots(dbToUse, week_name):

    pass


def open_csv(dbToUse, week_name):

    path = os.path.dirname(os.path.abspath(__file__)) + '/visuals/data/'

    name_of_file = dbToUse + '-' + week_name

    completeName = os.path.join(path, name_of_file+".csv")

    file = open(completeName, "r")

    return csv.reader(file, delimiter = ','), file


def open_ordered_csv(dbToUse, week_name):

    path = os.path.dirname(os.path.abspath(__file__)) + '/visuals/data/'

    name_of_file = dbToUse + '-' + week_name

    completeName = os.path.join(path, name_of_file+"-ordered.csv")

    file = open(completeName, "r")

    return csv.reader(file, delimiter = ','), file


def organize_by_days(dbToUse, day_order, week_name):

    ordered_rows = []

    for day_name in day_order:

        day_group = []

        reader, file = open_csv(dbToUse, week_name)

        for row in reader:

            if row[0] == day_name:

                day_group.append(row)

        day_group = sorted(day_group, key = lambda x : int(x[1].replace('[','').replace(']','')
                                                .replace(' ','').split(',')[0]))


        for d in day_group:
            ordered_rows.append(d)

        file.close()

    return ordered_rows


def create_csv_file(dbToUse, week_name):

    save_path = os.path.dirname(os.path.abspath(__file__)) + '/visuals/data/'

    name_of_file = dbToUse +'-' + week_name

    completeName = os.path.join(save_path, name_of_file+'-ordered'+".csv")

    file = open(completeName, "w")

    return csv.writer(file, delimiter = ','), file