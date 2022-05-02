from time import time
import unittest
import sqlite3
import os
import sys

sys.path.append(os.getcwd())
from sqlite.check_database import check_database
from lib.payroll import payroll as p
from lib.logger import Logger


class payroll_test(unittest.TestCase):
    """
    This test class tests the insertion and update operations function as expected.
    """
    good_1 = [os.getcwd() + "\\test\\resc\\good_tests\\584.xlsx"]
    good_1_altered = [os.getcwd() + "\\test\\resc\\altered_tests\\584.xlsx"]
    good_2 = [os.getcwd() + "\\test\\resc\\good_tests\\585.xlsx"]
    bad_1 = [os.getcwd() + "\\test\\resc\\bad_tests\\623.xlsx"]
    bad_2 = [os.getcwd() + "\\test\\resc\\bad_tests\\654.xlsx"]
    conn = None
    test_json = os.getcwd() + "\\test\\resc\\test.json"
    db = os.getenv('APPDATA') + "\\project-time-saver\\database_test.db"
    test_config = os.getcwd() + "\\test\\resc\\generate_report_and_payroll_test_config.json"

    
    @classmethod
    def setUpClass(cls):
        """
        Sets the stage for the tests. Deletes the DB, creates a new
        one and then connects to it.
        """
        payroll_test.delete_db()
        check_database.check(db_name="\\database_test.db")
        payroll_test.conn = sqlite3.connect(
            os.getenv('APPDATA') + "\\project-time-saver\\database_test.db")

    
    @classmethod
    def tearDownClass(cls):
        """
        Closes the connection to the DB once the tests are done.
        """
        payroll_test.conn.close()
        payroll_test.delete_db()

    def getRunData(self, cur):
        """
        Fetches all columns in the run table except timeStamp.
        """
        q1 = """CREATE TEMPORARY TABLE TempTable AS SELECT * FROM Run;"""
        q2 = """ALTER TABLE TempTable DROP COLUMN timeStamp;"""
        q3 = """SELECT * FROM TempTable;"""
        q4 = """DROP TABLE TempTable;"""
        cur.execute(q1)
        cur.execute(q2)
        returnVal = cur.execute(q3).fetchall()
        cur.execute(q4)
        return returnVal

    
    def test_1_insert_good_1(self):
        """
        This test tests that a known good file can be submitted.
        """
        cur = payroll_test.conn.cursor()
        p.loadWorkBooks(payroll_test.good_1, self.test_json, database=self.db, test_config_location = payroll_test.test_config)
        runvals = self.getRunData(cur)
        employeevals = cur.execute("""SELECT * FROM Employee;""").fetchall()
        respondedvals = cur.execute("""SELECT * FROM Responded;""").fetchall()
        timestampVals = cur.execute("""SELECT timeStamp FROM Run;""").fetchall()
        for val in timestampVals:
            self.assertTrue(type(val[0]) == float)
        for val in timestampVals:
            self.assertTrue(val[0] > 0)
        self.assertEqual(
            runvals,
            [(584, '2021-11-01', 949, 1038, 1, 0, 1, 1, 'C', 0, 0, None,
            None, '621', 1002, 1005, None, 1038, 1,
            0, 'Engine 3', 'lancaster,city', '', '', 'Med')])
        self.assertEqual(employeevals, [('M. Burkholder', 421, None),
                                        ('K. Gerber', 621, None),
                                        ('B. Ehrman - F13', 509, None)])
        self.assertEqual(respondedvals,
                         [(421, 584, '2021-11-01', 16.45, 'PNP', 0, 0.0),
                          (621, 584, '2021-11-01', 14.5, 'OD', 0, 0.0),
                          (509, 584, '2021-11-01', 0.0, 'OD', 1, 0.0)])

   
    def test_2_insert_good_2(self):
        """
        This test tests that a known good file can be submitted.
        """
        cur = payroll_test.conn.cursor()
        p.loadWorkBooks(payroll_test.good_2, self.test_json, database=self.db, test_config_location = payroll_test.test_config)
        runvals = self.getRunData(cur)
        employeevals = cur.execute("""SELECT * FROM Employee;""").fetchall()
        respondedvals = cur.execute("""SELECT * FROM Responded;""").fetchall()
        timestampVals = cur.execute("""SELECT timeStamp FROM Run;""").fetchall()
        for val in timestampVals:
            self.assertTrue(type(val[0]) == float)
        for val in timestampVals:
            self.assertTrue(val[0] > 0)
        self.assertEqual(
            runvals,
            [(584, '2021-11-01', 949, 1038, 1, 0, 1, 1, 'C', 0, 0,
              None, None, '621', 1002, 1005, None, 1038, 1,
              0, 'Engine 3', 'lancaster,city', '', '', 'Med'),
             (585, '2021-11-01', 1114, 1133, 1, 0, 1, 0, 'C', 0, 1,
              '1', '13', '1', 1117, 1121, None, 1133, 1, 0,
              'Engine 1', 'harrison,city', '', '', 'Fire,Invest')])
        self.assertEqual(employeevals, [('M. Burkholder', 421, None),
                                        ('K. Gerber', 621, None),
                                        ('B. Ehrman - F13', 509, None),
                                        ('D. Craig F1', 306, None),
                                        ('C. Wolf F2', 394, None),
                                        ('J. Platt - F15', 615, None),
                                        ('D.Zoda - F16', 215, None),
                                        ('T. Elzey - F17', 120, None),
                                        ('A. Hannie - F18', 520, None)])
        self.assertEqual(respondedvals,
                         [(421, 584, '2021-11-01', 16.45, 'PNP', 0, 0.0),
                          (621, 584, '2021-11-01', 14.5, 'OD', 0, 0.0),
                          (509, 584, '2021-11-01', 0.0, 'OD', 1, 0.0),
                          (421, 585, '2021-11-01', 16.45, 'P', 0, 0.0),
                          (621, 585, '2021-11-01', 14.5, 'OD', 0, 0.0),
                          (306, 585, '2021-11-01', 0.0, 'OD', 1, 0.0),
                          (394, 585, '2021-11-01', 0.0, 'OD', 1, 0.0),
                          (509, 585, '2021-11-01', 0.0, 'OD', 1, 0.0),
                          (615, 585, '2021-11-01', 0.0, 'P', 1, 0.0),
                          (215, 585, '2021-11-01', 0.0, 'OD', 1, 0.0),
                          (120, 585, '2021-11-01', 0.0, 'P', 1, 0.0),
                          (520, 585, '2021-11-01', 0.0, 'OD', 1, 0.0)])

    
    def test_3_reinsert_good_1(self):
        """
        This test tests that a known good file can be submitted, updating a
        previous submission.
        """
        cur = payroll_test.conn.cursor()
        p.loadWorkBooks(payroll_test.good_1_altered,
                        self.test_json,
                        database=self.db, test_config_location = payroll_test.test_config)
        runvals = self.getRunData(cur)
        employeevals = cur.execute("""SELECT * FROM Employee;""").fetchall()
        respondedvals = cur.execute("""SELECT * FROM Responded;""").fetchall()
        timestampVals = cur.execute("""SELECT timeStamp FROM Run;""").fetchall()
        for val in timestampVals:
            self.assertTrue(type(val[0]) == float)
        for val in timestampVals:
            self.assertTrue(val[0] > 0)
        self.assertEqual(
            runvals,
            [(584, '2021-11-01', 949, 1038, 1, 0, 1, 1, 'C', 0, 0,
              None, None, '621', 1002, 1005, None, 1038, 1,
              0, 'Engine 3', 'lancaster,city', '', '', 'Med'),
             (585, '2021-11-01', 1114, 1133, 1, 0, 1, 0, 'C', 0, 1,
              '1', '13', '1', 1117, 1121, None, 1133, 1, 0,
              'Engine 1', 'harrison,city', '', '', 'Fire,Invest')])
        self.assertEqual(employeevals, [('M. Burkholder', 421, None),
                                        ('K. Gerber', 621, None),
                                        ('B. Ehrman - F13', 509, None),
                                        ('D. Craig F1', 306, None),
                                        ('C. Wolf F2', 394, None),
                                        ('J. Platt - F15', 615, None),
                                        ('D.Zoda - F16', 215, None),
                                        ('T. Elzey - F17', 120, None),
                                        ('A. Hannie - F18', 520, None)])
        self.assertEqual(respondedvals,
                         [(421, 584, '2021-11-01', 16.45, 'PNP', 0, 0.0),
                          (621, 584, '2021-11-01', 14.5, 'OD', 0, 0.0),
                          (509, 584, '2021-11-01', 0.0, 'OD', 1, 0.0),
                          (421, 585, '2021-11-01', 16.45, 'P', 0, 0.0),
                          (621, 585, '2021-11-01', 14.5, 'OD', 0, 0.0),
                          (306, 585, '2021-11-01', 0.0, 'OD', 1, 0.0),
                          (394, 585, '2021-11-01', 0.0, 'OD', 1, 0.0),
                          (509, 585, '2021-11-01', 0.0, 'OD', 1, 0.0),
                          (615, 585, '2021-11-01', 0.0, 'P', 1, 0.0),
                          (215, 585, '2021-11-01', 0.0, 'OD', 1, 0.0),
                          (120, 585, '2021-11-01', 0.0, 'P', 1, 0.0),
                          (520, 585, '2021-11-01', 0.0, 'OD', 1, 0.0)])

    
    def test_4_insert_multiple_good(self):
        """
        Test to ensure that you can submit more than one file at once.
        """
        cur = payroll_test.conn.cursor()
        p.loadWorkBooks(payroll_test.good_1 + payroll_test.good_2,
                        self.test_json,
                        database=self.db, test_config_location = payroll_test.test_config)
        runvals = self.getRunData(cur)
        employeevals = cur.execute("""SELECT * FROM Employee;""").fetchall()
        respondedvals = cur.execute("""SELECT * FROM Responded;""").fetchall()
        timestampVals = cur.execute("""SELECT timeStamp FROM Run;""").fetchall()
        for val in timestampVals:
            self.assertTrue(type(val[0]) == float)
        for val in timestampVals:
            self.assertTrue(val[0] > 0)
        self.assertEqual(
            runvals,
            [(584, '2021-11-01', 949, 1038, 1, 0, 1, 1, 'C', 0, 0,
              None, None, '621', 1002, 1005, None, 1038, 1,
              0, 'Engine 3', 'lancaster,city', '', '', 'Med'),
             (585, '2021-11-01', 1114, 1133, 1, 0, 1, 0, 'C', 0, 1,
              '1', '13', '1', 1117, 1121, None, 1133, 1, 0,
              'Engine 1', 'harrison,city', '', '', 'Fire,Invest')])
        self.assertEqual(employeevals, [('M. Burkholder', 421, None),
                                        ('K. Gerber', 621, None),
                                        ('B. Ehrman - F13', 509, None),
                                        ('D. Craig F1', 306, None),
                                        ('C. Wolf F2', 394, None),
                                        ('J. Platt - F15', 615, None),
                                        ('D.Zoda - F16', 215, None),
                                        ('T. Elzey - F17', 120, None),
                                        ('A. Hannie - F18', 520, None)])
        self.assertEqual(respondedvals,
                         [(421, 584, '2021-11-01', 16.45, 'PNP', 0, 0.0),
                          (621, 584, '2021-11-01', 14.5, 'OD', 0, 0.0),
                          (509, 584, '2021-11-01', 0.0, 'OD', 1, 0.0),
                          (421, 585, '2021-11-01', 16.45, 'P', 0, 0.0),
                          (621, 585, '2021-11-01', 14.5, 'OD', 0, 0.0),
                          (306, 585, '2021-11-01', 0.0, 'OD', 1, 0.0),
                          (394, 585, '2021-11-01', 0.0, 'OD', 1, 0.0),
                          (509, 585, '2021-11-01', 0.0, 'OD', 1, 0.0),
                          (615, 585, '2021-11-01', 0.0, 'P', 1, 0.0),
                          (215, 585, '2021-11-01', 0.0, 'OD', 1, 0.0),
                          (120, 585, '2021-11-01', 0.0, 'P', 1, 0.0),
                          (520, 585, '2021-11-01', 0.0, 'OD', 1, 0.0)])

    
    def test_5_insert_bad_2(self):
        """
        This test tests that a known bad file will not submit.
        """
        self.removeFile()
        cur = payroll_test.conn.cursor()
        p.loadWorkBooks(payroll_test.bad_2, self.test_json, database=self.db, test_config_location = payroll_test.test_config)
        self.assertEqual(
            Logger.getErrors(self.test_json)[0]["type"], "Report format error")
        self.assertEqual(
            Logger.getErrors(self.test_json)[0]["message"].split("\\")[-1],
            "654.xlsx has error: Employee number cannot be empty!")
        self.assertTrue(Logger.getErrors(self.test_json)[0]["time"] != "")
        self.assertEqual(len(Logger.getErrors(self.test_json)), 1)
        self.removeFile()
        runvals = self.getRunData(cur)
        employeevals = cur.execute("""SELECT * FROM Employee;""").fetchall()
        respondedvals = cur.execute("""SELECT * FROM Responded;""").fetchall()
        timestampVals = cur.execute("""SELECT timeStamp FROM Run;""").fetchall()
        for val in timestampVals:
            self.assertTrue(type(val[0]) == float)
        for val in timestampVals:
            self.assertTrue(val[0] > 0)
        self.assertEqual(
            runvals,
            [(584, '2021-11-01', 949, 1038, 1, 0, 1, 1, 'C', 0, 0,
              None, None, '621', 1002, 1005, None, 1038, 1,
              0, 'Engine 3', 'lancaster,city', '', '', 'Med'),
             (585, '2021-11-01', 1114, 1133, 1, 0, 1, 0, 'C', 0, 1,
              '1', '13', '1', 1117, 1121, None, 1133, 1, 0,
              'Engine 1', 'harrison,city', '', '', 'Fire,Invest')])
        self.assertEqual(employeevals, [('M. Burkholder', 421, None),
                                        ('K. Gerber', 621, None),
                                        ('B. Ehrman - F13', 509, None),
                                        ('D. Craig F1', 306, None),
                                        ('C. Wolf F2', 394, None),
                                        ('J. Platt - F15', 615, None),
                                        ('D.Zoda - F16', 215, None),
                                        ('T. Elzey - F17', 120, None),
                                        ('A. Hannie - F18', 520, None)])
        self.assertEqual(respondedvals,
                         [(421, 584, '2021-11-01', 16.45, 'PNP', 0, 0.0),
                          (621, 584, '2021-11-01', 14.5, 'OD', 0, 0.0),
                          (509, 584, '2021-11-01', 0.0, 'OD', 1, 0.0),
                          (421, 585, '2021-11-01', 16.45, 'P', 0, 0.0),
                          (621, 585, '2021-11-01', 14.5, 'OD', 0, 0.0),
                          (306, 585, '2021-11-01', 0.0, 'OD', 1, 0.0),
                          (394, 585, '2021-11-01', 0.0, 'OD', 1, 0.0),
                          (509, 585, '2021-11-01', 0.0, 'OD', 1, 0.0),
                          (615, 585, '2021-11-01', 0.0, 'P', 1, 0.0),
                          (215, 585, '2021-11-01', 0.0, 'OD', 1, 0.0),
                          (120, 585, '2021-11-01', 0.0, 'P', 1, 0.0),
                          (520, 585, '2021-11-01', 0.0, 'OD', 1, 0.0)])


    def test_6_insert_mix(self):
        """
        Test to ensure that you can submit multiple files, mixed with bad ones.
        """
        self.removeFile()
        cur = payroll_test.conn.cursor()
        p.loadWorkBooks([payroll_test.good_1_altered[0], payroll_test.bad_2[0]], self.test_json, database = self.db, test_config_location = payroll_test.test_config)
        self.assertEqual(Logger.getErrors(self.test_json)[0]["type"], "Report format error")
        self.assertEqual(Logger.getErrors(self.test_json)[0]["message"].split("\\")[-1], "654.xlsx has error: Employee number cannot be empty!")
        self.assertTrue(Logger.getErrors(self.test_json)[0]["time"] != "")
        self.assertEqual(len(Logger.getErrors(self.test_json)), 1)
        self.removeFile()
        runvals = self.getRunData(cur)
        employeevals = cur.execute("""SELECT * FROM Employee;""").fetchall()
        respondedvals = cur.execute("""SELECT * FROM Responded;""").fetchall()
        timestampVals = cur.execute("""SELECT timeStamp FROM Run;""").fetchall()
        for val in timestampVals:
            self.assertTrue(type(val[0]) == float)
        for val in timestampVals:
            self.assertTrue(val[0] > 0)
        self.assertEqual(
            runvals,
            [(584, '2021-11-01', 949, 1038, 1, 0, 1, 1, 'C', 0, 0,
              None, None, '621', 1002, 1005, None, 1038, 1,
              0, 'Engine 3', 'lancaster,city', '', '', 'Med'),
             (585, '2021-11-01', 1114, 1133, 1, 0, 1, 0, 'C', 0, 1,
              '1', '13', '1', 1117, 1121, None, 1133, 1, 0,
              'Engine 1', 'harrison,city', '', '', 'Fire,Invest')])
        self.assertEqual(employeevals, [('M. Burkholder', 421, None),
                                        ('K. Gerber', 621, None),
                                        ('B. Ehrman - F13', 509, None),
                                        ('D. Craig F1', 306, None),
                                        ('C. Wolf F2', 394, None),
                                        ('J. Platt - F15', 615, None),
                                        ('D.Zoda - F16', 215, None),
                                        ('T. Elzey - F17', 120, None),
                                        ('A. Hannie - F18', 520, None)])
        self.assertEqual(respondedvals, [(421, 584, '2021-11-01', 16.45, 'PNP', 0, 0.0),
                                         (621, 584, '2021-11-01', 14.5, 'OD', 0, 0.0),
                                         (509, 584, '2021-11-01', 0.0, 'OD', 1, 0.0),
                                         (421, 585, '2021-11-01', 16.45, 'P', 0, 0.0),
                                         (621, 585, '2021-11-01', 14.5, 'OD', 0, 0.0),
                                         (306, 585, '2021-11-01', 0.0, 'OD', 1, 0.0),
                                         (394, 585, '2021-11-01', 0.0, 'OD', 1, 0.0),
                                         (509, 585, '2021-11-01', 0.0, 'OD', 1, 0.0),
                                         (615, 585, '2021-11-01', 0.0, 'P', 1, 0.0),
                                         (215, 585, '2021-11-01', 0.0, 'OD', 1, 0.0),
                                         (120, 585, '2021-11-01', 0.0, 'P', 1, 0.0),
                                         (520, 585, '2021-11-01', 0.0, 'OD', 1, 0.0)])

    def delete_db():
        """
        Deletes the DB as a part of the setup method.
        """
        if os.path.exists(
                os.getenv('APPDATA') +
                "\\project-time-saver\\database_test.db"):
            os.remove(
                os.getenv('APPDATA') +
                "\\project-time-saver\\database_test.db")


    def removeFile(self):
        """
        Removes the test log json.
        """
        if os.path.isfile(os.getcwd() + "\\test\\resc\\test.json"):
            os.remove(os.getcwd() + "\\test\\resc\\test.json")


if __name__ == '__main__':
    unittest.main()