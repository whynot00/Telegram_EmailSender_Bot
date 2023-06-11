import sqlite3
from support_files.incidents import normal_address as normalize

base = ["Нет", "14.12.2021", "г. Дзержинск, ул. Львоская, д. 55, кв. 13", "Грачев Р.А.", "asdasdasdasdasd"]

def insert_story(base):
    base.insert(2, normalize.normalize_address(base[2]))
    base.remove(base[3])

    connection = sqlite3.connect("support_files/incidents/database_inc/base_inc.db")
    cursor = connection.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS incidents(
        incident_id INTEGER PRIMARY KEY,
        revelation TEXT,
        date_incidient TEXT, 
        address_incidient TEXT,
        fellow TEXT,
        story TEXT);""")

    cursor.execute(
        """INSERT INTO incidents(
        revelation, 
        date_incidient,
        address_incidient,
        fellow, story) VALUES (?, ?, ?, ?, ?);""", base)

    connection.commit()