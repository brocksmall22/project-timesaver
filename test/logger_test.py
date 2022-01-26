from datetime import datetime
import unittest
import os
import json
import sys

sys.path.append(os.getcwd())
from lib.logger import Logger

"""
This test class tests the generation of the report tally.

WARNING: This clas is destructive. It will delete the database,
make backups as needed before running.
"""
class logger_test(unittest.TestCase):
    """
    Makse sure a new json can be created.
    """
    def test_create_file(self):
        Logger.createLogIfNotExists(os.getcwd() + "\\test\\resc\\test.json")
        self.assertTrue(os.path.isfile(os.getcwd() + "\\test\\resc\\test.json"))
        with open(os.getcwd() + "\\test\\resc\\test.json", "r") as testFile:
            contents = json.load(testFile)
            self.assertTrue(all (k in contents for k in ["lastUpdate", "errors", "generateMessages"]))
        self.removeFile()

    """
    Makes sure that new errors can be added.
    """
    def test_add_error(self):
        time = datetime.now()
        Logger.addNewError("test", time, "This is a test error message", file = os.getcwd() + "\\test\\resc\\test.json")
        with open(os.getcwd() + "\\test\\resc\\test.json", "r") as testFile:
            contents = json.load(testFile)
            self.assertEqual(contents["errors"][0]["type"], "test")
            self.assertEqual(contents["errors"][0]["time"], time.strftime("%Y-%m-%d %H:%M:%S"))
            self.assertEqual(contents["errors"][0]["message"], "This is a test error message")
        self.removeFile()

    """
    Makes sure that errors can be gotten.
    """
    def test_get_errors(self):
        time = datetime.now()
        Logger.addNewError("test", time, "This is a test error message", file = os.getcwd() + "\\test\\resc\\test.json")
        contents = Logger.getErrors(os.getcwd() + "\\test\\resc\\test.json")
        self.assertEqual(contents[0]["type"], "test")
        self.assertEqual(contents[0]["time"], time.strftime("%Y-%m-%d %H:%M:%S"))
        self.assertEqual(contents[0]["message"], "This is a test error message")
        Logger.addNewError("test", time, "This is a test error message", file = os.getcwd() + "\\test\\resc\\test.json")
        contents = Logger.getErrors(os.getcwd() + "\\test\\resc\\test.json")
        self.assertEqual(len(contents), 2)
        self.removeFile()

    """
    Ensures that errors can be cleared.
    """
    def test_clear_errors(self):
        time = datetime.now()
        Logger.addNewError("test", time, "This is a test error message", file = os.getcwd() + "\\test\\resc\\test.json")
        Logger.addNewError("test", time, "This is a test error message", file = os.getcwd() + "\\test\\resc\\test.json")
        Logger.clearErrors(os.getcwd() + "\\test\\resc\\test.json")
        contents = Logger.getErrors(os.getcwd() + "\\test\\resc\\test.json")
        self.assertEqual(len(contents), 0)
        self.removeFile()

    """
    Makes sure that new generation messages can be added.
    """
    def test_add_generate_message(self):
        time = datetime.now()
        Logger.addNewGenerateMessage("This is a test error message", file = os.getcwd() + "\\test\\resc\\test.json")
        with open(os.getcwd() + "\\test\\resc\\test.json", "r") as testFile:
            contents = json.load(testFile)
            self.assertEqual(contents["generateMessages"][0], "This is a test error message")
        self.removeFile()

    """
    Makes sure that the generation messages can be gotten.
    """
    def test_get_generate_message(self):
        time = datetime.now()
        Logger.addNewGenerateMessage("This is a test error message", file = os.getcwd() + "\\test\\resc\\test.json")
        contents = Logger.getGenerateMessages(os.getcwd() + "\\test\\resc\\test.json")
        self.assertEqual(contents[0], "This is a test error message")
        Logger.addNewGenerateMessage("This is a test error message", file = os.getcwd() + "\\test\\resc\\test.json")
        contents = Logger.getGenerateMessages(os.getcwd() + "\\test\\resc\\test.json")
        self.assertEqual(len(contents), 2)
        self.removeFile()

    """
    Makes sure that generation messages can be cleared out.
    """
    def test_clear_generate_message(self):
        time = datetime.now()
        Logger.addNewGenerateMessage("This is a test error message", file = os.getcwd() + "\\test\\resc\\test.json")
        Logger.addNewGenerateMessage("This is a test error message", file = os.getcwd() + "\\test\\resc\\test.json")
        Logger.clearGenerateMessages(os.getcwd() + "\\test\\resc\\test.json")
        contents = Logger.getGenerateMessages(os.getcwd() + "\\test\\resc\\test.json")
        self.assertEqual(len(contents), 0)
        self.removeFile()

    """
    Makes sure that the modification time can be set.
    """
    def test_set_modify_time(self):
        time = datetime.now()
        Logger.setLastUpdate(time.strftime("%Y-%m-%d %H:%M:%S"), file = os.getcwd() + "\\test\\resc\\test.json")
        with open(os.getcwd() + "\\test\\resc\\test.json", "r") as testFile:
            contents = json.load(testFile)
            self.assertEqual(contents["lastUpdate"], time.strftime("%Y-%m-%d %H:%M:%S"))
        self.removeFile()

    """
    Makes sure that the modification time can be gotten.
    """
    def test_get_modify_time(self):
        time = datetime.now()
        Logger.setLastUpdate(time.strftime("%Y-%m-%d %H:%M:%S"), file = os.getcwd() + "\\test\\resc\\test.json")
        contents = Logger.getLastUpdate(os.getcwd() + "\\test\\resc\\test.json")
        self.assertEqual(contents, time.strftime("%Y-%m-%d %H:%M:%S"))
        self.removeFile()
        
    """
    Removes the test log json.
    """
    def removeFile(self):
        os.remove(os.getcwd() + "\\test\\resc\\test.json")


if __name__ == "__main__":
    unittest.main()