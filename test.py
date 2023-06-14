from geopy.distance import geodesic as geo
from geopy.geocoders import Nominatim
import sqlite3
from jinja2 import Environment, FileSystemLoader


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

    connection = sqlite3.connect("support_files/incidents/database_inc/base_inc.db")
    cursor = connection.cursor()


    cursor.execute(f"SELECT * FROM coordinates")
    result_parcing =  cursor.fetchall()

    output = []


    for index, item in enumerate(result_parcing):
        output_info = []
        location = item[1], item[2]
        if geo(location, data).m < 1000:
            cursor.execute(f"SELECT * FROM incidents WHERE incident_id = {item[0]}")
            output_info.append(list(cursor.fetchone()))
            output_info[0].append(int(geo(location, data).m))
            output  += output_info
    return output



    cursor.close()
    connection.commit()


data = 56.271245, 43.882033

result = search_in_location(data)

print(result[0][6])

# for key in result.keys():
#     print(type(result[key][1]))
#     print(type(result[key][0][0]))

def test_request (db_list, search_title, userid):

    environment = Environment(loader=FileSystemLoader("support_files/incidents/html_temp/"))
    template = environment.get_template("form_request_template.html")

    content = template.render(database=db_list, amount=len(db_list), search_name=search_title)

    with open(f"user_files/{search_title}_{userid}.html", mode="w", encoding="utf-8") as message:
        message.write(content)


test_request(result, "asd", "11111")