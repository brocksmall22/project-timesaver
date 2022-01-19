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
        ConfigManager.createConfigIfNotExists(os.getcwd() + "\\test\\resc\\test.json")
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
    Removes the test log json.
    """
    def removeFile(self):
        os.remove(os.getcwd() + "\\test\\resc\\test.json")


if __name__ == "__main__":
    unittest.main()