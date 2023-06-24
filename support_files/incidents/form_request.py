from jinja2 import Environment, FileSystemLoader
import os


def form_story_in_html(db_list, search_title, userid, mode):
    environment = Environment(loader=FileSystemLoader("support_files/incidents/html_temp/"))
    if mode == "default":
        template = environment.get_template("form_request_template_criminal.html")
        content = template.render(database=db_list, amount=len(db_list), search_name=search_title)

    elif mode == "locate":
        template = environment.get_template("form_request_locate_template.html")
        content = template.render(database=db_list, amount=len(db_list), search_name=search_title)

    elif mode == "ID":
        template = environment.get_template("form_request_ID_template.html")
        
        incident = db_list["incident"]
        criminals = db_list["criminals"]
        criminal_case = db_list["criminal_case"]

        content = template.render(incident=db_list["incident"], criminals=db_list["criminals"], criminal_case=db_list["criminal_case"], amount=len(db_list), search_name=search_title)

    elif mode == "criminals":
        template = environment.get_template("form_request_template.html")
        content = template.render(database=db_list, search_name=search_title)

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

