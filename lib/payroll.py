from io import RawIOBase
import os
from openpyxl import load_workbook
import sqlite3
from sqlite3 import Error

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
            try:
                wb = load_workbook(file)
                payroll.readWorkBook(wb, file)
            except Exception as e:
                print(e)
                payroll.returnArray.append(f"File {file} has error: Critical error, file cannot be read!")

        if payroll.returnArray == []:
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
            payroll.returnArray.append(f"File {filename} has error: {e}")

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
                if sheet[f"L{payroll.endRange + 1}"].value != "=":
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
        for i1 in sheet[f"A21:H{payroll.endRange}"]:

            if i1[4].value is not None or i1[5].value is not None or i1[6].value is not None:
                if i1[0].value is None: raise Exception("Employee number cannot be empty!")
                if i1[1].value is None: raise Exception("Employee name cannot be empty!")

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
                elif i1[5].value is not None:
                    type_of_response = "P"
                elif i1[6].value is not None:
                    type_of_response = "OD"

                if payroll.empNeedsUpdated(conn, empNumber):
                    payroll.updateEmp(conn, Name, empNumber)
                else:
                    payroll.createEmployee(conn, Name, empNumber)
                if payroll.respondedNeedsUpdated(conn, empNumber, date, runNumber):
                    payroll.updateResponded(
                        conn, empNumber, payRate, date, runNumber, type_of_response, full_time)
                else:
                    payroll.createResponded(
                        conn, empNumber, payRate, date, runNumber, type_of_response, full_time)

    """
    getRunInfo(conn, wb)
    This gets the Run info from the sheet and runs the SQL import statements
    it requires the SQL connection and the workbook file
    It retuns the Run Date and Number
    """
    def getRunInfo(conn, wb):
        sheet = wb.active
        if sheet["D3"].value is None: raise Exception("Date cannot be empty!")
        if sheet["B3"].value is None: raise Exception("Run number cannot be empty!")
        if sheet["B8"].value is None: raise Exception("Run time cannot be empty!")
        if sheet["B5"].value is None: raise Exception("Reported cannot be empty!")
        if sheet["L5"].value is None: raise Exception("10-8 cannot be empty!")
        if sheet["F3"].value is None: raise Exception("Shift cannot be empty!")

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

        if payroll.runNeedsUpdated(conn, runNumber, date):
            payroll.updateRun(conn, runNumber, date, startTime,
                              endTime, runTime, stationCovered, medrun, shift, fullCover)
        else:
            payroll.createRun(conn, runNumber, date, startTime,
                              endTime, runTime, stationCovered, medrun, shift, fullCover)
        return date, runNumber

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

