import sys
import io
import os
from tkinter import N
from tkinter.messagebox import NO
import unittest

sys.path.append(os.getcwd())
from lib.visualize import visualize

class visualize_test(unittest.TestCase):
    """
    This class tests the output from the 'visualize' class to ensure that
    each figure creates the expected output on a fixed input.

    This set of tests is safe to run on a "live" system and will not affect
    a production database, log, or config.
    """
    dbFile = os.getcwd() + "\\test\\resc\\oct2021_good.db"
    testLog = os.getcwd() + "\\test\\resc\\test_log.json"
    startDate = "2021-09-01"
    endDate = "2021-11-30"
    plotApparatusUsageFrequencyExpected = None
    plotGivenAidExpected = None
    plotRunStartTimeDistributionExpected = None
    plotRunTownshipsExpected = None
    plotShiftCoverageExpected = None
    plotTakenAidExpected = None
    plotTypesOfRunsExpected = None
    
    @classmethod
    def setUpClass(cls):
        """
        This method sets up all of the variables for testing and ensures
        there are no files left over from previous/incomplete tests.
        """
        visualize_test.delete_files()
        basePath = os.getcwd() + "\\test\\resc\\expected_figures\\"
        with open(f"{basePath}plotApparatusUsageFrequencyExpected.png", "rb") as file:
            visualize_test.plotApparatusUsageFrequencyExpected = io.BytesIO(file.read())
        with open(f"{basePath}plotGivenAidExpected.png", "rb") as file:
            visualize_test.plotGivenAidExpected = io.BytesIO(file.read())
        with open(f"{basePath}plotRunStartTimeDistributionExpected.png", "rb") as file:
            visualize_test.plotRunStartTimeDistributionExpected = io.BytesIO(file.read())
        with open(f"{basePath}plotRunTownshipsExpected.png", "rb") as file:
            visualize_test.plotRunTownshipsExpected = io.BytesIO(file.read())
        with open(f"{basePath}plotShiftCoverageExpected.png", "rb") as file:
            visualize_test.plotShiftCoverageExpected = io.BytesIO(file.read())
        with open(f"{basePath}plotTakenAidExpected.png", "rb") as file:
            visualize_test.plotTakenAidExpected = io.BytesIO(file.read())
        with open(f"{basePath}plotTypesOfRunsExpected.png", "rb") as file:
            visualize_test.plotTypesOfRunsExpected = io.BytesIO(file.read())

    
    @classmethod
    def tearDownClass(cls):
        visualize_test.delete_files()


    def test_plotApparatusUsageFrequency(self):
        """
        Generates the apparatus frequency figure and tests against
        one on the disk.
        """
        value = visualize.plotApparatusUsageFrequency(visualize_test.startDate,
                                                              visualize_test.endDate,
                                                              dbFile = visualize_test.dbFile,
                                                              test_log_location = visualize_test.testLog)
        self.assertEqual(value.getvalue(), visualize_test.plotApparatusUsageFrequencyExpected.getvalue())


    def test_plotGivenAid(self):
        """
        Generates the given aid figure and tests against
        one on the disk.
        """
        value = visualize.plotGivenAid(visualize_test.startDate,
                                                              visualize_test.endDate,
                                                              dbFile = visualize_test.dbFile,
                                                              test_log_location = visualize_test.testLog)
        self.assertEqual(value.getvalue(), visualize_test.plotGivenAidExpected.getvalue())


    def test_plotRunStartTimeDistribution(self):
        """
        Generates the start time distribution figure and tests against
        one on the disk.
        """
        value = visualize.plotRunStartTimeDistribution(visualize_test.startDate,
                                                              visualize_test.endDate,
                                                              dbFile = visualize_test.dbFile,
                                                              test_log_location = visualize_test.testLog)
        self.assertEqual(value.getvalue(), visualize_test.plotRunStartTimeDistributionExpected.getvalue())


    def test_plotRunTownships(self):
        """
        Generates the township frequency figure and tests against
        one on the disk.
        """
        value = visualize.plotRunTownships(visualize_test.startDate,
                                                              visualize_test.endDate,
                                                              dbFile = visualize_test.dbFile,
                                                              test_log_location = visualize_test.testLog)
        self.assertEqual(value.getvalue(), visualize_test.plotRunTownshipsExpected.getvalue())


    def test_plotShiftCoverage(self):
        """
        Generates the shift coverage frequency figure and tests against
        one on the disk.
        """
        value = visualize.plotShiftCoverage(visualize_test.startDate,
                                                              visualize_test.endDate,
                                                              dbFile = visualize_test.dbFile,
                                                              test_log_location = visualize_test.testLog)
        self.assertEqual(value.getvalue(), visualize_test.plotShiftCoverageExpected.getvalue())


    def test_plotTakenAid(self):
        """
        Generates the taken aid figure and tests against
        one on the disk.
        """
        value = visualize.plotTakenAid(visualize_test.startDate,
                                                              visualize_test.endDate,
                                                              dbFile = visualize_test.dbFile,
                                                              test_log_location = visualize_test.testLog)
        self.assertEqual(value.getvalue(), visualize_test.plotTakenAidExpected.getvalue())


    def test_plotTypesOfRuns(self):
        """
        Generates the incident type frequency figure and tests against
        one on the disk.
        """
        value = visualize.plotTypesOfRuns(visualize_test.startDate,
                                                              visualize_test.endDate,
                                                              dbFile = visualize_test.dbFile,
                                                              test_log_location = visualize_test.testLog)
        self.assertEqual(value.getvalue(), visualize_test.plotTypesOfRunsExpected.getvalue())


    def delete_files():
        if os.path.exists(visualize_test.testLog):
            os.remove(visualize_test.testLog)
        

if __name__ == '__main__':
    unittest.main()