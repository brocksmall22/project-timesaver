import sqlite3
from sqlite3 import Error

"""
This class is responsible for running all sql operations. It requires that it be enstantiated.
This class should be used in a `with` block. Follow the example below:
    ```
    with sqlFunctions("path/to/the/database") as object_name:
        # Calls to functions that depend on this class
        # or calls directly to this class will use
        # the object in this block.
    ```
Usage in this manor is required as it creates the connection, runs all needed actions,
and cleanly closes the object and connection to the db upon exiting the with scope.
"""
class sqlFunctions():
    def __init__(self, dbFile):
        self.conn = self.createConnection(dbFile)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.commit()
        self.conn.close()


    """
    createConnection(db_file)
    this creates the connection to the SQL database
    it requires the path to the Database
    """
    def createConnection(self, dbFile):
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
    createRun(self, runNumber, date, stopTime, endTime, runTime, Covered, Medrun, shift) 
    this is the general insertion of runs into the data base.
    it requires the runNumber, Date, StartTime, EndTime, Runtime,Bool for station covered, bool for Medrun, and the connextion to the sql database
    -------------------------------------------------------------------------------------------------------
    updateRun(self, num, date, startTime, endTime, runTime)
    this updates the run given that it has alredy been insterted into the database and has differing information then therun alredy has
     it requires the runNumber, Date, StartTime, EndTime, Runtime,Bool for station covered, bool for Medrun, and the connextion to the sql database
    -------------------------------------------------------------------------------------------------------
    runNeedsUpdated(self, num, date)
    this checks the runs alredy in the database against the given information to see if the run needs to be updatded
    it requires the Run number, date, and connection to the sql database
    """
    def createRun(self, runNumber, date, stopTime, endTime, runTime, Covered, Medrun, shift):
        sql = """ INSERT INTO Run(number, date, startTime, stopTime, runTime, Covered, Medrun, shift)
                VALUES({0},\'{1}\',{2},{3},{4}, {5}, {6}, \'{7}\') """
        cur = self.conn.cursor()
        sql = sql.format(runNumber, date, stopTime,
                         endTime, runTime, Covered, Medrun, shift)
        cur.execute(sql)
        return cur.lastrowid

    def updateRun(self, runNumber, date, startTime, endTime, runTime, Covered, Medrun, shift):
        statement = f"""UPDATE Run SET runTime = {runTime}, startTime = {startTime}, stopTime = {endTime}, Covered = {Covered}, Medrun = {Medrun}, shift = \'{shift}\' WHERE number = {runNumber} AND date = \'{date}\';"""
        cur = self.conn.cursor()
        cur.execute(statement)
        return cur.lastrowid

    def runNeedsUpdated(self, runNumber, date):
        statement = f"""SELECT * FROM Run WHERE Date = \'{date}\' AND number = {runNumber};"""
        cur = self.conn.cursor()
        cur.execute(statement)
        values = cur.fetchall()

        return False if len(values) == 0 else True

    """
    This Contains all of the SQL functions related to the Responded tabel
    -------------------------------------------------------------------------------------------------------
    createResponded(self, empNumber, payRate, date, num)
    this is the general insertion for the Responded Table
    it requires the connection to the SQL database as well as the Employee number, payrate, date of the run, and the run number
    -------------------------------------------------------------------------------------------------------
    respondedNeedsUpdated(self, empNumber, date, rNum)
    this is to check the responded table against the given information to see if the responded table needs to be updated 
    it requires the SQL Connection as well as Employee number, date of the run, and the run number
    -------------------------------------------------------------------------------------------------------
    updateResponded(self, empNumber, payRate, date, rNum)
    this is to update the responded table
    it requires the connection to the SQL database as well as the Employee number, payrate, date of the run, and the run number
    """
    def createResponded(self, empNumber, payRate, date, num):
        sql = """INSERT INTO Responded(empNumber, runNumber, date, payRate)
                VALUES({0},{1},\'{2}\',{3}) """
        cur = self.conn.cursor()
        sql = sql.format(empNumber, num, date, payRate)
        cur.execute(sql)
        return cur.lastrowid

    def respondedNeedsUpdated(self, empNumber, date, rNum):
        statement = f"""SELECT * FROM Responded WHERE Date = \'{date}\' AND empNumber = {empNumber} AND runNumber = {rNum};"""
        cur = self.conn.cursor()
        cur.execute(statement)
        values = cur.fetchall()

        return False if len(values) == 0 else True

    def updateResponded(self, empNumber, payRate, date, rNum):
        statement = f"""UPDATE Responded SET payRate = {payRate} WHERE empNumber = {empNumber} AND date = \'{date}\' AND runNumber = {rNum};"""
        cur = self.conn.cursor()
        cur.execute(statement)
        return cur.lastrowid
    """
    This Contains all of the SQL functions related to the Employee tabel
    -------------------------------------------------------------------------------------------------------
    createEmployee(self, name, empNumber)
    This is the insertion for the Employee table
    It requires the SQL connection as well as the name, and employee number
    -------------------------------------------------------------------------------------------------------
    empNeedsUpdated(self, empNumber)
    this checks the Employee table against the given information to see if it needs to be updated
    it rquires the SQL connection as well as the Employee number
    -------------------------------------------------------------------------------------------------------
    updateEmp(self, name ,empNumber)
    this updates the employee table given the new information
    it requires the SQL connection as well as the Employee Name and Number
    """
    def createEmployee(self, name, empNumber):
        sql = f""" INSERT INTO Employee(name,number)
                VALUES(\'{name}\',{empNumber}) """
        cur = self.conn.cursor()
        cur.execute(sql)
        return cur.lastrowid

    def empNeedsUpdated(self, empNumber):
        statement = f"""SELECT * FROM Employee WHERE number = {empNumber};"""
        cur = self.conn.cursor()
        cur.execute(statement)
        values = cur.fetchall()

        return False if len(values) == 0 else True

    def updateEmp(self, name, empNumber):
        statement = f"""UPDATE Employee SET name = \'{name}\' WHERE number = {empNumber};"""
        cur = self.conn.cursor()
        cur.execute(statement)
        return cur.lastrowid