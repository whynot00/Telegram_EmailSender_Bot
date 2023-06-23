from openpyxl import load_workbook
import json
import sqlite3


list_none = [(1, 'Нет', '21.02.2023', 'Нижний Новгород Львовская 31 32 ', 'Грачев', 'Банк', None, 24234, None, None, None, None, None, None, None), ('Грачев', 'Банк', None, 24234, None, None, None, None, None, None, None)]



base = ["Нет", "14.12.2021", "Дзержинск Львоская 55 13", "Грачев Р.А.", "asdasdasdasdasd", "банк"]
base_1 = ["Грачев Роман", "21.02.1999", "21.02.2022", "Подозреваемый"]

id_crime = 2

connection = sqlite3.connect("support_files/incidents/database_inc/base_inc.db")
cursor = connection.cursor()

# cursor.execute("""DROP TABLE criminal_case""")


# cursor.execute("""
#     CREATE TABLE IF NOT EXISTS criminal_case(
#     id INTEGER PRIMARY KEY,
#     kusp TEXT,
#     num_case TEXT,
#     date_case TEXT,
#     article TEXT);
# """)


# cursor.execute("""
#     CREATE TABLE IF NOT EXISTS criminals(
#     id INTEGER PRIMARY KEY,
#     name TEXT,
#     birthday TEXT,
#     date_catch TEXT,
#     status_crime TEXT,
#     curator_tg_id INTEGER,
#     tg_id INTEGER,
#     FOREIGN KEY(curator_tg_id) REFERENCES curators(id_tg));
#     """)

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
#     kusp INTEGER,
#     FOREIGN KEY(id_crimes) REFERENCES criminals(id),
#     FOREIGN KEY(kusp) REFERENCES criminal_case(kusp)
#     );
#     """)

# cursor.execute("""
#     CREATE TABLE IF NOT EXISTS curators(
#     id INTEGER PRIMARY KEY,
#     id_tg TEXT,
#     username_tg TEXT,
#     oper_drove TEXT);
#     """)

cursor.execute("""
    UPDATE incidents SET id_crimes = 3 WHERE incident_id = 2
""")


# cursor.execute("""
#         CREATE TABLE IF NOT EXISTS coordinates(
#         incident_id INTEGER PRIMARY KEY,
#         latitude INTEGER,
#         longitude INTEGER);
#         """)

def select():
    cursor.execute(f"""
        SELECT incidents.*, criminal_case.*, criminals.*
        FROM incidents 
        FULL JOIN criminal_case ON criminal_case.kusp=incidents.kusp 
        FULL JOIN  criminals ON criminals.id=incidents.id_crimes
        WHERE criminal_case.num_case LIKE "%4021%"
    """)
    return cursor.fetchall()

# cursor.execute("SELECT criminals.name, criminals.birthday FROM criminals WHERE criminals.name LIKE '%Иванов%'")

result_searching = select()

print(result_searching)

# list_1 = []

# for index, item in enumerate(result_searching):
#     list_2 = []
#     for index_row, item_row in enumerate(result_searching[index]):
#         if item_row is None:
#             list_2.append("-")
#         else:
#             list_2.append(item_row)
        
#     list_1.append(list_2)

# id_key = list_1[0][-7]



# dict_sql = {}

# for item in list_1:
#     dict_sql[f"id_{id_key}"] = item

# print(dict_sql)


cursor.close()
connection.commit()