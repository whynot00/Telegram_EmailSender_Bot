from jinja2 import Environment, FileSystemLoader
import os

string = [
    (1, 'Да', '23.10.2022', 'Нижний Новгород Львоская 55 13 ', 'Грачев Р.А.', 'asdasdasdasdasd'), 
    (2, 'Да', '23.10.2022', 'Нижний Новгород Львоская 55 13 ', 'Грачев Р.А.', 'asdasdasdasdasd'), 
    (15, 'Да', '21.10.2022', 'Ниижний Новгород ', 'грачев', 'ыдвопатыдвоатывоат')
]

def form_story_in_html(db_list, search_title, userid, mode):

    if mode == "default":
        environment = Environment(loader=FileSystemLoader("support_files/incidents/html_temp/"))
        template = environment.get_template("form_request_template.html")

        content = template.render(database=db_list, amount=len(db_list), search_name=search_title)
        
        with open(f"user_files/{search_title}_{userid}.html", mode="w", encoding="utf-8") as message:
            message.write(content)


    elif mode == "locate":
        environment = Environment(loader=FileSystemLoader("support_files/incidents/html_temp/"))
        template = environment.get_template("form_request_locate_template.html")

        content = template.render(database=db_list, amount=len(db_list), search_name=search_title)

        with open(f"user_files/{search_title}_{userid}.html", mode="w", encoding="utf-8") as message:
            message.write(content)

    
    
def check_folder(id_incident):
    try:    
        for file in os.listdir(f"user_files/photos/{id_incident}"):
            filename = os.path.basename(file)
        if filename:
            return True
    
    except FileNotFoundError:
        return False

