from openpyxl import load_workbook
import json
import sqlite3


dict_table = {}

# wb = load_workbook("table.xlsx")

# ws = wb.active

# for index, row in enumerate(ws.values):
#     dict_table[f"id_{index}"] = {
#         "name": str(row[0]).strip(),
#         "uri_name": str(row[1]).strip(),
#         "fio": str(row[2]).strip(),
#         "powers": str(row[3]).strip(),
#         "phone": str(row[4]).strip(),
#         "email": str(row[5]).strip(),
#         "cities": str(row[6]).strip()
#     }

# for key in dict_table.keys():
#     item = dict_table[key]["phone"].replace(" ","").replace(")","").replace("(","").replace("+","").replace("-","")
#     if item[0] == "8":
#         dict_table[key]["phone"] = item.replace("8", "7", 1)
#     else:
#         dict_table[key]["phone"] = item
#     print(dict_table[key]["phone"])


# with open("text.json", "w+") as file:
#     json.dump(dict_table, file, ensure_ascii=False)

connection = sqlite3.connect("support_files/incidents/database_inc/base_inc.db")
cursor = connection.cursor()

with open("text.json", "r") as file:
    jsonfile = json.load(file)

cursor.execute("""
    CREATE TABLE IF NOT EXISTS reference(
        id_ref INTEGER PRIMARY KEY,
        name TEXT,
        uri_name TEXT,
        fio TEXT,
        powers TEXT,
        phone TEXT,
        email TEXT,
        cities TEXT);
    """)

for key in jsonfile.keys():
    array_keys = [jsonfile[key]["name"], jsonfile[key]["uri_name"],jsonfile[key]["fio"],jsonfile[key]["powers"],jsonfile[key]["phone"],jsonfile[key]["email"],jsonfile[key]["cities"]]
    print(array_keys)
    cursor.execute("""
        INSERT INTO reference(
            name, uri_name,
            fio, powers,
            phone, email,
            cities) VALUES (?, ?, ?, ?, ?, ?, ?);""", array_keys)

cursor.close()
connection.commit()