import re
from tkinter.messagebox import showerror


def check_int(name, value):
    if not value.isdigit() or int(value) <= 0 or re.match("^0+\d+$", value) is not None:
        showerror('Error', 'Invalid ' + name)
        return False
    else:
        return True


def check_str(name, value):
    if not isinstance(value, str) or value == '':
        showerror('Error', 'Invalid ' + name)
        return False
    else:
        return True


def check_date(name, value):
    if check_str(name, value) is True:
        if re.match("^\d\d/\d\d/\d\d\d\d$", value) is None:
            showerror('Error', 'Invalid ' + name)
            return False
        else:
            return True
    else:
        return False


def check_time(name, value):
    if not name and not value:
        return False
    else:
        return True


def check_enumerate(name, value, enumarate):
    if check_str(name, value) is True:
        if value not in enumarate:
            showerror('Error', 'Invalid ' + name)
            return False
        else:
            return True
    else:
        return False


def check_score(name, first_score, second_score):
    if float(first_score) + float(second_score) != 1.0:
        showerror('Error', 'Invalid ' + name)
        return False
    else:
        return True
