from importlib.resources import path
import unittest
import os
import sys

from black import assert_equivalent

sys.path.append(os.getcwd())
from lib.backup_manager import backupManager as bM


class backupManager_test(unittest.TestCase):
    def test_hashing(self):
        path = os.getcwd() + "\\test\\resc\\HashingTests\\Test1.txt"
        test_hash = bM.generateHash(path)
        known_hash = "4844031a445e2d525326674b682a431d"
        self.assertEqual(test_hash, known_hash)

    def test_hashing_xlxs(self):
        path = os.getcwd() + "\\test\\resc\\good_tests\\584.xlsx"
        test_hash = bM.generateHash(path)
        known_hash = "6b48244d052d62b20635d635e4252ae1"
        self.assertEqual(test_hash, known_hash)

    def test_checksum_1(self):
        path1 = os.getcwd() + "\\test\\resc\\HashingTests\\Test1.txt"
        path2 = os.getcwd() + "\\test\\resc\\HashingTests\\Test2.txt"
        result = bM.checksum(path1, path2)
        self.assertTrue(result)

    def test_checksum_2(self):
        path1 = os.getcwd() + "\\test\\resc\\HashingTests\\Test1.txt"
        path2 = os.getcwd() + "\\test\\resc\\HashingTests\\Test3.txt"
        result = bM.checksum(path1, path2)
        self.assertFalse(result)

    def test_uploadDatabase(self):
        path = os.getcwd() + "\\test\\resc\\HashingTests\\Test1.txt"
        result = bM.uploadLocalDB(
            bM.getLocalDB(path), os.getcwd() + "\\test\\resc\\HashingTests\\UploadTest"
        )
        known = os.getcwd() + "\\test\\resc\\HashingTests\\UploadTest\\Test1.txt"
        self.assertEqual(result, known)


if __name__ == "__main__":
    unittest.main()
