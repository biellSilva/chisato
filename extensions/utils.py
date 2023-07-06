from discord import Role
from datetime import date, time, datetime


class DatetimeFomartError(Exception):
    '''Called when it can not convert string to datetime object'''
    def __init__(self, date_str: str):
        self.date_str = date_str
        super().__init__(self.date_str)

class NotMentionableRole(Exception):
    '''Called when the role is not mentionable'''
    def __init__(self, role: Role):
        self.role = role
        super().__init__(self.role)

class InvalidHexFormat(Exception):
    '''Called when the string isn\'t hex'''
    def __init__(self, hex: str):
        self.hex = hex
        super().__init__(self.hex)

        

def check_date_format(raw_date: str):

    '''
    takes in a string to convert and returns a datetime object 
    '''

    today = date.today().strftime('%d/%m/%Y')
    hour = time(hour=21, minute=0).strftime('%H:%M')
    _format = '%d/%m/%Y %H:%M'

    if '/' in raw_date and ':' in raw_date:
        datetime_obj = datetime.strptime(raw_date, _format).timetuple()
    
    elif ':' in raw_date:
        datetime_obj = datetime.strptime(f'{today} {raw_date}', _format).timetuple()
    
    elif '/' in raw_date:
        datetime_obj = datetime.strptime(f'{raw_date} {hour}', _format).timetuple()

    else:
        raise DatetimeFomartError(raw_date)
    
    return datetime_obj


