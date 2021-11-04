import unittest
import sqlite3
import os

import sys
sys.path.append(os.getcwd())
from sqlite.check_database import check_database

"""
This test suite ensures the DB is correctly created.

WARNING: These tests will delete the DB, so back up the DB
if need be!
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
        check_database.check()
        create_database_test.conn = sqlite3.connect(
            os.getenv('APPDATA') + "\\project-time-saver\\database.db")

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
        cur = create_database_test.conn.cursor()
        count = 0
        tables = cur.execute("""SELECT * FROM sqlite_master where type='table';""").fetchall()
        for value in tables:
            if "Employee" in value or "Run" in value or "Responded" in value:
                count += 1
        self.assertEqual(count, 3)

    """
    Ensures that the Run table has all of its columns.
    """
    def test_run_columns(self):
        cur = create_database_test.conn.cursor()
        count = 0
        columns = cur.execute("""PRAGMA table_info(Run);""").fetchall()
        for value in columns:
            if "number" in value or "date" in value or "startTime" in value or "stopTime" in value\
                    or "runTime" in value or "Covered" in value or "Medrun" in value or "shift" in value:
                count += 1
        self.assertEqual(count, 8)
    
    """
    Ensures that the Responded table has all of its columns.
    """
    def test_responded_columns(self):
        cur = create_database_test.conn.cursor()
        count = 0
        columns = cur.execute("""PRAGMA table_info(Responded);""").fetchall()
        for value in columns:
            if "empNumber" in value or "runNumber" in value or "date" in value or "payRate" in value:
                count += 1
        self.assertEqual(count, 4)

    """
    Ensures that the Employee table has all of its columns.
    """
    def test_employee_columns(self):
        cur = create_database_test.conn.cursor()
        count = 0
        columns = cur.execute("""PRAGMA table_info(Employee);""").fetchall()
        for value in columns:
            if "name" in value or "number" in value or "city_number" in value:
                count += 1
        self.assertEqual(count, 3)

    """
    Deletes the DB as a part of the setup method.
    """
    def delete_db():
        if os.path.exists(os.getenv('APPDATA') + "\\project-time-saver\\database.db"):
            os.remove(os.getenv('APPDATA') + "\\project-time-saver\\database.db")

if __name__ == '__main__':
    unittest.main()