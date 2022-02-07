import os
import unittest
import shutil

import sys
sys.path.append(os.getcwd())
from sqlite.check_database import check_database

"""
Tests the creation of the database in various conditions.

WARNING: The operations in these tests are destructive. If you have any files stored
in the roaming location for this application, back them up before running these
tests!
"""
class check_database_test(unittest.TestCase):

    """
    Deletes the directory, then checks to see that the server can recreate it
    and re-populate it.
    """
    def test_create_database_when_missing_db(self):
        check_database_test.delete_dir()
        check_database.check()
        self.assertTrue(check_database_test.file_exists())

    """
    Deletes the database file and attempts to recreate it.
    """
    def test_create_database_when_missing_db_in_existing_dir(self):
        check_database_test.delete_file()
        check_database.check()
        self.assertTrue(check_database_test.file_exists())

    """
    Checks to ensure the DB is not overwritten if it is already present
    during the check.
    """
    def test_no_changes_if_db_present(self):
        before = os.path.getmtime(os.getenv('APPDATA') + "\\project-time-saver\\database.db")
        check_database.check()
        after = os.path.getmtime(os.getenv('APPDATA') + "\\project-time-saver\\database.db")
        self.assertEqual(before, after)        

    """
    Checks to ensure a DB can be created with another name.
    """
    def test_create_db_by_other_name(self):
        check_database.check(db_name = "\\database_test.db")
        self.assertTrue(os.path.exists(os.getenv("APPDATA") + "\\project-time-saver\\database_test.db"))
        os.unlink(os.getenv("APPDATA") + "\\project-time-saver\\database_test.db") 

    """
    Deletes the DB file.
    """
    def delete_file():
        if os.path.exists(os.getenv('APPDATA') + "\\project-time-saver\\database.db"):
            os.remove(os.getenv('APPDATA') + "\\project-time-saver\\database.db")

    """
    Deletes the folder and everything in it.
    """
    def delete_dir():
        if os.path.exists(os.getenv('APPDATA') + "\\project-time-saver\\database.db") or \
                os.path.exists(os.getenv('APPDATA') + "\\project-time-saver"):
            shutil.rmtree(os.getenv('APPDATA') + "\\project-time-saver")

    """
    Checks to see if the DB file exists.

    returns..
        case 1: True if it does exist
        case 2: False if it does not exist
    """
    def file_exists():
        return True  if os.path.exists(os.getenv('APPDATA') + "\\project-time-saver\\database.db") else False

if __name__ == '__main__':
    unittest.main()