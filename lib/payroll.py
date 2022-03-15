from datetime import datetime
import os
from pydoc import ispackage
from sqlite3.dbapi2 import Timestamp
from openpyxl import load_workbook
from .sqlFunctions import sqlFunctions
from .logger import Logger
from .oneDriveConnect import oneDriveConnect
import traceback


class payroll:

    Year = datetime.now().strftime("%Y") + "-1-1"


    def loadWorkBooks(fileList = [],
                      test_log_location = "",
                      database = os.getenv('APPDATA') + "\\project-time-saver\\database.db") -> bool:
        """
        Loops Through the fileList array and runs the readWorkBook on each file this is the main driver for the program

        TODO: Fix error handling here. if SQL statement fails, causes error that looks like an I/O error

        inputs..
            fileList (optional): a list of files you wish to process; optional as in production
                the program will automatically retrieve the needed files to update
            test_log_location (optional): a URI for the logfile location; optional as this is
                reserved for testing purposes
        returns..
            True if all files were ingested without error
            False if there were any errors
        """
        success = True
        Logger.setLastUpdate(datetime.now().strftime("%Y-%m-%d %H:%M"), 
                            file  = test_log_location)
        if fileList == []:
            fileList = oneDriveConnect.getFiles()
            if fileList == None:
                Logger.addNewError("Configuration error", datetime.now(), 
                                    "Misconfiguration: no path is set for folder containing proofread run reports.", 
                                    file = test_log_location)
        for file in fileList:
            try:
                with sqlFunctions(database) as sqlRunner:
                    Timestamp = oneDriveConnect.getLastModifiedDate(file)
                    fileRunNumber = oneDriveConnect.extensionStripper(file)
                    if sqlRunner.newRunNeedsUpdated(fileRunNumber, Timestamp, payroll.Year) \
                                or not sqlRunner.checkIfExists(fileRunNumber, payroll.Year):
                        wb = load_workbook(file)
                        payroll.readWorkBook(wb, file, test_log_location, database)
            except Exception as e:
                print(e)
                traceback.print_exc()
                Logger.addNewError("I/O error", datetime.now(), 
                                    f"File {file} has error: Critical error, file cannot be read!", 
                                    file = test_log_location)
                success = False
        return success


    def readWorkBook(wb, filename, test_log_location, database = os.getenv('APPDATA') + "\\project-time-saver\\database.db"):
        """
        readWorkBook(wb, filename)
        reads an indiual work book then prints the resulting values from in the range of cells A21->F55
        It requires the Workbook and the Filename
        """
        Timestamp = oneDriveConnect.getLastModifiedDate(filename)
        try:
            with sqlFunctions(database) as sqlRunner:
                payroll.getRange(wb)
                date, runNumber, needsUpdated= payroll.getRunInfo(
                    sqlRunner, wb, Timestamp)
                assert runNumber == int(oneDriveConnect.extensionStripper(filename)), "The file's name and the run number within do not match"
                if needsUpdated:
                    payroll.getEmpinfo(sqlRunner, wb, date, runNumber)
        except Exception as e:
            print(e)
            traceback.print_exc()
            Logger.addNewError("report format error", datetime.now(), f"File {filename} has error: {e}", file = test_log_location)


    def getEmpinfo(sqlRunner, reportReader, date, runNumber):
        """
        This gets the Employee information from the run report then
        it runs the employee and Responded SQL insertions.

        inputs..
            sqlRunner: the sql class object
            reportReader: the object for getting information
                out of a run
            date: the date of the run
            rNum: the number of the run
        """
        for empInfo in reportReader.getEmployeesInRun():
                if sqlRunner.empNeedsUpdated(empInfo["number"]):
                    sqlRunner.updateEmp(empInfo["name"], empInfo["number"])
                else:
                    sqlRunner.createEmployee(empInfo["name"], empInfo["number"])
                if sqlRunner.respondedNeedsUpdated(empInfo["number"], date, runNumber):
                    sqlRunner.updateResponded(
                        empInfo["number"], empInfo["payRate"], date, runNumber,
                        empInfo["responseType"], empInfo["fullTime"], empInfo["subhours"])
                else:
                    sqlRunner.createResponded(
                        empInfo["number"], empInfo["payRate"], date, runNumber,
                        empInfo["responseType"], empInfo["fullTime"], empInfo["subhours"])


    def getRunInfo(sqlRunner, wb, Timestamp):
        """
        This gets the Run info from the sheet and runs the SQL import statements.

        inputs..
            sqlRunner: the sql class object
            wb: the workbook we are processing
        returns:
            case 1: the run, date, and run number of the workbook
        """
        if sqlRunner.newRunNeedsUpdated(runNumber, Timestamp, payroll.Year):
            sqlRunner.updateRun(runNumber, date, startTime, endTime, runTime, 
                                stationCovered, medrun, shift, Timestamp, 
                                fullCover, fsc, paid)
            return date, runNumber, True
        elif not sqlRunner.checkIfExists(runNumber, date):
            sqlRunner.createRun(runNumber, date, startTime, endTime, runTime, 
                                stationCovered, medrun, shift, Timestamp, 
                                fullCover, fsc, paid)
            return date, runNumber, True
        return date, runNumber, False