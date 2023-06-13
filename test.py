from geopy.distance import geodesic as geo
from geopy.geocoders import Nominatim
import sqlite3


# geolocator = Nominatim(user_agent="Tester")

# adress = "Нижний Новгород Львовская 31"

# location_1 = (56.268312, 43.881331)

# location_adress = geolocator.geocode(adress)

# location = location_adress.latitude, location_adress.longitude

# print(location)

# print(round(geo(location, location_1).m, 0))

base = ["Нет", "14.12.2021", "Нижний Новгород Дьяконова 10 55", "Грачев Р.А.", "asdasdasdasdasd"]


def test(base):
    geolocator = Nominatim(user_agent="Tester")
    print(geolocator)
    connection = sqlite3.connect("base_inc.db")
    cursor = connection.cursor()

    location_adress = geolocator.geocode(base[2])
    print(location_adress)
    coordinates = location_adress.latitude, location_adress.longitude



    cursor.execute("""
            
        CREATE TABLE IF NOT EXISTS incidents(
        incident_id INTEGER PRIMARY KEY,
        revelation TEXT,
        date_incidient TEXT, 
        address_incidient TEXT,
        fellow TEXT,
        story TEXT);
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
        fellow, story) VALUES (?, ?, ?, ?, ?);""", base)

    cursor.execute(
        """INSERT INTO coordinates(
        latitude, longitude) VALUES (?, ?);""", coordinates)

    connection.commit()


def search_in_location(data):

    connection = sqlite3.connect("base_inc.db")
    cursor = connection.cursor()


    cursor.execute(f"SELECT * FROM coordinates")
    result_parcing =  cursor.fetchall()


    output_info = []
    output = {}


    for item in result_parcing:
        location = item[1], item[2]
        if round(geo(location, data).m, 0) < 5000:
            cursor.execute(f"SELECT * FROM incidents WHERE incident_id = {item[0]}")
            output_info.append(cursor.fetchone())
            output_info.append(round(geo(location, data).m, 0))
            output[f"id_{item[0]}"] = output_info

    return output



    cursor.close()
    connection.commit()

# test(base)
data = 56.268312, 43.881331

result = search_in_location(data)

print(result)

for key in result.keys():
    print(result[key][1])