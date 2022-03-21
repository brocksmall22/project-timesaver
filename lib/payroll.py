from datetime import datetime
import os
from sqlite3.dbapi2 import Timestamp
from .sqlFunctions import sqlFunctions
from .logger import Logger
from .oneDriveConnect import oneDriveConnect
from .report_reader import report_reader
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
                        with report_reader(file) as reportReader:
                            payroll.processIncident(reportReader, sqlRunner, file, test_log_location, database)
            except Exception as e:
                print(e)
                traceback.print_exc()
                Logger.addNewError("I/O error", datetime.now(), 
                                    f"File {file} has error: Critical error, file cannot be read!", 
                                    file = test_log_location)
                success = False
        return success


    def processIncident(reportReader, sqlRunner, filename, test_log_location, database = os.getenv('APPDATA') + "\\project-time-saver\\database.db"):
        """
        TODO: Update this docstring

        readWorkBook(wb, filename)
        reads an indiual work book then prints the resulting values from in the range of cells A21->F55
        It requires the Workbook and the Filename
        """
        Timestamp = oneDriveConnect.getLastModifiedDate(filename)
        try:
            date, runNumber, needsUpdated = payroll.getRunInfo(
                sqlRunner, reportReader, Timestamp)
            assert runNumber == int(oneDriveConnect.extensionStripper(filename)), "The file's name and the incident number within do not match"
            if needsUpdated:
                payroll.getEmpinfo(sqlRunner, reportReader, date, runNumber)
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


    def getRunInfo(sqlRunner, reportReader, Timestamp):
        """
        This gets the Run info from the sheet and runs the SQL import statements.

        inputs..
            sqlRunner: the sql class object
            reportReader: the object for getting information
                out of a run
        returns:
            case 1: the run, date, and run number of the workbook
        """
        runInfo = reportReader.getRunInfo()
        if sqlRunner.newRunNeedsUpdated(runInfo["runNumber"], Timestamp, payroll.Year):
            sqlRunner.updateRun(runInfo["runNumber"], runInfo["date"], runInfo["startTime"],
                    runInfo["endTime"], runInfo["runTime"], runInfo["stationCovered"],
                    runInfo["medRun"], runInfo["shift"], Timestamp, runInfo["fullCover"],
                    runInfo["fsc"], runInfo["paid"], runInfo['OIC'], runInfo['SO'],
                    runInfo['filer'], runInfo['1076'], runInfo['1023'], runInfo['UC'],
                    runInfo['1008'], runInfo['workingHours'], runInfo['offHours'],
                    runInfo['apparatus'], runInfo['township'], runInfo['givenAid'],
                    runInfo['takenAid'])
            return runInfo["date"], runInfo["runNumber"], True
        elif not sqlRunner.checkIfExists(runInfo["runNumber"], runInfo["date"]):
            sqlRunner.createRun(runInfo["runNumber"], runInfo["date"], runInfo["startTime"],
                    runInfo["endTime"], runInfo["runTime"], runInfo["stationCovered"],
                    runInfo["medRun"], runInfo["shift"], Timestamp, runInfo["fullCover"],
                    runInfo["fsc"], runInfo["paid"], runInfo['OIC'], runInfo['SO'],
                    runInfo['filer'], runInfo['1076'], runInfo['1023'], runInfo['UC'],
                    runInfo['1008'], runInfo['workingHours'], runInfo['offHours'],
                    runInfo['apparatus'], runInfo['township'], runInfo['givenAid'],
                    runInfo['takenAid'])
            return runInfo["date"], runInfo["runNumber"], True
        return runInfo["date"], runInfo["runNumber"], False