import os
from database_creation import creator

class check_database:
    @staticmethod
    def check(path = os.getenv('APPDATA') + "\\project-time-saver", db_name = "\\database.db"):
        if not os.path.exists(path):
            os.makedirs(path)
            creator.create_db(path + db_name)
        elif not os.path.exists(path + db_name):
            creator.create_db(path + db_name)