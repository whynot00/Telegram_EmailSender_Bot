import sqlite3
# from support_files.incidents import normal_address as normalize

from geopy.distance import geodesic as geo
from geopy.geocoders import Nominatim

base = ["Нет", "14.12.2021", "Дзержинск Львоская 55 13", "Грачев Р.А.", "asdasdasdasdasd"]

def insert_story(base):
    base.insert(2, normalize.normalize_address(base[2]))
    base.remove(base[3])

    geolocator = Nominatim(user_agent="Tester")
    location_adress = geolocator.geocode(base[2])
    coordinates = location_adress.latitude, location_adress.longitude

    connection = sqlite3.connect("support_files/incidents/database_inc/base_inc.db")
    cursor = connection.cursor()

    cursor.execute("""
            
        CREATE TABLE IF NOT EXISTS incidents(
        incident_id INTEGER PRIMARY KEY,
        revelation TEXT,
        date_incidient TEXT, 
        address_incidient TEXT,
        fellow TEXT,
        story TEXT,
        crime_type TEXT);
        """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS coordinates(
        incident_id INTEGER PRIMARY KEY,
        latitude INTEGER,
        longitude INTEGER);
        """)

    cursor.execute(
        """INSERT INTO incidents(
        revelation, 
        date_incidient,
        address_incidient,
        fellow, story, crime_type) VALUES (?, ?, ?, ?, ?, ?);""", base)

    cursor.execute(
        """INSERT INTO coordinates(
        latitude, longitude) VALUES (?, ?);""", coordinates)

    connection.commit()

def insert_face_crime(base):
    connection = sqlite3.connect("support_files/incidents/database_inc/base_inc.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS criminals(
            id INTEGER PRIMARY KEY,
            name TEXT,
            birthday TEXT,
            date_catch TEXT,
            status_crime TEXT);
    """)

    cursor.execute("""
        INSERT INTO criminals(name, birthday, date_catch, status_crime) VALUES (?, ?, ?, ?);""", base)

    cursor.close()
    connection.commit()

# list_data = ["Грачев Роман Алексеевич", "11.12.2022", "21.02.2023", "Подозреваемый"]

# insert_face_crime(list_data)