# -----------------------------------------------------------------------------------------------------------------------
    """
    createConnection(db_file)
    this creates the connection to the SQL database
    it requires the path to the Database
    """
    def createConnection(dbFile):
        conn = None
        try:
            conn = sqlite3.connect(dbFile)
            return conn
        except Error as e:
            print(e)
        return conn

    """
    This contains all of the SQL functions related to Runs
    -------------------------------------------------------------------------------------------------------
    createRun(conn, runNumber, date, stopTime, endTime, runTime, Covered, Medrun, shift) 
    this is the general insertion of runs into the data base.
    it requires the runNumber, Date, StartTime, EndTime, Runtime,Bool for station covered, bool for Medrun, and the connextion to the sql database
    -------------------------------------------------------------------------------------------------------
    updateRun(conn, num, date, startTime, endTime, runTime)
    this updates the run given that it has alredy been insterted into the database and has differing information then therun alredy has
     it requires the runNumber, Date, StartTime, EndTime, Runtime,Bool for station covered, bool for Medrun, and the connextion to the sql database
    -------------------------------------------------------------------------------------------------------
    runNeedsUpdated(conn, num, date)
    this checks the runs alredy in the database against the given information to see if the run needs to be updatded
    it requires the Run number, date, and connection to the sql database
    """
    def createRun(conn, runNumber, date, stopTime, endTime, runTime, Covered, Medrun, shift, fullCover):
        sql = """ INSERT INTO Run(number, date, startTime, stopTime, runTime, Covered, Medrun, shift, full_coverage)
                VALUES({0},\'{1}\',{2},{3},{4}, {5}, {6}, \'{7}\', {8}) """
        cur = conn.cursor()
        sql = sql.format(runNumber, date, stopTime,
                         endTime, runTime, Covered, Medrun, shift, fullCover)
        cur.execute(sql)
        return cur.lastrowid

    def updateRun(conn, runNumber, date, startTime, endTime, runTime, Covered, Medrun, shift, fullCover):
        statement = f"""UPDATE Run SET runTime = {runTime}, startTime = {startTime}, stopTime = {endTime}, 
            Covered = {Covered}, Medrun = {Medrun}, shift = \'{shift}\', full_coverage = {fullCover} WHERE number = {runNumber} AND date = \'{date}\';"""
        cur = conn.cursor()
        cur.execute(statement)
        return cur.lastrowid

    def runNeedsUpdated(conn, runNumber, date):
        statement = f"""SELECT * FROM Run WHERE Date = \'{date}\' AND number = {runNumber};"""
        cur = conn.cursor()
        cur.execute(statement)
        values = cur.fetchall()

        return False if len(values) == 0 else True

    """
    This Contains all of the SQL functions related to the Responded tabel
    -------------------------------------------------------------------------------------------------------
    createResponded(conn, empNumber, payRate, date, num)
    this is the general insertion for the Responded Table
    it requires the connection to the SQL database as well as the Employee number, payrate, date of the run, and the run number
    -------------------------------------------------------------------------------------------------------
    respondedNeedsUpdated(conn, empNumber, date, rNum)
    this is to check the responded table against the given information to see if the responded table needs to be updated 
    it requires the SQL Connection as well as Employee number, date of the run, and the run number
    -------------------------------------------------------------------------------------------------------
    updateResponded(conn, empNumber, payRate, date, rNum)
    this is to update the responded table
    it requires the connection to the SQL database as well as the Employee number, payrate, date of the run, and the run number
    """
    def createResponded(conn, empNumber, payRate, date, num, type_of_response, full_time):
        sql = """INSERT INTO Responded(empNumber, runNumber, date, payRate, type_of_response, full_time)
                VALUES({0},{1},\'{2}\',{3},'{4}',{5}) """
        cur = conn.cursor()
        sql = sql.format(empNumber, num, date, payRate, type_of_response, full_time)
        cur.execute(sql)
        return cur.lastrowid

    def respondedNeedsUpdated(conn, empNumber, date, rNum):
        statement = f"""SELECT * FROM Responded WHERE Date = \'{date}\' AND empNumber = {empNumber} AND runNumber = {rNum};"""
        cur = conn.cursor()
        cur.execute(statement)
        values = cur.fetchall()

        return False if len(values) == 0 else True

    def updateResponded(conn, empNumber, payRate, date, rNum, type_of_response, full_time):
        statement = f"""UPDATE Responded SET payRate = {payRate}, type_of_response = '{type_of_response}', 
            full_time = {full_time} WHERE empNumber = {empNumber} AND date = \'{date}\' AND runNumber = {rNum};"""
        cur = conn.cursor()
        cur.execute(statement)
        return cur.lastrowid
    """
    This Contains all of the SQL functions related to the Employee tabel
    -------------------------------------------------------------------------------------------------------
    createEmployee(conn, name, empNumber)
    This is the insertion for the Employee table
    It requires the SQL connection as well as the name, and employee number
    -------------------------------------------------------------------------------------------------------
    empNeedsUpdated(conn, empNumber)
    this checks the Employee table against the given information to see if it needs to be updated
    it rquires the SQL connection as well as the Employee number
    -------------------------------------------------------------------------------------------------------
    updateEmp(conn, name ,empNumber)
    this updates the employee table given the new information
    it requires the SQL connection as well as the Employee Name and Number
    """
    def createEmployee(conn, name, empNumber):
        sql = f""" INSERT INTO Employee(name,number)
                VALUES(\'{name}\',{empNumber}) """
        cur = conn.cursor()
        cur.execute(sql)
        return cur.lastrowid

    def empNeedsUpdated(conn, empNumber):
        statement = f"""SELECT * FROM Employee WHERE number = {empNumber};"""
        cur = conn.cursor()
        cur.execute(statement)
        values = cur.fetchall()

        return False if len(values) == 0 else True

    def updateEmp(conn, name, empNumber):
        statement = f"""UPDATE Employee SET name = \'{name}\' WHERE number = {empNumber};"""
        cur = conn.cursor()
        cur.execute(statement)
        return cur.lastrowid
