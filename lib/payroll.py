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

    endRange = 0
    Year = datetime.now().strftime("%Y") + "-1-1"


    def loadWorkBooks(fileList = [], test_log_location = ""):
        """
        loadWorkBooks(fileList)
        loops Through the fileList array and runs the readWorkBook on each file this is the main driver for the program
        This requires the whole file list

        TODO: Fix error handling here. if SQL statement fails, causes error that looks like an I/O error
        TODO: Add error for when no folder is set
        """
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


    def readWorkBook(wb, filename, test_log_location):
        """
        readWorkBook(wb, filename)
        reads an indiual work book then prints the resulting values from in the range of cells A21->F55
        It requires the Workbook and the Filename
        """
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
            traceback.print_exc()
            Logger.addNewError("report format error", datetime.now(), f"File {filename} has error: {e}", file = test_log_location)


    def reset():
        """
        Resets the global variables for the next run of this class.
        """
        payroll.endRange = 0


    def getRange(wb):
        """
        This function loops through the work book file to determine
        the row containing the last employee.

        inputs..
            wb: the workbook being processed
        """
        end = False
        sheet = wb.active
        if payroll.endRange == 0:
            payroll.endRange = 21
            while (not end):
                if sheet[f"L{payroll.endRange + 1}"].value != "=":
                    payroll.endRange = payroll.endRange + 1
                else:
                    end = True


    def checkForErrors(wb):
        """
        This method stops execution and raises an error if there is a detectable issue
        with a run sheet.

        inputs..
            wb: the workbook of the current run sheet
        """
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


    def getEmpinfo(sqlRunner, wb, date, runNumber):
        """
        getEmpinfo(sqlRunner, wb, date, rNum)
        This gets the Employee information from the wb file then
        it runs the employee and Responded SQL insertions.

        inputs..
            sqlRunner: the sql class object
            wb: the workbook being processed
            date: the date of the run
            rNum: the number of the run
        """
        sheet = wb.active
        for i1 in sheet[f"A21:O{payroll.endRange}"]:
            if i1[4].value is not None or i1[5].value is not None or i1[6].value is not None:
                empNumber = wb["Pay"][i1[0].value.split("!")[1]].value
                if i1[7].value is not None:
                    payRate = wb["Pay"][i1[7].value.split("!")[1]].value
                    full_time = 0
                else:
                    payRate = 0
                    full_time = 1
                Name = wb["Pay"][i1[1].value.split("!")[1]].value
                if i1[4].value is not None:
                    type_of_response = "PNP"
                elif i1[6].value is not None:
                    type_of_response = "OD"
                elif i1[5].value is not None:
                    type_of_response = "P"
                subhours = int(i1[14].value) if i1[14].value is not None else 0
                print(f"Responder: {Name}; number: {empNumber}; type: {type_of_response}; full-time: {full_time}")
                if sqlRunner.empNeedsUpdated(empNumber):
                    sqlRunner.updateEmp(Name, empNumber)
                else:
                    sqlRunner.createEmployee(Name, empNumber)
                if sqlRunner.respondedNeedsUpdated(empNumber, date, runNumber):
                    sqlRunner.updateResponded(
                        empNumber, payRate, date, runNumber, type_of_response, full_time, subhours)
                else:
                    sqlRunner.createResponded(
                        empNumber, payRate, date, runNumber, type_of_response, full_time, subhours)


    def getRunInfo(sqlRunner, wb, Timestamp):
        """
        This gets the Run info from the sheet and runs the SQL import statements.

        inputs..
            sqlRunner: the sql class object
            wb: the workbook we are processing
        returns:
            case 1: the run, date, and run number of the workbook
        """
        sheet = wb.active
        date = sheet["D3"].value.strftime("%Y-%m-%d")
        runNumber = sheet["B3"].value
        runTime = sheet["B8"].value
        startTime = sheet["B5"].value
        endTime = sheet["L5"].value
        shift = sheet["F3"].value
        fsc = 1 if payroll.checkForFill(sheet, "Q6") else 0
        stationCovered = 1 if payroll.checkForFill(sheet, "F6") else 0
        medrun = 1 if sheet == wb["MED RUN"] else 0
        fullCover = payroll.getFullCover(sheet, shift)
        paid = payroll.isPaid(sheet, fsc, medrun)
        print("\n\n\n\n")
        print(f"Processing run: {runNumber} from date {date}")
        print(f"Medrun: {medrun}; FSC: {fsc}; runTime: {runTime}")
        print(f"Start: {startTime}; end: {endTime}; station covered: {stationCovered}")
        print(f"shift: {shift}; fully covered: {fullCover}, paid: {paid}")
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


    def checkForFill(sheet, cell: str) -> bool:
        """
        This method is to check if the given cell is filled or not.
        Checks for color, legacy index, and any text/number value.

        inputs..
            sheet: the sheet we are checking
        outputs..
            case 1: False if it is not filled
            case 2: True if it is
        """
        color = sheet[cell].fill.start_color.index
        if type(color) == int:
            return False if color == 1 else True
        else:
            return False if color == "00000000" and\
                sheet[cell].value == None else True


    def isPaid(sheet, fsc, medrun):
        """
        This method is for determining if a run is paid or not. Some FSC runs are paid,
        others are not, so this method sorts them out.

        inputs..
            sheet: the sheet we are checking
            fsc: the bit that determines if it is a FSC run
            medrun: the bit that determines if it is a medrun
        outputs..
            case 1: 0 if it is not paid
            case 2: 1 if it is paid
        """
        if medrun == 1:
            return 0
        if fsc == 1 and sheet["D5"].value != None:
            return 1
        if fsc == 1:
            for i1 in sheet[f"E21:G{payroll.endRange}"]:
                if i1[0] not in [None, ""] or i1[1] not in [None, ""]:
                    return 0
            return 1
        if fsc == 0 and medrun == 0:
            return 1


    def getFullCover(sheet, shift) -> int:
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
