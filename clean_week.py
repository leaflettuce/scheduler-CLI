import csv
import os.path
from pymongo import MongoClient


client = MongoClient('localhost', 27017)


def clean(dbToUse, week_name):

    db = client[dbToUse]
    data = list(db[week_name].find())

    writer, file = create_csv_file(dbToUse, week_name)

    writer.writerow(['day','shift','name','position','min','max','current'])

    for row in data:
        for shifts in row['week_shifts']:
            day = shifts[0]
            shift = shifts[1]
            name = row['name']
            position = row['position']
            min1 = row['min']
            max1 = row['max']
            current = row['current']

            writer.writerow([day,shift,name,position,min1,max1,current])

    file.close()


def create_csv_file(dbToUse, week_name):

    save_path = os.path.dirname(os.path.abspath(__file__)) + '/visuals/data/'

    name_of_file = dbToUse +'-' + week_name

    completeName = os.path.join(save_path, name_of_file+".csv")

    file = open(completeName, "w")

    return csv.writer(file, delimiter = ','), file