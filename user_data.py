import hashlib
from tkinter import *

# Class User_data
class User_data:
    def __init__(self):
        pass

    def check_phone(self, testS=str, validSymbols=str()):
        flag = True
        if len(testS) < 9 or len(testS) > 9:
            return False
        for val in testS:
            if not (val in validSymbols):
                flag = False
                break
        if flag == True:
            return True
        else:
            return False

    def clear(self, entries=[]):
        if type(entries[0] == Entry):
            for data in entries:
                data.delete(0, END)
        else:
            print("Error type")

    def check_email(self, testS=str, validSymbols=str()):
        flag = False
        for val in testS:
            if val in validSymbols:
                flag = True
                break
        if flag == True:
            return True
        else:
            return False

    def is_number(self, str):
        try:
            float(str)
            return True
        except ValueError:
            return False

    def is_int(self, str):
        try:
            int(str)
            return True
        except ValueError:
            return False

    def md5sum(self, value):
        return hashlib.md5(value.encode()).hexdigest()
