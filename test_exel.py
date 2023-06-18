from openpyxl import load_workbook
import json
import sqlite3

base = ["Нет", "14.12.2021", "Дзержинск Львоская 55 13", "Грачев Р.А.", "asdasdasdasdasd", "банк"]
base_1 = ["Грачев Роман", "21.02.1999", "21.02.2022", "Подозреваемый"]

id_crime = 2

connection = sqlite3.connect("test_db.db")
cursor = connection.cursor()

# cursor.execute("""
#     CREATE TABLE IF NOT EXISTS incidents(
#     incident_id INTEGER PRIMARY KEY,
#     revelation TEXT,
#     date_incidient TEXT, 
#     address_incidient TEXT,
#     fellow TEXT,
#     story TEXT,
#     crime_type TEXT,
#     id_crimes INTEGER, 
#     FOREIGN KEY(id_crimes) REFERENCES criminals(id)
#     );
#     """)

# cursor.execute("""
#     CREATE TABLE IF NOT EXISTS criminals(
#     id INTEGER PRIMARY KEY,
#     name TEXT,
#     birthday TEXT,
#     date_catch TEXT,
#     status_crime TEXT);
#     """)

# cursor.execute(
#     """INSERT INTO incidents(
#     revelation, 
#     date_incidient,
#     address_incidient,
#     fellow, story, crime_type) VALUES (?, ?, ?, ?, ?, ?);""", base)

# cursor.execute(
#     """INSERT INTO criminals(
#     name, 
#     birthday,
#     date_catch,
#     status_crime) VALUES (?, ?, ?, ?);""", base_1)

def update(id_crime, id_incident):
    cursor.execute(f"""
        UPDATE incidents SET id_crimes = {id_crime} WHERE incident_id = {id_incident}
    """)

# update(2, 1)

def select():
    cursor.execute(f"""
        SELECT incidents.*, criminals.name FROM incidents
    """)
    print(cursor.fetchall())

select()

cursor.close()
connection.commit()