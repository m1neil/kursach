from locale import strcoll
import sqlite3


class Card:
    def __init__(self, database=str, card_query=str):
        self.card_database = sqlite3.connect(database)
        self.card_cursor = self.card_database.cursor()
        self.card_database.execute(card_query)
        self.card_database.commit()
        self.card_cursor.close()
        self.card_database.close()

    def set_card_database(self, link_database):
        self.card_database = link_database

    def set_card_cursor(self, cursor):
        self.card_cursor = cursor

    def get_card_database(self):
        return self.card_database

    def get_card_cursor(self):
        return self.card_cursor

    def close_card_database(self):
        self.card_database.close()

    def close_card_cursor(self):
        self.card_cursor.close()
