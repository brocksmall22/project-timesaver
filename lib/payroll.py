from io import RawIOBase
import os
from openpyxl import load_workbook
import sqlite3
from sqlite3 import Error


class payroll:

    database = r"C://sqlite/RunReportDB"
    returnArray = []
    endRange = 0

    """
    loadWorkBooks(fileList)
    loops Through the fileList array and runs the readWorkBook on each file this is the main driver for the program
    This requires the whole file list
    It returns the retun array of the failed files or true if no files have failed
    """
    def loadWorkBooks(fileList):
        for file in fileList:
            print(file)
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
        except Exception as e:
            print(e)
            payroll.returnArray.append(filename)

        conn.close

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

            if i1[5].value == 1:

                empNumber = wb["Pay"][i1[0].value.split("!")[1]].value
                print("Emp Num: " + str(empNumber))
                payRate = wb["Pay"][i1[7].value.split("!")[1]].value
                print("PayRate: " + str(payRate))
                Name = wb["Pay"][i1[1].value.split("!")[1]].value
                print("Name: "+Name)
                if payroll.empNeedsUpdated(conn, empNumber):
                    payroll.updateEmp(conn, Name, empNumber)
                else:
                    payroll.createEmployee(conn, Name, empNumber)
                if payroll.respondedNeedsUpdated(conn, empNumber, date, runNumber):
                    payroll.updateResponded(
                        conn, empNumber, payRate, date, runNumber)
                else:
                    payroll.createResponded(
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
        if(sheet["F6"].value == 1):
            stationCovered = 1
        else:
            stationCovered = 0
        if(sheet == wb["MED RUN"]):
            medrun = 1
        else:
            medrun = 0
        if payroll.runNeedsUpdated(conn, runNumber, date):
            payroll.updateRun(conn, runNumber, date, startTime,
                              endTime, runTime, stationCovered, medrun, shift)
        else:
            payroll.createRun(conn, runNumber, date, startTime,
                              endTime, runTime, stationCovered, medrun, shift)
        return date, runNumber

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
    createRun 
    this is the general insertion of runs into the data base.
    it requires the runNumber, Date, StartTime, EndTime, Runtime, and the connextion to the sql database
    -------------------------------------------------------------------------------------------------------
    updateRun(conn, num, date, startTime, endTime, runTime)
    this updates the run given that it has alredy been insterted into the database and has differing information then therun alredy has
    it requires the runNumber, Date, StartTime, EndTime, Runtime, and the connextion to the sql database
    -------------------------------------------------------------------------------------------------------
    runNeedsUpdated(conn, num, date)
    this checks the runs alredy in the database against the given information to see if the run needs to be updatded
    it requires the Run number, date, and connection to the sql database
    """
    def createRun(conn, runNumber, date, stopTime, endTime, runTime, Covered, Medrun, shift):
        sql = """ INSERT INTO Run(number, date, startTime, stopTime, runTime, Covered, Medrun, shift)
                VALUES({0},\'{1}\',{2},{3},{4}, {5}, {6}, \'{7}\') """
        cur = conn.cursor()
        sql = sql.format(runNumber, date, stopTime,
                         endTime, runTime, Covered, Medrun, shift)
        print(sql)
        cur.execute(sql)
        conn.commit()
        return cur.lastrowid

    def updateRun(conn, runNumber, date, startTime, endTime, runTime, Covered, Medrun, shift):
        statement = f"""UPDATE Run SET runTime = {runTime}, startTime = {startTime}, stopTime = {endTime}, Covered = {Covered}, Medrun = {Medrun}, shift = \'{shift}\' WHERE number = {runNumber} AND date = \'{date}\';"""
        cur = conn.cursor()
        cur.execute(statement)
        conn.commit()
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
    def createResponded(conn, empNumber, payRate, date, num):
        sql = """ INSERT INTO Responded(empNumber, runNumber, date, payRate)
                VALUES({0},{1},\'{2}\',{3}) """
        cur = conn.cursor()
        sql = sql.format(empNumber, num, date, payRate)
        print(sql)
        cur.execute(sql)
        conn.commit()
        return cur.lastrowid

    def respondedNeedsUpdated(conn, empNumber, date, rNum):
        statement = f"""SELECT * FROM Responded WHERE Date = \'{date}\' AND empNumber = {empNumber} AND runNumber = {rNum};"""
        cur = conn.cursor()
        cur.execute(statement)
        values = cur.fetchall()

        return False if len(values) == 0 else True

    def updateResponded(conn, empNumber, payRate, date, rNum):
        statement = f"""UPDATE Responded SET payRate = {payRate} WHERE empNumber = {empNumber} AND date = \'{date}\' AND runNumber = {rNum};"""
        cur = conn.cursor()
        cur.execute(statement)
        conn.commit()
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
        conn.commit()
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
        conn.commit()
        return cur.lastrowid
