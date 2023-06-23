import sqlite3
from support_files.incidents import normal_address as normalize

from geopy.distance import geodesic as geo
from geopy.geocoders import Nominatim

# Поиск по SQL-таблице по дате и по адресу
def search_in_base(data, mode):

    connection = sqlite3.connect("support_files/incidents/database_inc/base_inc.db")
    cursor = connection.cursor()

    if mode == "date":    
        cursor.execute(f"""
        SELECT incidents.*,
        criminal_case.num_case, criminal_case.date_case, criminal_case.article, 
        criminals.name, criminals.date_catch, criminals.status_crime, criminals.tg_id
        FROM incidents 
        FULL JOIN criminal_case ON criminal_case.kusp=incidents.kusp 
        FULL JOIN  criminals ON criminals.id=incidents.id_crimes
        WHERE incidents.date_incidient LIKE "%{data}%"
        """)
        
    elif mode == "address":
        cursor.execute(f"""
        SELECT incidents.*,
        criminal_case.num_case, criminal_case.date_case, criminal_case.article, 
        criminals.name, criminals.date_catch, criminals.status_crime, criminals.tg_id
        FROM incidents 
        FULL JOIN criminal_case ON criminal_case.kusp=incidents.kusp 
        FULL JOIN  criminals ON criminals.id=incidents.id_crimes
        WHERE incidents.address_incidient LIKE "%{data}%"
        """)

    elif mode == "id":
        cursor.execute(f"""
        SELECT incidents.incident_id, incidents.revelation, incidents.date_incidient, incidents.address_incidient,
        incidents.fellow, incidents.story, incidents.crime_type, incidents.kusp,
        criminal_case.num_case, criminal_case.date_case, criminal_case.article, 
        criminals.name, criminals.date_catch, criminals.status_crime, criminals.tg_id, criminals.curator_tg_id, criminals.birthday
        FROM incidents 
        FULL JOIN criminal_case ON criminal_case.kusp=incidents.kusp 
        FULL JOIN  criminals ON criminals.id=incidents.id_crimes
        WHERE incidents.incident_id={data}
        """)

        result_searching = cursor.fetchall()[0]

        dict_search = {
            "incident": [],
            "criminal_case": [],
            "criminals": []
        }
        x = 0
        while x < 17:
            if x < 7:
                if result_searching[x] is None:
                    dict_search["incident"].append("-")
                else:
                    dict_search["incident"].append(str(result_searching[x]))
            elif x >= 7 and x < 11:
                if result_searching[x] is None:
                    dict_search["criminal_case"].append("-")
                else:
                    dict_search["criminal_case"].append(str(result_searching[x]))
            elif x >= 11 and x < 17:
                if result_searching[x] is None:
                    dict_search["criminals"].append("-")
                else:
                    dict_search["criminals"].append(str(result_searching[x]))
            x += 1
        return dict_search

    elif mode == "reference":
        cursor.execute(f"SELECT * FROM reference WHERE search_name LIKE '%{data}%'")
        return cursor.fetchall()
    
    elif mode == "criminals":
        cursor.execute(f"SELECT criminals.id, criminals.name, criminals.birthday FROM criminals WHERE criminals.name LIKE '%{data}%'")
        result_searching = cursor.fetchall()
        if len(result_searching) > 1:
            message_send = ""
            for item in result_searching:
                message_send += f"<b>ID:</b> {item[0]}\n<b>ФИО:</b> {item[1]}\n<b>Дата рождения:</b> {item[2]}\n\n"
            message_send += "<b>Найдены несколько лиц, введите необходимый ID:</b>"
            return result_searching, message_send
        else:
            cursor.execute(f"""
            SELECT incidents.*, criminal_case.*, criminals.*
            FROM incidents 
            FULL JOIN criminal_case ON criminal_case.kusp=incidents.kusp 
            FULL JOIN  criminals ON criminals.id=incidents.id_crimes
            WHERE criminals.name LIKE "%{data}%"
            """)
            return cursor.fetchall(), None

    elif mode == "criminals_id":
        cursor.execute(f"""
            SELECT incidents.*, criminal_case.*, criminals.*
            FROM incidents 
            FULL JOIN criminal_case ON criminal_case.kusp=incidents.kusp 
            FULL JOIN  criminals ON criminals.id=incidents.id_crimes
            WHERE criminals.id={data}
            """)
        result_searching = cursor.fetchall()
        return result_searching

    elif mode == "criminals_all":
        cursor.execute(f"SELECT criminals.id, criminals.name, criminals.birthday FROM criminals")
        result_searching = cursor.fetchall()
        message_send = ""
        for item in result_searching:
            message_send += f"<b>ID:</b> {item[0]}\n<b>ФИО:</b> {item[1]}\n<b>Дата рождения:</b> {item[2]}\n\n"
        message_send += "<b>Выведены все лица, введите необходимый ID:</b>"
        return result_searching, message_send

    elif mode == "criminal_case":
        cursor.execute(f"""
        SELECT incidents.*, criminal_case.num_case, criminal_case.date_case, 
        criminal_case.article, criminals.name, criminals.date_catch, 
        criminals.status_crime, criminals.tg_id
        FROM incidents 
        FULL JOIN criminal_case ON criminal_case.kusp=incidents.kusp 
        FULL JOIN  criminals ON criminals.id=incidents.id_crimes
        WHERE criminal_case.num_case LIKE "%{data}%"
        """)
        return cursor.fetchall()

    result_parcing = cursor.fetchall()

    list_1 = []

    for index, item in enumerate(result_parcing):
        list_2 = []
        for index_row, item_row in enumerate(result_parcing[index]):
            if item_row is None:
                list_2.append("-")
            else:
                list_2.append(item_row)
            
        list_1.append(list_2)

    return list_1

    cursor.close()
    connection.commit()


