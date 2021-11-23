import sqlite3
from sqlite3 import Error

class sqlFunctions:
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
    def createRun(conn, runNumber, date, stopTime, endTime, runTime, Covered, Medrun, shift):
        sql = """ INSERT INTO Run(number, date, startTime, stopTime, runTime, Covered, Medrun, shift)
                VALUES({0},\'{1}\',{2},{3},{4}, {5}, {6}, \'{7}\') """
        cur = conn.cursor()
        sql = sql.format(runNumber, date, stopTime,
                         endTime, runTime, Covered, Medrun, shift)
        cur.execute(sql)
        return cur.lastrowid

    def updateRun(conn, runNumber, date, startTime, endTime, runTime, Covered, Medrun, shift):
        statement = f"""UPDATE Run SET runTime = {runTime}, startTime = {startTime}, stopTime = {endTime}, Covered = {Covered}, Medrun = {Medrun}, shift = \'{shift}\' WHERE number = {runNumber} AND date = \'{date}\';"""
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
    def createResponded(conn, empNumber, payRate, date, num):
        sql = """INSERT INTO Responded(empNumber, runNumber, date, payRate)
                VALUES({0},{1},\'{2}\',{3}) """
        cur = conn.cursor()
        sql = sql.format(empNumber, num, date, payRate)
        cur.execute(sql)
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