import unittest
import os
import sys
from openpyxl.reader.excel import load_workbook

sys.path.append(os.getcwd())
from sqlite.check_database import check_database
from lib.generate_report import generate_report as gp
from lib.payroll import payroll as p

"""
This test class tests the generation of the report tally.

WARNING: This clas is destructive. It will delete the database,
make backups as needed before running.
"""
class generate_report_test(unittest.TestCase):
    """
    This method deletes the database, makes a new one, and populates it.
    """
    @classmethod
    def setUpClass(cls):
        generate_report_test.delete_db()
        check_database.check()
        p.loadWorkBooks([os.getcwd() + "\\test\\resc\\good_1.xlsx",
            os.getcwd() + "\\test\\resc\\good_2.xlsx"])

    """
    This is the actual test.
    """
    def test_generate_tally(self):
        results = gp.generate_report("2021-11-01", "2021-11-07")
        self.assertEqual(type(results[0]), type(True))
        self.assertEqual(generate_report_test.get_total(), 0)

    """
    This function helps ensure the inputted values are correct. It is
    100% logically dependant on the runs inputted, so if you change which
    files you submit to the database, you will have to restructure this.
    """
    def get_total():
        wb = load_workbook(os.getenv('APPDATA') + "\\project-time-saver\\tally.xlsx",
                data_only=True)
        sheet = wb.active
        notNone = True
        total = 0
        row = 8
        while notNone == True:
            if sheet[f"E{row}"].value is not None and int(sheet[f"E{row}"].value) != 0:
                total = float(sheet[f"H{row}"].value)
            if sheet[f"E{row}"].value is None:
                notNone = False
            else:
                row += 1
        return total

    """
    Deletes the DB as a part of the setup method.
    """
    def delete_db():
        if os.path.exists(os.getenv('APPDATA') + "\\project-time-saver\\database.db"):
            os.remove(os.getenv('APPDATA') + "\\project-time-saver\\database.db")

if __name__ == "__main__":
    unittest.main()