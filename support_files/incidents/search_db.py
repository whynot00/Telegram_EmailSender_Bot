import sqlite3
from support_files.incidents import normal_address as normalize

from geopy.distance import geodesic as geo
from geopy.geocoders import Nominatim

date = "23.10.2022"
address = "Нижний Новгород"


# Поиск по SQL-таблице по дате и по адресу
def search_in_base(data, mode):

    connection = sqlite3.connect("support_files/incidents/database_inc/base_inc.db")
    cursor = connection.cursor()

    if mode == "date":    
        cursor.execute(f"SELECT * FROM incidents WHERE date_incidient LIKE '{data}'")
        return cursor.fetchall()
        
    elif mode == "address":
        cursor.execute(f"SELECT * FROM incidents WHERE address_incidient LIKE '%{data}%'")
        return cursor.fetchall()

    elif mode == "id":
        cursor.execute(f"SELECT * FROM incidents WHERE incident_id LIKE '{data}'")
        return cursor.fetchall()

    elif mode == "locate":
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
                output += output_info\

        return output

    elif mode == "reference":
        cursor.execute(f"SELECT * FROM reference WHERE search_name LIKE '%{data}%'")
        return cursor.fetchall()
    
    elif mode == "criminals":
        print(data, type(data))
        cursor.execute(f"SELECT * FROM criminals WHERE LOWER(name) LIKE LOWER('%{data}%')")
        return cursor.fetchall()

    cursor.close()
    connection.commit()


def search_in_base_revelation(mode):

    connection = sqlite3.connect("support_files/incidents/database_inc/base_inc.db")
    cursor = connection.cursor()

    if mode == "Да":
        cursor.execute(f"SELECT * FROM incidents WHERE revelation LIKE 'Да'")
        return cursor.fetchall()

    elif mode == "Нет":
        cursor.execute(f"SELECT * FROM incidents WHERE revelation LIKE 'Нет'")
        return cursor.fetchall()

    elif mode == "all":
        cursor.execute(f"SELECT * FROM incidents")
        return cursor.fetchall()

    cursor.close()
    connection.commit()


