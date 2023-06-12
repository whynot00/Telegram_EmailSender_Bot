import sqlite3
from datetime import datetime, date, time


param = ["romans516", "981397216", "bot-help440@mail.ru", "photo", "01.06.2023 22:13"]

def logs(data_dict, action):
    con = sqlite3.connect("logs/logs.db")
    cur = con.cursor()

    data_dict.append(str(datetime.today().strftime("%d.%m.%Y %H:%M")))
    
    if action == "email_send":
        cur.execute(f"CREATE TABLE IF NOT EXISTS {action}(user_name TEXT, user_id TEXT, recipient TEXT, type TEXT, datetime TEXT);")
        cur.execute(f"INSERT INTO {action} VALUES(?, ?, ?, ?, ?);", data_dict)

    elif action == "change_powers":
        cur.execute(f"CREATE TABLE IF NOT EXISTS {action}(user_name TEXT, user_id TEXT, change TEXT, chduser_id TEXT, datetime TEXT);")
        cur.execute(f"INSERT INTO {action} VALUES(?, ?, ?, ?, ?);", data_dict)

    elif action == "incidents":
        cur.execute(f"CREATE TABLE IF NOT EXISTS {action}(user_name TEXT, user_id TEXT, type_story TEXT, content TEXT, datetime TEXT);")
        cur.execute(f"INSERT INTO {action} VALUES(?, ?, ?, ?, ?);", data_dict)

    con.commit()

