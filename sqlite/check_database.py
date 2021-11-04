import os
from .database_creation import creator

class check_database:
    @staticmethod
    def check():
        if not os.path.exists(os.getenv('APPDATA') + "\\project-time-saver"):
            os.makedirs(os.getenv('APPDATA') + "\\project-time-saver")
            creator.create_db(os.getenv('APPDATA') + "\\project-time-saver\\database.db")
        elif not os.path.exists(os.getenv('APPDATA') + "\\project-time-saver\\database.db"):
            creator.create_db(os.getenv('APPDATA') + "\\project-time-saver\\database.db")