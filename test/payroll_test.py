import unittest
import sqlite3
import os

import sys
sys.path.append(os.getcwd())
from sqlite.check_database import check_database
from lib.payroll import payroll as p
from lib.logger import Logger

"""
This test class tests the insertion and update operations function as expected.
"""
class payroll_test(unittest.TestCase):
    good_1 = [os.getcwd() + "\\test\\resc\\good_tests\\584.xlsx"]
    good_1_altered = [os.getcwd() + "\\test\\resc\\altered_tests\\584.xlsx"]
    good_2 = [os.getcwd() + "\\test\\resc\\good_tests\\585.xlsx"]
    bad_1 = [os.getcwd() + "\\test\\resc\\bad_tests\\623.xlsx"]
    bad_2 = [os.getcwd() + "\\test\\resc\\bad_tests\\654.xlsx"]
    conn = None
    test_json = os.getcwd() + "\\test\\resc\\test.json"
    db = os.getenv('APPDATA') + "\\project-time-saver\\database_test.db"


    """
    Sets the stage for the tests. Deletes the DB, creates a new
    one and then connects to it.
    """
    @classmethod
    def setUpClass(cls):
        payroll_test.delete_db()
        check_database.check(db_name = "\\database_test.db")
        payroll_test.conn = sqlite3.connect(
            os.getenv('APPDATA') + "\\project-time-saver\\database_test.db")

    """
    Closes the connection to the DB once the tests are done.
    """
    @classmethod
    def tearDownClass(cls):
        payroll_test.conn.close()
        payroll_test.delete_db()

    """
    This test tests that a known good file can be submitted.
    """
    def test_1_insert_good_1(self):
        cur = payroll_test.conn.cursor()
        p.loadWorkBooks(payroll_test.good_1, self.test_json, database = self.db)
        runvals = cur.execute("""SELECT * FROM Run;""").fetchall()
        employeevals = cur.execute("""SELECT * FROM Employee;""").fetchall()
        respondedvals = cur.execute("""SELECT * FROM Responded;""").fetchall()
        self.assertEqual(runvals, [(584, '2021-11-01', 949, 1038, 1, 0, 1, 1, 'C', 0, 0, 1647303547.6173499, None, None, '621', 1002, 1005, None, 1038, 1, 0, 'ENGINE 3', 'harrison,city', '', '', 'Med')])
        self.assertEqual(employeevals, [('M. Burkholder', 421, None), ('K. Gerber', 621, None), ('B. Ehrman - F13', 509, None)])
        self.assertEqual(respondedvals, [(421, 584, '2021-11-01', 16.45, 'PNP', 0, 0.0), (621, 584, '2021-11-01', 14.5, 'OD', 0, 0.0), (509, 584, '2021-11-01', 0.0, 'OD', 1, 0.0)])

    """
    This test tests that a known good file can be submitted.
    """
    def test_2_insert_good_2(self):
        cur = payroll_test.conn.cursor()
        p.loadWorkBooks(payroll_test.good_2, self.test_json, database = self.db)
        runvals = cur.execute("""SELECT * FROM Run;""").fetchall()
        employeevals = cur.execute("""SELECT * FROM Employee;""").fetchall()
        respondedvals = cur.execute("""SELECT * FROM Responded;""").fetchall()
        self.assertEqual(runvals, [(584, '2021-11-01', 949, 1038, 1, 0, 1, 1, 'C', 0, 0, 1647303547.6173499, None, None, '621', 1002, 1005, None, 1038, 1, 0, 'ENGINE 3', 'harrison,city', '', '', 'Med'), (585, '2021-11-01', 1114, 1133, 1, 0, 1, 0, 'C', 0, 1, 1647303547.6193557, '1', '13', '1', 1117, 1121, None, 1133, 1, 0, 'ENGINE 1', 'lancaster,city', '', '', 'Fire,Invest')])
        self.assertEqual(employeevals, [('M. Burkholder', 421, None), ('K. Gerber', 621, None), ('B. Ehrman - F13', 509, None), ('D. Craig F1', 306, None), ('C. Wolf F2', 394, None), ('J. Platt - F15', 615, None), ('D.Zoda - F16', 215, None), ('T. Elzey - F17', 120, None), ('A. Hannie - F18', 520, None)])
        self.assertEqual(respondedvals, [(421, 584, '2021-11-01', 16.45, 'PNP', 0, 0.0), (621, 584, '2021-11-01', 14.5, 'OD', 0, 0.0), (509, 584, '2021-11-01', 0.0, 'OD', 1, 0.0), (421, 585, '2021-11-01', 16.45, 'P', 0, 0.0), (621, 585, '2021-11-01', 14.5, 'OD', 0, 0.0), (306, 585, '2021-11-01', 0.0, 'OD', 1, 0.0), (394, 585, '2021-11-01', 0.0, 'OD', 1, 0.0), (509, 585, '2021-11-01', 0.0, 'OD', 1, 0.0), (615, 585, '2021-11-01', 0.0, 'P', 1, 0.0), (215, 585, '2021-11-01', 0.0, 'OD', 1, 0.0), (120, 585, '2021-11-01', 0.0, 'P', 1, 0.0), (520, 585, '2021-11-01', 0.0, 'OD', 1, 0.0)])

    """
    This test tests that a known good file can be submitted, updating a
    previous submission.
    """
    def test_3_reinsert_good_1(self):
        cur = payroll_test.conn.cursor()
        p.loadWorkBooks(payroll_test.good_1_altered, self.test_json, database = self.db)
        runvals = cur.execute("""SELECT * FROM Run;""").fetchall()
        employeevals = cur.execute("""SELECT * FROM Employee;""").fetchall()
        respondedvals = cur.execute("""SELECT * FROM Responded;""").fetchall()
        self.assertEqual(runvals, [(584, '2021-11-01', 949, 1038, 1, 0, 1, 1, 'C', 0, 0, 1647303547.6173499, None, None, '621', 1002, 1005, None, 1038, 1, 0, 'ENGINE 3', 'harrison,city', '', '', 'Med'), (585, '2021-11-01', 1114, 1133, 1, 0, 1, 0, 'C', 0, 1, 1647303547.6193557, '1', '13', '1', 1117, 1121, None, 1133, 1, 0, 'ENGINE 1', 'lancaster,city', '', '', 'Fire,Invest')])
        self.assertEqual(employeevals, [('M. Burkholder', 421, None), ('K. Gerber', 621, None), ('B. Ehrman - F13', 509, None), ('D. Craig F1', 306, None), ('C. Wolf F2', 394, None), ('J. Platt - F15', 615, None), ('D.Zoda - F16', 215, None), ('T. Elzey - F17', 120, None), ('A. Hannie - F18', 520, None)])
        self.assertEqual(respondedvals, [(421, 584, '2021-11-01', 16.45, 'PNP', 0, 0.0), (621, 584, '2021-11-01', 14.5, 'OD', 0, 0.0), (509, 584, '2021-11-01', 0.0, 'OD', 1, 0.0), (421, 585, '2021-11-01', 16.45, 'P', 0, 0.0), (621, 585, '2021-11-01', 14.5, 'OD', 0, 0.0), (306, 585, '2021-11-01', 0.0, 'OD', 1, 0.0), (394, 585, '2021-11-01', 0.0, 'OD', 1, 0.0), (509, 585, '2021-11-01', 0.0, 'OD', 1, 0.0), (615, 585, '2021-11-01', 0.0, 'P', 1, 0.0), (215, 585, '2021-11-01', 0.0, 'OD', 1, 0.0), (120, 585, '2021-11-01', 0.0, 'P', 1, 0.0), (520, 585, '2021-11-01', 0.0, 'OD', 1, 0.0)])

    """
    Test to ensure that you can submit more than one file at once.
    """
    def test_4_insert_multiple_good(self):
        cur = payroll_test.conn.cursor()
        p.loadWorkBooks(payroll_test.good_1 + payroll_test.good_2, self.test_json, database = self.db)
        runvals = cur.execute("""SELECT * FROM Run;""").fetchall()
        employeevals = cur.execute("""SELECT * FROM Employee;""").fetchall()
        respondedvals = cur.execute("""SELECT * FROM Responded;""").fetchall()
        self.assertEqual(runvals, [(584, '2021-11-01', 949, 1038, 1, 0, 1, 1, 'C', 0, 0, 1639672228.955099), (585, '2021-11-01', 1114, 1133, 1, 0, 1, 0, 'C', 0, 1, 1639672228.9591231)])
        self.assertEqual(employeevals, [('M. Burkholder', 421, None), ('K. Gerber', 621, None), ('B. Ehrman - F13', 509, None), ('D. Craig F1', 306, None), ('C. Wolf F2', 394, None), ('J. Platt - F15', 615, None), ('D.Zoda - F16', 215, None), ('T. Elzey - F17', 120, None), ('A. Hannie - F18', 520, None)])
        self.assertEqual(respondedvals, [(421, 584, '2021-11-01', 16.45, 'PNP', 0, 0.0), (621, 584, '2021-11-01', 14.5, 'OD', 0, 0.0), (509, 584, '2021-11-01', 0.0, 'OD', 1, 0.0), (421, 585, '2021-11-01', 16.45, 'P', 0, 0.0), (621, 585, '2021-11-01', 14.5, 'OD', 0, 0.0), (306, 585, '2021-11-01', 0.0, 'OD', 1, 0.0), (394, 585, '2021-11-01', 0.0, 'OD', 1, 0.0), (509, 585, '2021-11-01', 0.0, 'OD', 1, 0.0), (615, 585, '2021-11-01', 0.0, 'P', 1, 0.0), (215, 585, '2021-11-01', 0.0, 'OD', 1, 0.0), (120, 585, '2021-11-01', 0.0, 'P', 1, 0.0), (520, 585, '2021-11-01', 0.0, 'OD', 1, 0.0)])

    # """
    # This test tests that a known bad file will not submit.
    # """
    # def test_5_insert_bad_1(self):
    #     cur = payroll_test.conn.cursor()
    #     self.removeFile()
    #     p.loadWorkBooks(payroll_test.bad_1, self.test_json, database = self.db)
    #     self.assertEqual(Logger.getErrors(self.test_json)[0]["type"], "report format error")
    #     self.assertEqual(Logger.getErrors(self.test_json)[0]["message"].split("\\")[-1], "623.xlsx has error: Date cannot be empty!")
    #     self.assertTrue(Logger.getErrors(self.test_json)[0]["time"] != "")
    #     self.assertEqual(len(Logger.getErrors(self.test_json)), 1)
    #     self.removeFile()
    #     runvals = cur.execute("""SELECT * FROM Run;""").fetchall()
    #     employeevals = cur.execute("""SELECT * FROM Employee;""").fetchall()
    #     respondedvals = cur.execute("""SELECT * FROM Responded;""").fetchall()
    #     self.assertEqual(runvals, [(584, '2021-11-01', 949, 1038, 1, 0, 1, 1, 'C', 0, 0, 1639672228.955099), (585, '2021-11-01', 1114, 1133, 1, 0, 1, 0, 'C', 0, 1, 1639672228.9591231)])
    #     self.assertEqual(employeevals, [('M. Burkholder', 421, None), ('K. Gerber', 621, None), ('B. Ehrman - F13', 509, None), ('D. Craig F1', 306, None), ('C. Wolf F2', 394, None), ('J. Platt - F15', 615, None), ('D.Zoda - F16', 215, None), ('T. Elzey - F17', 120, None), ('A. Hannie - F18', 520, None)])
    #     self.assertEqual(respondedvals, [(421, 584, '2021-11-01', 16.45, 'PNP', 0, 0.0), (621, 584, '2021-11-01', 14.5, 'OD', 0, 0.0), (509, 584, '2021-11-01', 0.0, 'OD', 1, 0.0), (421, 585, '2021-11-01', 16.45, 'P', 0, 0.0), (621, 585, '2021-11-01', 14.5, 'OD', 0, 0.0), (306, 585, '2021-11-01', 0.0, 'OD', 1, 0.0), (394, 585, '2021-11-01', 0.0, 'OD', 1, 0.0), (509, 585, '2021-11-01', 0.0, 'OD', 1, 0.0), (615, 585, '2021-11-01', 0.0, 'P', 1, 0.0), (215, 585, '2021-11-01', 0.0, 'OD', 1, 0.0), (120, 585, '2021-11-01', 0.0, 'P', 1, 0.0), (520, 585, '2021-11-01', 0.0, 'OD', 1, 0.0)])

    # """
    # This test tests that a known bad file will not submit.
    # """
    # def test_6_insert_bad_2(self):
    #     self.removeFile()
    #     cur = payroll_test.conn.cursor()
    #     p.loadWorkBooks(payroll_test.bad_2, self.test_json, database = self.db)
    #     self.assertEqual(Logger.getErrors(self.test_json)[0]["type"], "report format error")
    #     self.assertEqual(Logger.getErrors(self.test_json)[0]["message"].split("\\")[-1], "654.xlsx has error: Employee number cannot be empty!")
    #     self.assertTrue(Logger.getErrors(self.test_json)[0]["time"] != "")
    #     self.assertEqual(len(Logger.getErrors(self.test_json)), 1)
    #     self.removeFile()
    #     runvals = cur.execute("""SELECT * FROM Run;""").fetchall()
    #     employeevals = cur.execute("""SELECT * FROM Employee;""").fetchall()
    #     respondedvals = cur.execute("""SELECT * FROM Responded;""").fetchall()
    #     self.assertEqual(runvals, [(584, '2021-11-01', 949, 1038, 1, 0, 1, 1, 'C', 0, 0, 1639672228.955099), (585, '2021-11-01', 1114, 1133, 1, 0, 1, 0, 'C', 0, 1, 1639672228.9591231)])
    #     self.assertEqual(employeevals, [('M. Burkholder', 421, None), ('K. Gerber', 621, None), ('B. Ehrman - F13', 509, None), ('D. Craig F1', 306, None), ('C. Wolf F2', 394, None), ('J. Platt - F15', 615, None), ('D.Zoda - F16', 215, None), ('T. Elzey - F17', 120, None), ('A. Hannie - F18', 520, None)])
    #     self.assertEqual(respondedvals, [(421, 584, '2021-11-01', 16.45, 'PNP', 0, 0.0), (621, 584, '2021-11-01', 14.5, 'OD', 0, 0.0), (509, 584, '2021-11-01', 0.0, 'OD', 1, 0.0), (421, 585, '2021-11-01', 16.45, 'P', 0, 0.0), (621, 585, '2021-11-01', 14.5, 'OD', 0, 0.0), (306, 585, '2021-11-01', 0.0, 'OD', 1, 0.0), (394, 585, '2021-11-01', 0.0, 'OD', 1, 0.0), (509, 585, '2021-11-01', 0.0, 'OD', 1, 0.0), (615, 585, '2021-11-01', 0.0, 'P', 1, 0.0), (215, 585, '2021-11-01', 0.0, 'OD', 1, 0.0), (120, 585, '2021-11-01', 0.0, 'P', 1, 0.0), (520, 585, '2021-11-01', 0.0, 'OD', 1, 0.0)])

    # """
    # Test to ensure that you can submit multiple files, mixed with bad ones.
    # """
    # def test_7_insert_mix(self):
    #     self.removeFile()
    #     cur = payroll_test.conn.cursor()
    #     p.loadWorkBooks([payroll_test.good_1_altered[0], payroll_test.bad_2[0]], self.test_json, database = self.db)
    #     self.assertEqual(Logger.getErrors(self.test_json)[0]["type"], "report format error")
    #     self.assertEqual(Logger.getErrors(self.test_json)[0]["message"].split("\\")[-1], "654.xlsx has error: Employee number cannot be empty!")
    #     self.assertTrue(Logger.getErrors(self.test_json)[0]["time"] != "")
    #     self.assertEqual(len(Logger.getErrors(self.test_json)), 1)
    #     self.removeFile()
    #     runvals = cur.execute("""SELECT * FROM Run;""").fetchall()
    #     employeevals = cur.execute("""SELECT * FROM Employee;""").fetchall()
    #     respondedvals = cur.execute("""SELECT * FROM Responded;""").fetchall()
    #     self.assertEqual(runvals, [(584, '2021-11-01', 949, 1038, 1, 0, 1, 1, 'C', 0, 0, 1639672228.955099), (585, '2021-11-01', 1114, 1133, 1, 0, 1, 0, 'C', 0, 1, 1639672228.9591231)])
    #     self.assertEqual(employeevals, [('M. Burkholder', 421, None), ('K. Gerber', 621, None), ('B. Ehrman - F13', 509, None), ('D. Craig F1', 306, None), ('C. Wolf F2', 394, None), ('J. Platt - F15', 615, None), ('D.Zoda - F16', 215, None), ('T. Elzey - F17', 120, None), ('A. Hannie - F18', 520, None)])
    #     self.assertEqual(respondedvals, [(421, 584, '2021-11-01', 16.45, 'PNP', 0, 0.0), (621, 584, '2021-11-01', 14.5, 'OD', 0, 0.0), (509, 584, '2021-11-01', 0.0, 'OD', 1, 0.0), (421, 585, '2021-11-01', 16.45, 'P', 0, 0.0), (621, 585, '2021-11-01', 14.5, 'OD', 0, 0.0), (306, 585, '2021-11-01', 0.0, 'OD', 1, 0.0), (394, 585, '2021-11-01', 0.0, 'OD', 1, 0.0), (509, 585, '2021-11-01', 0.0, 'OD', 1, 0.0), (615, 585, '2021-11-01', 0.0, 'P', 1, 0.0), (215, 585, '2021-11-01', 0.0, 'OD', 1, 0.0), (120, 585, '2021-11-01', 0.0, 'P', 1, 0.0), (520, 585, '2021-11-01', 0.0, 'OD', 1, 0.0)])

    """
    Deletes the DB as a part of the setup method.
    """
    def delete_db():
        if os.path.exists(os.getenv('APPDATA') + "\\project-time-saver\\database_test.db"):
            os.remove(os.getenv('APPDATA') + "\\project-time-saver\\database_test.db")

    """
    Removes the test log json.
    """
    def removeFile(self):
        if os.path.isfile(os.getcwd() + "\\test\\resc\\test.json"):
            os.remove(os.getcwd() + "\\test\\resc\\test.json")

if __name__ == '__main__':
    unittest.main()