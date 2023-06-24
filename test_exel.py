from openpyxl import load_workbook
import json
import sqlite3

connection = sqlite3.connect("support_files/incidents/database_inc/base_inc.db")
cursor = connection.cursor()

cursor.execute("""DROP TABLE criminal_case""")
cursor.execute("""DROP TABLE criminals""")
cursor.execute("""DROP TABLE incidents""")
cursor.execute("""DROP TABLE curators""")
cursor.execute("""DROP TABLE coordinates""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS criminal_case(
    id INTEGER PRIMARY KEY,
    kusp TEXT,
    num_case TEXT,
    date_case TEXT,
    article TEXT);
""")


cursor.execute("""
    CREATE TABLE IF NOT EXISTS criminals(
    id INTEGER PRIMARY KEY,
    name TEXT,
    birthday TEXT,
    date_catch TEXT,
    status_crime TEXT,
    curator_tg_id INTEGER,
    tg_id INTEGER,
    FOREIGN KEY(curator_tg_id) REFERENCES curators(id_tg));
    """)

cursor.execute("""
    CREATE TABLE IF NOT EXISTS incidents(
    incident_id INTEGER PRIMARY KEY,
    revelation TEXT,
    date_incidient TEXT, 
    address_incidient TEXT,
    fellow TEXT,
    story TEXT,
    crime_type TEXT,
    id_crimes INTEGER,
    kusp INTEGER,
    FOREIGN KEY(id_crimes) REFERENCES criminals(id),
    FOREIGN KEY(kusp) REFERENCES criminal_case(kusp)
    );
    """)

cursor.execute("""
    CREATE TABLE IF NOT EXISTS curators(
    id INTEGER PRIMARY KEY,
    id_tg TEXT,
    username_tg TEXT,
    oper_drove TEXT);
    """)

cursor.execute("""
    CREATE TABLE IF NOT EXISTS coordinates(
    incident_id INTEGER PRIMARY KEY,
    latitude INTEGER,
    longitude INTEGER);
    """)

cursor.close()
connection.commit()