def search_in_base_revelation(mode):

    connection = sqlite3.connect("support_files/incidents/database_inc/base_inc.db")
    cursor = connection.cursor()

    if mode == "Да":
        cursor.execute(f"""
        SELECT incidents.*,
        criminal_case.num_case, criminal_case.date_case, criminal_case.article, 
        criminals.name, criminals.date_catch, criminals.status_crime, criminals.tg_id
        FROM incidents 
        FULL JOIN criminal_case ON criminal_case.kusp=incidents.kusp 
        FULL JOIN  criminals ON criminals.id=incidents.id_crimes
        WHERE incidents.revelation LIKE 'Да'
        """)
        
    elif mode == "Нет":
        cursor.execute(f"""
        SELECT incidents.*,
        criminal_case.num_case, criminal_case.date_case, criminal_case.article, 
        criminals.name, criminals.date_catch, criminals.status_crime, criminals.tg_id
        FROM incidents 
        FULL JOIN criminal_case ON criminal_case.kusp=incidents.kusp 
        FULL JOIN  criminals ON criminals.id=incidents.id_crimes
        WHERE incidents.revelation LIKE 'Нет'
        """)

    elif mode == "all":
        cursor.execute(f"""
        SELECT incidents.*,
        criminal_case.num_case, criminal_case.date_case, criminal_case.article, 
        criminals.name, criminals.date_catch, criminals.status_crime, criminals.tg_id
        FROM incidents 
        FULL JOIN criminal_case ON criminal_case.kusp=incidents.kusp 
        FULL JOIN  criminals ON criminals.id=incidents.id_crimes
        """)
        
    result_parcing = cursor.fetchall()

    list_1 = []

    for index, item in enumerate(result_parcing):
        list_2 = []
        for index_row, item_row in enumerate(result_parcing[index]):
            if item_row is None:
                list_2.append("-")
            else:
                list_2.append(item_row)
            
        list_1.append(list_2)

    return list_1

    cursor.close()
    connection.commit()


