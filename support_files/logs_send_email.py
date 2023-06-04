import csv
from datetime import datetime, date, time


def logs_email_write(data_dict):
    date_time = datetime.today().strftime("%d.%m.%Y %H:%M")
    data = [
        [data_dict['user_username'], data_dict['user_id'], data_dict['recipient'], data_dict['type'], date_time]
        ]
        
    with open("logs/logs_email.csv", "a") as write_object:
        writer = csv.writer(write_object)
        for row_item in data:
            writer.writerow(row_item)

