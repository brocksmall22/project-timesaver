import unittest
import os
import json
import sys

sys.path.append(os.getcwd())
from lib.config_manager import ConfigManager

"""
This test class tests the generation of the report tally.
WARNING: This clas is destructive. It will delete the database,
make backups as needed before running.
"""
class config_manager_test(unittest.TestCase):
    """
    Makse sure a new json can be created.
    """
    def test_create_file(self):
        ConfigManager.createConfigIfNotExists(file = os.getcwd() + "\\test\\resc\\test.json")
        self.assertTrue(os.path.isfile(os.getcwd() + "\\test\\resc\\test.json"))
        with open(os.getcwd() + "\\test\\resc\\test.json", "r") as testFile:
            contents = json.load(testFile)
            self.assertTrue(all (k in contents for k in ["folder_path"]))
        self.removeFile()

    """
    Makes sure that the folder can be set.
    """
    def test_set_folder(self):
        ConfigManager.set_folderPath("C:\\some\\path", file = os.getcwd() + "\\test\\resc\\test.json")
        with open(os.getcwd() + "\\test\\resc\\test.json", "r") as testFile:
            contents = json.load(testFile)
            self.assertEqual(contents["folder_path"], "C:\\some\\path")
        self.removeFile()

    """
    Makes sure that the folder can be gotten.
    """
    def test_get_folder(self):
        ConfigManager.set_folderPath("C:\\some\\path", file = os.getcwd() + "\\test\\resc\\test.json")
        contents = ConfigManager.get_folderPath(os.getcwd() + "\\test\\resc\\test.json")
        self.assertEqual(contents, "C:\\some\\path")
        self.removeFile()

    """
    Test to ensure the backup path can be set.
    """
    def test_set_backup_path(self):
        ConfigManager.set_backupPath("C:\\some\\path", file = os.getcwd() + "\\test\\resc\\test.json")
        with open(os.getcwd() + "\\test\\resc\\test.json", "r") as testFile:
            contents = json.load(testFile)
            self.assertEqual(contents["Backup_path"], "C:\\some\\path")
        self.removeFile()

    """
    Test to ensure the backup path can be retrieved.
    """
    def test_get_backup_path(self):
        ConfigManager.set_backupPath("C:\\some\\path", file = os.getcwd() + "\\test\\resc\\test.json")
        contents = ConfigManager.get_backupPath(os.getcwd() + "\\test\\resc\\test.json")
        self.assertEqual(contents, "C:\\some\\path")
        self.removeFile()

    """
    Test to ensure the breakdown path can be set.
    """
    def test_set_breakdown_path(self):
        ConfigManager.set_blankBreakdownPath("C:\\some\\path", file = os.getcwd() + "\\test\\resc\\test.json")
        with open(os.getcwd() + "\\test\\resc\\test.json", "r") as testFile:
            contents = json.load(testFile)
            self.assertEqual(contents["blank_breakdown_path"], "C:\\some\\path")
        self.removeFile()

    """
    Test to ensure the breakdown path can be retrieved.
    """
    def test_get_breakdown_path(self):
        ConfigManager.set_blankBreakdownPath("C:\\some\\path", file = os.getcwd() + "\\test\\resc\\test.json")
        contents = ConfigManager.get_blankBreakdownPath(os.getcwd() + "\\test\\resc\\test.json")
        self.assertEqual(contents, "C:\\some\\path")
        self.removeFile()

    """
    Tests to ensure the paroll path can be set.
    """
    def test_set_payroll_path(self):
         ConfigManager.set_blankPayrollPath("C:\\some\\path", file = os.getcwd() + "\\test\\resc\\test.json")
         with open(os.getcwd() + "\\test\\resc\\test.json", "r") as testFile:
             contents = json.load(testFile)
             self.assertEqual(contents["blank_payroll_path"], "C:\\some\\path")
         self.removeFile()

    """
    Tests to ensure the payroll path can be retrieved.
    """
    def test_get_payroll_path(self):
        ConfigManager.set_blankPayrollPath("C:\\some\\path", file = os.getcwd() + "\\test\\resc\\test.json")
        contents = ConfigManager.get_blankPayrollPath(os.getcwd() + "\\test\\resc\\test.json")
        self.assertEqual(contents, "C:\\some\\path")
        self.removeFile()

    """
    Tests to ensure the layout configurations can be set.
    """
    def test_set_cellLocations(self):
         ConfigManager.set_cellLocations([{"startDate": "",
                                              "endDate": "",
                                              "incidentNumber": "",
                                              "date": "",
                                              "shift": "",
                                              "OIC": "",
                                              "SO": "",
                                              "filer": "",
                                              "reported": "",
                                              "paged": "",
                                              "1076": "",
                                              "1023": "",
                                              "UC": "",
                                              "1008": "",
                                              "stationCovered": "",
                                              "weekend": "",
                                              "workingHours": "",
                                              "offHours": "",
                                              "shiftCovered": "",
                                              "runTime": "",
                                              "firstEmployeeRow": "",
                                              "runType": {},
                                              "apparatus": {},
                                              "township": {
                                              "harrison": {"city": "", "county": ""},
                                              "lancaster": {"city": "", "county": ""}
                                              },
                                              "givenAid": {},
                                              "takenAid": {}},
                                              {"startDate": "",
                                              "endDate": "",
                                              "incidentNumber": "",
                                              "date": "",
                                              "shift": "",
                                              "OIC": "",
                                              "SO": "",
                                              "filer": "",
                                              "reported": "",
                                              "paged": "",
                                              "1076": "",
                                              "1023": "",
                                              "UC": "",
                                              "1008": "",
                                              "stationCovered": "",
                                              "weekend": "",
                                              "workingHours": "",
                                              "offHours": "",
                                              "shiftCovered": "",
                                              "runTime": "",
                                              "firstEmployeeRow": "",
                                              "runType": {},
                                              "apparatus": {},
                                              "township": {
                                              "harrison": {"city": "", "county": ""},
                                              "lancaster": {"city": "", "county": ""}
                                              },
                                              "givenAid": {},
                                              "takenAid": {}}],
                                              file = os.getcwd() + "\\test\\resc\\test.json")
         with open(os.getcwd() + "\\test\\resc\\test.json", "r") as testFile:
             contents = json.load(testFile)
             self.assertEqual(contents["cell_locations"], [{"startDate": "",
                                                            "endDate": "",
                                                            "incidentNumber": "",
                                                            "date": "",
                                                            "shift": "",
                                                            "OIC": "",
                                                            "SO": "",
                                                            "filer": "",
                                                            "reported": "",
                                                            "paged": "",
                                                            "1076": "",
                                                            "1023": "",
                                                            "UC": "",
                                                            "1008": "",
                                                            "stationCovered": "",
                                                            "weekend": "",
                                                            "workingHours": "",
                                                            "offHours": "",
                                                            "shiftCovered": "",
                                                            "runTime": "",
                                                            "firstEmployeeRow": "",
                                                            "runType": {},
                                                            "apparatus": {},
                                                            "township": {
                                                            "harrison": {"city": "", "county": ""},
                                                            "lancaster": {"city": "", "county": ""}
                                                            },
                                                            "givenAid": {},
                                                            "takenAid": {}},
                                                            {"startDate": "",
                                                            "endDate": "",
                                                            "incidentNumber": "",
                                                            "date": "",
                                                            "shift": "",
                                                            "OIC": "",
                                                            "SO": "",
                                                            "filer": "",
                                                            "reported": "",
                                                            "paged": "",
                                                            "1076": "",
                                                            "1023": "",
                                                            "UC": "",
                                                            "1008": "",
                                                            "stationCovered": "",
                                                            "weekend": "",
                                                            "workingHours": "",
                                                            "offHours": "",
                                                            "shiftCovered": "",
                                                            "runTime": "",
                                                            "firstEmployeeRow": "",
                                                            "runType": {},
                                                            "apparatus": {},
                                                            "township": {
                                                            "harrison": {"city": "", "county": ""},
                                                            "lancaster": {"city": "", "county": ""}
                                                            },
                                                            "givenAid": {},
                                                            "takenAid": {}}])
         self.removeFile()

    """
    Tests to ensure the layout configurations can be retrieved.
    """
    def test_get_allCellLocationConfigs(self):
        ConfigManager.set_cellLocations([{"startDate": "",
                                            "endDate": "",
                                            "incidentNumber": "",
                                            "date": "",
                                            "shift": "",
                                            "OIC": "",
                                            "SO": "",
                                            "filer": "",
                                            "reported": "",
                                            "paged": "",
                                            "1076": "",
                                            "1023": "",
                                            "UC": "",
                                            "1008": "",
                                            "stationCovered": "",
                                            "weekend": "",
                                            "workingHours": "",
                                            "offHours": "",
                                            "shiftCovered": "",
                                            "runTime": "",
                                            "firstEmployeeRow": "",
                                            "runType": {},
                                            "apparatus": {},
                                            "township": {
                                            "harrison": {"city": "", "county": ""},
                                            "lancaster": {"city": "", "county": ""}
                                            },
                                            "givenAid": {},
                                            "takenAid": {}},
                                            {"startDate": "",
                                            "endDate": "",
                                            "incidentNumber": "",
                                            "date": "",
                                            "shift": "",
                                            "OIC": "",
                                            "SO": "",
                                            "filer": "",
                                            "reported": "",
                                            "paged": "",
                                            "1076": "",
                                            "1023": "",
                                            "UC": "",
                                            "1008": "",
                                            "stationCovered": "",
                                            "weekend": "",
                                            "workingHours": "",
                                            "offHours": "",
                                            "shiftCovered": "",
                                            "runTime": "",
                                            "firstEmployeeRow": "",
                                            "runType": {},
                                            "apparatus": {},
                                            "township": {
                                            "harrison": {"city": "", "county": ""},
                                            "lancaster": {"city": "", "county": ""}
                                            },
                                            "givenAid": {},
                                            "takenAid": {}}],
                                            file = os.getcwd() + "\\test\\resc\\test.json")
        contents = ConfigManager.get_allCellLocationConfigs(os.getcwd() + "\\test\\resc\\test.json")
        self.assertEqual(contents, [{"startDate": "",
                                    "endDate": "",
                                    "incidentNumber": "",
                                    "date": "",
                                    "shift": "",
                                    "OIC": "",
                                    "SO": "",
                                    "filer": "",
                                    "reported": "",
                                    "paged": "",
                                    "1076": "",
                                    "1023": "",
                                    "UC": "",
                                    "1008": "",
                                    "stationCovered": "",
                                    "weekend": "",
                                    "workingHours": "",
                                    "offHours": "",
                                    "shiftCovered": "",
                                    "runTime": "",
                                    "firstEmployeeRow": "",
                                    "runType": {},
                                    "apparatus": {},
                                    "township": {
                                    "harrison": {"city": "", "county": ""},
                                    "lancaster": {"city": "", "county": ""}
                                    },
                                    "givenAid": {},
                                    "takenAid": {}},
                                    {"startDate": "",
                                    "endDate": "",
                                    "incidentNumber": "",
                                    "date": "",
                                    "shift": "",
                                    "OIC": "",
                                    "SO": "",
                                    "filer": "",
                                    "reported": "",
                                    "paged": "",
                                    "1076": "",
                                    "1023": "",
                                    "UC": "",
                                    "1008": "",
                                    "stationCovered": "",
                                    "weekend": "",
                                    "workingHours": "",
                                    "offHours": "",
                                    "shiftCovered": "",
                                    "runTime": "",
                                    "firstEmployeeRow": "",
                                    "runType": {},
                                    "apparatus": {},
                                    "township": {
                                    "harrison": {"city": "", "county": ""},
                                    "lancaster": {"city": "", "county": ""}
                                    },
                                    "givenAid": {},
                                    "takenAid": {}}])
        self.removeFile()

    """
    Removes the test log json.
    """
    def removeFile(self):
        if os.path.exists(os.getcwd() + "\\test\\resc\\test.json"):
            os.remove(os.getcwd() + "\\test\\resc\\test.json")


if __name__ == "__main__":
    unittest.main()