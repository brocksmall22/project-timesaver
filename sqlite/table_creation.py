import sqlite3
from sqlite3 import Error

database = r"file name"


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main():
    sql_create_employee_table = """ CREATE TABLE IF NOT EXISTS Employee (name STRING, number SMALLINT PRIMARY KEY); """

    sql_create_run_table = """CREATE TABLE IF NOT EXISTS Run (number TINYINT PRIMARY KEY, date DATE, 
                                startTime SMALLINT, stopTime SMALLINT, runTime TINYINT); """

    sql_create_report_table = """CREATE TABLE IF NOT EXISTS Responded (empNumber STRING REFERENCES Employee (number), 
                                runNumber TINYINT REFERENCES Run (number), date DATE REFERENCES Run (date), 
                                payRate FLOAT);"""

    conn = create_connection(database)

    # create tables
    if conn is not None:
        create_table(conn, sql_create_employee_table)
        create_table(conn, sql_create_run_table)
        create_table(conn, sql_create_report_table)
        print("Success!")
    else:
        print("Error! cannot create the database connection.")


if __name__ == "__main__":
    main()
