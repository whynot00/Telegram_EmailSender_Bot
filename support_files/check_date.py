from datetime import datetime

def check_date(date):
    try:
        check_date = datetime.strptime(date, '%d.%m.%Y')
        
        return True

    except ValueError:
        return False
