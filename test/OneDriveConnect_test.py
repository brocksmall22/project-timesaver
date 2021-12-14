import unittest
import sqlite3
import os

import sys
sys.path.append(os.getcwd())
from unittest import result
from lib.oneDriveConnect import oneDriveConnect as o

class OneDriveConnect_test(unittest.TestCase):
    goodFiles = []
    badFiles = []

    def test_1_a_getFilesTest1(self):
        path = "C:\\Users\\Flameon9521\\Documents\\GitHub\\project-timesaver\\test\\resc\\good_tests"
        OneDriveConnect_test.goodFiles = o.getFiles(path)
        self.assertEqual(len(OneDriveConnect_test.goodFiles), 2)

    def test_1_b_extensionStripperTest1(self):
        result = o.extensionStripper(OneDriveConnect_test.goodFiles[0])
        self.assertEqual(result, "584")

    def test_1_c_getLastModifiedDateTest1(self):
        result = o.getLastModifiedDate(OneDriveConnect_test.goodFiles[0])
        self.assertEqual(result, 1639447547.951233)

    def test_2_a_getFilesTest2(self):
        path = "C:\\Users\\Flameon9521\\Documents\\GitHub\\project-timesaver\\test\\resc\\bad_tests"
        OneDriveConnect_test.badFiles = o.getFiles(path)

        self.assertEqual(len(OneDriveConnect_test.badFiles), 4)

    def test_2_b_extensionStripperTest2(self):
        result = o.extensionStripper(OneDriveConnect_test.badFiles[2])

        self.assertEqual(result, "623")

    def test_2_c_getLastModifiedDateTest2(self):
        result = o.getLastModifiedDate(OneDriveConnect_test.badFiles[2])

        self.assertEqual(result, 1639447547.9457757)


if __name__ == '__main__':
    unittest.main()
