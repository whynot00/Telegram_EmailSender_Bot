import sqlite3

with open("sss.txt", "r") as file:
    sss = file.read()
    print(sss[0])

table_names = ["drop_farsen", "saledroppp"]

def select_member_fromdb(userid):
    con = sqlite3.connect('logs/member_list.db')
    cursor = con.cursor()
    for item in table_names:
        cursor.execute(f"SELECT * FROM {table_names[table_names.index(item)]} WHERE userid = {userid}")
        records = cursor.fetchall()
        if not records:
            break
        else:
            print(f"В базе {table_names[table_names.index(item)]} есть")

    cursor.close()
    con.close()

# select_member_fromdb("822912189")