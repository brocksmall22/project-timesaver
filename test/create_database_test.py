import unittest
import sqlite3
import os

import sys
from unittest.case import expectedFailure
sys.path.append(os.getcwd())
from sqlite.check_database import check_database

"""
This test suite ensures the DB is correctly created.
"""
class create_database_test(unittest.TestCase):
    conn = None

    """
    Sets the stage for the tests. Deletes the DB, creates a new
    one and then connects to it.
    """
    @classmethod
    def setUpClass(cls):
        create_database_test.delete_db()
        check_database.check(db_name = "\\database_test.db")
        create_database_test.conn = sqlite3.connect(
            os.getenv('APPDATA') + "\\project-time-saver\\database_test.db")

    """
    Closes the connection to the DB once the tests are done.
    """
    @classmethod
    def tearDownClass(cls):
        create_database_test.conn.close

    """
    Ensures that the database has all of the tables.
    """
    def test_database_has_all_tables(self):
        expected_tables = ["Employee", "Responded", "Run"]
        real_tables = []
        cur = create_database_test.conn.cursor()
        tables = cur.execute("""SELECT name FROM sqlite_schema where type='table';""").fetchall()
        for table in tables:
            real_tables.append(table[0])
        self.assertTrue(all(expected in real_tables for expected in expected_tables))
        self.assertTrue(all(real in expected_tables for real in real_tables))

    """
    Ensures that the Run table has all of its columns.
    """
    def test_run_columns(self):
        expected_columns = ['number', 'date', 'startTime', 'stopTime', 'runTime', 'fsc', 'Covered', 'Medrun', 'shift', 'full_coverage', 'paidRun', 'timeStamp']
        real_columns = []
        cur = create_database_test.conn.cursor()
        columns = cur.execute("""PRAGMA table_info(Run);""").fetchall()
        for column in columns:
            real_columns.append(column[1])
        self.assertTrue(all(expected in real_columns for expected in expected_columns))
        self.assertTrue(all(real in expected_columns for real in real_columns))
    
    """
    Ensures that the Responded table has all of its columns.
    """
    def test_responded_columns(self):
        expected_columns = ['empNumber', 'runNumber', 'date', 'payRate', 'type_of_response', 'full_time', 'subhours']
        real_columns = []
        cur = create_database_test.conn.cursor()
        columns = cur.execute("""PRAGMA table_info(Responded);""").fetchall()
        for column in columns:
            real_columns.append(column[1])
        self.assertTrue(all(expected in real_columns for expected in expected_columns))
        self.assertTrue(all(real in expected_columns for real in real_columns))

    """
    Ensures that the Employee table has all of its columns.
    """
    def test_employee_columns(self):
        expected_columns = ["name", "number", "city_number"]
        real_columns = []
        cur = create_database_test.conn.cursor()
        columns = cur.execute("""PRAGMA table_info(Employee);""").fetchall()
        for column in columns:
            real_columns.append(column[1])
        self.assertTrue(all(expected in real_columns for expected in expected_columns))
        self.assertTrue(all(real in expected_columns for real in real_columns))

    """
    Deletes the DB as a part of the setup method.
    """
    def delete_db():
        if os.path.exists(os.getenv('APPDATA') + "\\project-time-saver\\database_test.db"):
            os.remove(os.getenv('APPDATA') + "\\project-time-saver\\database_test.db")

if __name__ == '__main__':
    unittest.main()