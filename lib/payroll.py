from datetime import datetime
import os
from sqlite3.dbapi2 import Timestamp
from openpyxl import load_workbook
from .sqlFunctions import sqlFunctions
from .logger import Logger
from .oneDriveConnect import oneDriveConnect
import traceback


class payroll:

    endRange = 0
    Year = datetime.now().strftime("%Y") + "-1-1"

    """
    loadWorkBooks(fileList)
    loops Through the fileList array and runs the readWorkBook on each file this is the main driver for the program
    This requires the whole file list

    TODO: Fix error handling here. if SQL statement fails, causes error that looks like an I/O error
    """
    def loadWorkBooks(fileList = [], test_log_location = ""):
        payroll.reset()
        Logger.setLastUpdate(datetime.now().strftime("%Y-%m-%d %H:%M"), file  = test_log_location)
        if fileList == []:
            fileList = oneDriveConnect.getFiles()
        for file in fileList:
            try:
                with sqlFunctions(os.getenv('APPDATA') + "\\project-time-saver\\database.db") as sqlRunner:
                    Timestamp = oneDriveConnect.getLastModifiedDate(file)
                    fileRunNumber = oneDriveConnect.extensionStripper(file)
                    if sqlRunner.newRunNeedsUpdated(fileRunNumber, Timestamp, payroll.Year) or not sqlRunner.checkIfExists(fileRunNumber, payroll.Year):
                        wb = load_workbook(file)
                        payroll.readWorkBook(wb, file, test_log_location)
            except Exception as e:
                print(e)
                traceback.print_exc()
                Logger.addNewError("I/O error", datetime.now(), f"File {file} has error: Critical error, file cannot be read!", file = test_log_location)

    """
    readWorkBook(wb, filename)
    reads an indiual work book then prints the resulting values from in the range of cells A21->F55
    It requires the Workbook and the Filename
    """
    def readWorkBook(wb, filename, test_log_location):
        Timestamp = oneDriveConnect.getLastModifiedDate(filename)
        try:
            with sqlFunctions(os.getenv('APPDATA') + "\\project-time-saver\\database.db") as sqlRunner:
                payroll.getRange(wb)
                if not payroll.checkForErrors(wb):
                    date, runNumber, needsUpdated= payroll.getRunInfo(
                        sqlRunner, wb, Timestamp)
                    assert runNumber == int(oneDriveConnect.extensionStripper(filename)), "The file's name and the run number within do not match"
                    if needsUpdated:
                        payroll.getEmpinfo(sqlRunner, wb, date, runNumber)
        except Exception as e:
            print(e)
            Logger.addNewError("report format error", datetime.now(), f"File {filename} has error: {e}", file = test_log_location)

    """
    Resets the global variables for the next run of this class.
    """
    def reset():
        payroll.endRange = 0

    """
    getRange(wb)
    this function loops through the work book file
    it requires the work book file
    """
    def getRange(wb):
        end = False
        sheet = wb.active
        if payroll.endRange == 0:
            payroll.endRange = 21
            while (not end):
                if sheet[f"L{payroll.endRange + 1}"].value != "=":
                    payroll.endRange = payroll.endRange + 1
                else:
                    end = True

    """
    This method stops execution and raises an error if there is a detectable issue
    with a run sheet.

    inputs..
        wb: the workbook of the current run sheet
    """
    def checkForErrors(wb):
        sheet = wb.active
        for i1 in sheet[f"A21:h{payroll.endRange}"]:
            if i1[4].value is not None or i1[5].value is not None or i1[6].value is not None:
                if i1[0].value in [None, '']:
                    raise Exception("Employee number cannot be empty!")
                if i1[1].value in [None, '']:
                    raise Exception("Employee name cannot be empty!")
                if sheet["D3"].value in [None, '']:
                    raise Exception("Date cannot be empty!")
        if sheet["B3"].value in [None, '']:
            raise Exception("Run number cannot be empty!")
        if sheet["B8"].value in [None, '']:
            raise Exception("Run time cannot be empty!")
        if sheet["B5"].value in [None, '']:
            raise Exception("Reported cannot be empty!")
        if sheet["L5"].value in [None, '']:
            raise Exception("10-8 cannot be empty!")
        if sheet["F3"].value in [None, '']:
            raise Exception("Shift cannot be empty!")

    """
    getEmpinfo(sqlRunner, wb, date, rNum)
    This gets the Employee information from the wb file then it runs the employee and Responded SQL insertions
    It requires the SQL connection class workbookFile and the Date and RunNumber from the getRunInfo
    """
    def getEmpinfo(sqlRunner, wb, date, runNumber):
        sheet = wb.active
        for i1 in sheet[f"A21:h{payroll.endRange}"]:
            if i1[4].value is not None or i1[5].value is not None or i1[6].value is not None:
                empNumber = wb["Pay"][i1[0].value.split("!")[1]].value
                if i1[7].value is not None:
                    payRate = wb["Pay"][i1[7].value.split("!")[1]].value
                    full_time = 0
                else:
                    payRate = 0
                    full_time = 1
                Name = wb["Pay"][i1[1].value.split("!")[1]].value
                if i1[5].value is not None:
                    type_of_response = "P"
                elif i1[4].value is not None:
                    type_of_response = "PNP"
                elif i1[6].value is not None:
                    type_of_response = "OD"
                if sqlRunner.empNeedsUpdated(empNumber):
                    sqlRunner.updateEmp(Name, empNumber)
                else:
                    sqlRunner.createEmployee(Name, empNumber)
                if sqlRunner.respondedNeedsUpdated(empNumber, date, runNumber):
                    sqlRunner.updateResponded(
                        empNumber, payRate, date, runNumber, type_of_response, full_time)
                else:
                    sqlRunner.createResponded(
                        empNumber, payRate, date, runNumber, type_of_response, full_time)

    """
    getRunInfo(sqlRunner, wb)
    This gets the Run info from the sheet and runs the SQL import statements
    it requires the SQL connection class and the workbook file
    It retuns the Run Date and Number
    """
    def getRunInfo(sqlRunner, wb, Timestamp):
        sheet = wb.active
        date = sheet["D3"].value.strftime("%Y-%m-%d")
        runNumber = sheet["B3"].value
        runTime = sheet["B8"].value
        startTime = sheet["B5"].value
        endTime = sheet["L5"].value
        shift = sheet["F3"].value
        if(sheet["F6"].value is not None):
            stationCovered = 1
        else:
            stationCovered = 0
        if(sheet == wb["MED RUN"]):
            medrun = 1
        else:
            medrun = 0
        fullCover = payroll.getFullCover(sheet, shift)
        if sqlRunner.newRunNeedsUpdated(runNumber, Timestamp, payroll.Year):
            sqlRunner.updateRun(runNumber, date, startTime,
                                endTime, runTime, stationCovered, medrun, shift, Timestamp, fullCover)
            return date, runNumber, True
        elif not sqlRunner.checkIfExists(runNumber, date):
            sqlRunner.createRun(runNumber, date, startTime,
                                endTime, runTime, stationCovered, medrun, shift, Timestamp, fullCover)
            return date, runNumber, True
        return date, runNumber, False

    """
    This function is responsible for determining if a run was fully
    covered by its respective shift.

    inputs..
        sheet: the current run sheet
        shift: the shift of the run
    returns..
        case 1: interger 1 if the run is fully covered
        case 2: interger 0 if the run is not fully covered
    """
    def getFullCover(sheet, shift) -> int:
        fullCover = False
        lastShift = None
        for i in range(21, payroll.endRange + 1):
            if sheet[f"L{i}"].value is not None:
                lastShift = sheet[f"L{i}"].value
            if lastShift == shift and (sheet[f"E{i}"].value is not None or sheet[f"F{i}"].value is not None):
                fullCover = True
            elif lastShift == shift and sheet[f"A{i}"].value not in [000, 0000, "000", "0000"]:
                fullCover = False
                break
        return int(fullCover)
