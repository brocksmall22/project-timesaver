import unittest
import sqlite3
import os

import sys
sys.path.append(os.getcwd())
from sqlite.check_database import check_database
from lib.payroll import payroll as p

"""
This test class tests the insertion and update operations function as expected.

WARNING: This is a destructive test class and will delete the DB. Back up the DB
if it has important information!
"""
class payroll_test(unittest.TestCase):
    good_1 = [os.getcwd() + "\\test\\resc\\good_1.xlsx"]
    good_1_altered = [os.getcwd() + "\\test\\resc\\good_1_altered.xlsx"]
    good_2 = [os.getcwd() + "\\test\\resc\\good_2.xlsx"]
    bad_1 = [os.getcwd() + "\\test\\resc\\bad_1.xlsx"]
    bad_2 = [os.getcwd() + "\\test\\resc\\bad_2.xlsx"]
    conn = None

    """
    Sets the stage for the tests. Deletes the DB, creates a new
    one and then connects to it.
    """
    @classmethod
    def setUpClass(cls):
        payroll_test.delete_db()
        check_database.check()
        payroll_test.conn = sqlite3.connect(
            os.getenv('APPDATA') + "\\project-time-saver\\database.db")

    """
    Closes the connection to the DB once the tests are done.
    """
    @classmethod
    def tearDownClass(cls):
        payroll_test.conn.close

    """
    This test tests that a known good file can be submitted.
    """
    def test_1_insert_good_1(self):
        cur = payroll_test.conn.cursor()
        result = p.loadWorkBooks(payroll_test.good_1)
        self.assertTrue(result[0])
        runvals = cur.execute("""SELECT * FROM Run;""").fetchall()
        employeevals = cur.execute("""SELECT * FROM Employee;""").fetchall()
        respondedvals = cur.execute("""SELECT * FROM Responded;""").fetchall()
        self.assertEqual(runvals, [(584, '2021-11-01', 949, 1038, 1, 1, 1, 'C')])
        self.assertEqual(employeevals, [])
        self.assertEqual(respondedvals, [])

    """
    This test tests that a known good file can be submitted.
    """
    def test_2_insert_good_2(self):
        cur = payroll_test.conn.cursor()
        result = p.loadWorkBooks(payroll_test.good_2)
        self.assertTrue(result[0])
        runvals = cur.execute("""SELECT * FROM Run;""").fetchall()
        employeevals = cur.execute("""SELECT * FROM Employee;""").fetchall()
        respondedvals = cur.execute("""SELECT * FROM Responded;""").fetchall()
        self.assertEqual(runvals, [(584, '2021-11-01', 949, 1038, 1, 1, 1, 'C'), 
            (585, '2021-11-01', 1114, 1133, 1, 1, 0, 'C')])
        self.assertEqual(employeevals, [('M. Burkholder', 421, None)])
        self.assertEqual(respondedvals, [(421, 585, '2021-11-01', 16.45)])

    """
    This test tests that a known good file can be submitted, updating a
    previous submission.
    """
    def test_3_reinsert_good_1(self):
        cur = payroll_test.conn.cursor()
        result = p.loadWorkBooks(payroll_test.good_1_altered)
        self.assertTrue(result[0])
        runvals = cur.execute("""SELECT * FROM Run;""").fetchall()
        employeevals = cur.execute("""SELECT * FROM Employee;""").fetchall()
        respondedvals = cur.execute("""SELECT * FROM Responded;""").fetchall()
        self.assertEqual(runvals, [(584, '2021-11-01', 949, 1038, 1, 1, 1, 'A'), 
            (585, '2021-11-01', 1114, 1133, 1, 1, 0, 'C')])
        self.assertEqual(employeevals, [('M. Burkholder', 421, None)])
        self.assertEqual(respondedvals, [(421, 585, '2021-11-01', 16.45)])

    """
    Test to ensure that you can submit more than one file at once.
    """
    def test_4_insert_multiple_good(self):
        cur = payroll_test.conn.cursor()
        result = p.loadWorkBooks([payroll_test.good_1[0], payroll_test.good_2[0]])
        self.assertTrue(result[0])
        runvals = cur.execute("""SELECT * FROM Run;""").fetchall()
        employeevals = cur.execute("""SELECT * FROM Employee;""").fetchall()
        respondedvals = cur.execute("""SELECT * FROM Responded;""").fetchall()
        self.assertEqual(runvals, [(584, '2021-11-01', 949, 1038, 1, 1, 1, 'C'), 
            (585, '2021-11-01', 1114, 1133, 1, 1, 0, 'C')])
        self.assertEqual(employeevals, [('M. Burkholder', 421, None)])
        self.assertEqual(respondedvals, [(421, 585, '2021-11-01', 16.45)])

    """
    This test tests that a known bad file will not submit.
    """
    def test_5_insert_bad_1(self):
        cur = payroll_test.conn.cursor()
        result = p.loadWorkBooks(payroll_test.bad_1)
        self.assertEqual(result, [os.getcwd() + '\\test\\resc\\bad_1.xlsx'])
        runvals = cur.execute("""SELECT * FROM Run;""").fetchall()
        employeevals = cur.execute("""SELECT * FROM Employee;""").fetchall()
        respondedvals = cur.execute("""SELECT * FROM Responded;""").fetchall()
        self.assertEqual(runvals, [(584, '2021-11-01', 949, 1038, 1, 1, 1, 'C'), 
            (585, '2021-11-01', 1114, 1133, 1, 1, 0, 'C')])
        self.assertEqual(employeevals, [('M. Burkholder', 421, None)])
        self.assertEqual(respondedvals, [(421, 585, '2021-11-01', 16.45)])

    """
    This test tests that a known bad file will not submit.
    """
    def test_6_insert_bad_2(self):
        cur = payroll_test.conn.cursor()
        result = p.loadWorkBooks(payroll_test.bad_2)
        self.assertEqual(result, [os.getcwd() + '\\test\\resc\\bad_2.xlsx'])
        runvals = cur.execute("""SELECT * FROM Run;""").fetchall()
        employeevals = cur.execute("""SELECT * FROM Employee;""").fetchall()
        respondedvals = cur.execute("""SELECT * FROM Responded;""").fetchall()
        self.assertEqual(runvals, [(584, '2021-11-01', 949, 1038, 1, 1, 1, 'C'), 
            (585, '2021-11-01', 1114, 1133, 1, 1, 0, 'C')])
        self.assertEqual(employeevals, [('M. Burkholder', 421, None)])
        self.assertEqual(respondedvals, [(421, 585, '2021-11-01', 16.45)])

    """
    Test to ensure that you can submit multiple files, mixed with bad ones.
    """
    def test_7_insert_mix(self):
        cur = payroll_test.conn.cursor()
        result = p.loadWorkBooks([payroll_test.good_1_altered[0], payroll_test.bad_2[0]])
        self.assertEqual(result, [os.getcwd() + '\\test\\resc\\bad_2.xlsx'])
        runvals = cur.execute("""SELECT * FROM Run;""").fetchall()
        employeevals = cur.execute("""SELECT * FROM Employee;""").fetchall()
        respondedvals = cur.execute("""SELECT * FROM Responded;""").fetchall()
        self.assertEqual(runvals, [(584, '2021-11-01', 949, 1038, 1, 1, 1, 'A'), 
            (585, '2021-11-01', 1114, 1133, 1, 1, 0, 'C')])
        self.assertEqual(employeevals, [('M. Burkholder', 421, None)])
        self.assertEqual(respondedvals, [(421, 585, '2021-11-01', 16.45)])

    """
    Deletes the DB as a part of the setup method.
    """
    def delete_db():
        if os.path.exists(os.getenv('APPDATA') + "\\project-time-saver\\database.db"):
            os.remove(os.getenv('APPDATA') + "\\project-time-saver\\database.db")

if __name__ == '__main__':
    unittest.main()