from io import RawIOBase
import os
from openpyxl import load_workbook
import sqlFunctions

class payroll:

    returnArray = []
    endRange = 0

    """
    loadWorkBooks(fileList)
    loops Through the fileList array and runs the readWorkBook on each file this is the main driver for the program
    This requires the whole file list
    It returns the retun array of the failed files or true if no files have failed
    """
    def loadWorkBooks(fileList):
        payroll.reset()
        for file in fileList:
            wb = load_workbook(file)

            payroll.readWorkBook(wb, file)

        if len(payroll.returnArray) == 0:
            return [True]
        else:
            return payroll.returnArray

    """
    readWorkBook(wb, filename)
    reads an indiual work book then prints the resulting values from in the range of cells A21->F55
    It requires the Workbook and the Filename
    """
    def readWorkBook(wb, filename):
        conn = payroll.createConnection(
            os.getenv('APPDATA') + "\\project-time-saver\\database.db")
        try:

            payroll.getRange(wb)

            date, runNumber = payroll.getRunInfo(conn, wb)
            payroll.getEmpinfo(conn, wb, date, runNumber)

            conn.commit()
        except Exception as e:
            print(e)
            payroll.returnArray.append(filename)

        conn.close

    """
    Resets the global variables for the next run of this class.
    """
    def reset():
        payroll.endRange = 0
        payroll.returnArray = []

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
                if sheet[f"H{payroll.endRange + 1}"].value != None:
                    payroll.endRange = payroll.endRange + 1
                else:
                    end = True

    """
    getEmpinfo(conn, wb, date, rNum)
    This gets the Employee information from the wb file then it runs the employee and Responded SQL insertions
    It requires the SQL connection workbookFile and the Date and RunNumber from the getRunInfo
    """
    def getEmpinfo(conn, wb, date, runNumber):
        sheet = wb.active
        for i1 in sheet[f"A21:h{payroll.endRange}"]:

            if i1[5].value is not None:
                assert(None not in [i1[0].value, i1[1].value, i1[7].value])
                assert('' not in [i1[0].value, i1[1].value, i1[7].value])
                assert('None' not in [i1[0].value, i1[1].value, i1[7].value])

                empNumber = wb["Pay"][i1[0].value.split("!")[1]].value
                payRate = wb["Pay"][i1[7].value.split("!")[1]].value
                Name = wb["Pay"][i1[1].value.split("!")[1]].value

                if sqlFunctions.empNeedsUpdated(conn, empNumber):
                    sqlFunctions.updateEmp(conn, Name, empNumber)
                else:
                    sqlFunctions.createEmployee(conn, Name, empNumber)
                if sqlFunctions.respondedNeedsUpdated(conn, empNumber, date, runNumber):
                    sqlFunctions.updateResponded(
                        conn, empNumber, payRate, date, runNumber)
                else:
                    sqlFunctions.createResponded(
                        conn, empNumber, payRate, date, runNumber)

    """
    getRunInfo(conn, wb)
    This gets the Run info from the sheet and runs the SQL import statements
    it requires the SQL connection and the workbook file
    It retuns the Run Date and Number
    """
    def getRunInfo(conn, wb):
        sheet = wb.active
        date = str(sheet["D3"].value).split(" ")[0]
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
        assert(None not in [date, runNumber, runTime, startTime, endTime, shift])
        assert('' not in [date, runNumber, runTime, startTime, endTime, shift])
        assert('None' not in [date, runNumber, runTime, startTime, endTime, shift])
        if sqlFunctions.runNeedsUpdated(conn, runNumber, date):
            sqlFunctions.updateRun(conn, runNumber, date, startTime,
                              endTime, runTime, stationCovered, medrun, shift)
        else:
            sqlFunctions.createRun(conn, runNumber, date, startTime,
                              endTime, runTime, stationCovered, medrun, shift)
        return date, runNumber

# -----------------------------------------------------------------------------------------------------------------------

