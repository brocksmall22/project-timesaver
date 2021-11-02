import sqlite3
from sqlite3 import Error

class creator:
    @staticmethod
    def create_db(db_file):
        sql_create_employee_table = """ CREATE TABLE IF NOT EXISTS Employee (name STRING, number SMALLINT PRIMARY KEY, city_number SMALLINT NULL); """

        sql_create_run_table = """CREATE TABLE IF NOT EXISTS Run (number TINYINT, date DATE, 
                                    startTime SMALLINT, stopTime SMALLINT, runTime TINYINT, PRIMARY KEY(number, date)); """

        sql_create_report_table = """CREATE TABLE IF NOT EXISTS Responded (empNumber STRING REFERENCES Employee (number), 
                                    runNumber TINYINT REFERENCES Run (number), date DATE REFERENCES Run (date), 
                                    payRate FLOAT, PRIMARY KEY(date, empNumber, runNumber));"""

        conn = creator.create_connection(db_file)

        # create tables
        if conn is not None:    
            creator.create_table(conn, sql_create_employee_table)
            creator.create_table(conn, sql_create_run_table)
            creator.create_table(conn, sql_create_report_table)
            print("Success!")
        else:
            print("Error! cannot create the database connection.")
    
    @staticmethod
    def create_connection(db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            print(e)
        return conn

    @staticmethod
    def create_table(conn, create_table_sql):
        try:
            c = conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)
