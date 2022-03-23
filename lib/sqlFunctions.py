import sqlite3
from sqlite3 import Error
import os
from turtle import st

class sqlFunctions():
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
    
    def __init__(self,
                dbFile =  os.getenv('APPDATA') + "\\project-time-saver\\database.db"):
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
    TODO: Update this documentation
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

    def createRun(self, runNumber, date, startTime, endTime, runTime, covered,
                  medrun, shift, timestamp, fullCover, fsc, paid, oic, so,
                  filler, code1076, code1023, uc, code1008, workingHours, offHours,
                  apparatus, township, givenAid, takenAid, runType):
        sql = """INSERT INTO Run(number, date, startTime, stopTime, runTime, covered,
                Medrun, shift, timeStamp, full_coverage, fsc, paidRun, oic, so, filler,
                code1076, code1023, uc, code1008, workingHours, offHours,
                apparatus, township, givenAid, takenAid, runType) VALUES(?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) """
        params = [runNumber, date, startTime, endTime, runTime, covered, medrun,
                shift, timestamp, fullCover, fsc, paid, oic, so, filler, code1076,
                code1023, uc, code1008, workingHours, offHours, apparatus, township,
                givenAid, takenAid, runType]
        cur = self.conn.cursor()
        cur.execute(sql, params)
        return cur.lastrowid

    def updateRun(self, runNumber, date, startTime, endTime, runTime, covered,
                  medrun, shift, timestamp, fullCover, fsc, paid, oic, so,
                  filler, code1076, code1023, uc, code1008, workingHours, offHours,
                  apparatus, township, givenAid, takenAid, runType):
        statement = """UPDATE Run SET runTime = ?, startTime = ?, stopTime = ?, 
                    covered = ?, Medrun = ?, shift = ?, timeStamp = ?,
                    full_coverage = ?, fsc = ?, paidRun = ?, oic = ?, so = ?,
                    filler = ?, code1076 = ?, code1023 = ?, uc = ?, code1008 = ?,
                    workingHours = ?, offHours = ?, apparatus = ?, township = ?,
                    givenAid = ?, takenAid = ? WHERE number = ? AND date = ?
                    AND runType = ?;"""
        params = [runNumber, date, startTime, endTime, runTime, covered, medrun,
                shift, timestamp, fullCover, fsc, paid, oic, so, filler, code1076,
                code1023, uc, code1008, workingHours, offHours, apparatus, township,
                givenAid, takenAid, runType]
        cur = self.conn.cursor()
        cur.execute(statement, params)
        return cur.lastrowid

    def newRunNeedsUpdated(self, runNumber, Timestamp, Year):
        statement = """SELECT * FROM Run WHERE timeStamp < ?
                    AND number = ? AND date >= ?;"""
        params = [Timestamp, runNumber, Year]
        cur = self.conn.cursor()
        cur.execute(statement, params)
        values = cur.fetchall()

        return False if len(values) == 0 else True

    def checkIfExists(self, runNumber, year):
        statement = f"""SELECT * FROM Run WHERE Date >= ? AND number = ?;"""
        params = [year, runNumber]
        cur = self.conn.cursor()
        cur.execute(statement, params)
        values = cur.fetchall()

        return False if len(values) == 0 else True

    """
    This Contains all of the SQL functions related to the Responded table
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

    def createResponded(self, empNumber, payRate, date, num, type_of_response,
                        full_time, subhours):
        sql = """INSERT INTO Responded(empNumber, runNumber, date, payRate,
                type_of_response, full_time, subhours) VALUES(?, ?, ?, ?,
                ?, ?, ?) """
        params = [empNumber, num, date, payRate, type_of_response,
                full_time, subhours]
        cur = self.conn.cursor()
        cur.execute(sql, params)
        return cur.lastrowid

    def respondedNeedsUpdated(self, empNumber, date, rNum):
        statement = """SELECT * FROM Responded WHERE Date = ?
                    AND empNumber = ? AND runNumber = ?;"""
        params = [date, empNumber, rNum]
        cur = self.conn.cursor()
        cur.execute(statement, params)
        values = cur.fetchall()

        return False if len(values) == 0 else True

    def updateResponded(self, empNumber, payRate, date, rNum, type_of_response,
                        full_time, subhours):
        statement = """UPDATE Responded SET payRate = ? WHERE empNumber = ?
                    AND date = ? AND runNumber = ? AND type_of_response = ?,
                    full_time = ?, subhours = ?;"""
        params = [payRate, empNumber, date, rNum, type_of_response, full_time, subhours]
        cur = self.conn.cursor()
        cur.execute(statement, params)
        return cur.lastrowid

    """
    This Contains all of the SQL functions related to the Employee table
    -------------------------------------------------------------------------------------------------------
    createEmployee(self, name, empNumber)
    This is the insertion for the Employee table
    It requires the SQL connection as well as the name, and employee number
    -------------------------------------------------------------------------------------------------------
    empNeedsUpdated(self, empNumber)
    this checks the Employee table against the given information to see if it needs to be updated
    it requires the SQL connection as well as the Employee number
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

    """
    Get the count of runs a specific employee has responded to in a specific period.

    inputs..
        start_date: the start of the period
        end_date: the end of the period
        empNum: the department employee ID
    returns..
        An int containing the number of runs
    """

    def getCountOfRunsForEmployeeBetweenDates(self, start_date, end_date,
                                              empNum):
        cur = self.conn.cursor()
        return cur.execute(f"""SELECT COUNT(*) FROM Run where number = (
                    SELECT runNumber FROM Responded WHERE date 
                    BETWEEN \'{start_date}\' AND \'{end_date}\' 
                    AND empNumber = {empNum}) AND Medrun = 0""").fetchall(
        )[0][0]

    """
    Get the total hours a specific employee is being paid for.

    inputs..
        start_date: the start of the period
        end_date: the end of the period
        empNumber: the department employee ID
    returns..
        An int containing the number of hours
    """

    def getSumOfHoursForEmployeeBetweenGivenDates(self, start_date, end_date,
                                                  empNumber):
        cur = self.conn.cursor()
        return cur.execute(
            f"""SELECT SUM(runTime) FROM Run WHERE number = (SELECT runNumber FROM Responded WHERE type_of_response = 'P' AND empNumber = {empNumber} AND date BETWEEN \'{start_date}\' AND \'{end_date}\') AND Medrun = 0;"""
        ).fetchall()[0][0]

    """
    Get an ordered list of runs in a given range of dates.

    inputs..
        start_date: the start of the period
        end_date: the end of the period
    returns..
        A list of tuples containing one run number each like `(run number)`
    """

    def getOrderedRunsBetweenTwoDates(self, start_date, end_date):
        cur = self.conn.cursor()
        return cur.execute(f"""SELECT DISTINCT number FROM Run WHERE 
                    date BETWEEN \'{start_date}\' AND \'{end_date}\' ORDER BY number;"""
                           ).fetchall()

    """
    This method gets the number of runs for a given period.

    inputs..
        start_date: the first date as a string
        end_date: the last date as a string
    returns..
        case 1: the number of runs
    """

    def getNumberOfRuns(self, start_date, end_date):
        cur = self.conn.cursor()
        return cur.execute(
            f"""SELECT COUNT(number) FROM Run WHERE date BETWEEN \'{start_date}\' AND \'{end_date}\';"""
        ).fetchall()[0][0]

    """
    This method gets the lowest run number for a given period.

    inputs..
        start_date: the first date as a string
        end_date: the last date as a string
    returns..
        case 1: the first run
    """

    def getFirstRunNumber(self, start_date, end_date):
        cur = self.conn.cursor()
        return cur.execute(
            f"""SELECT MIN(number) FROM Run WHERE date BETWEEN \'{start_date}\' AND \'{end_date}\';"""
        ).fetchall()[0][0]

    """
    This method gets the highest run number for a given period.

    inputs..
        start_date: the first date as a string
        end_date: the last date as a string
    returns..
        case 1: the last run
    """

    def getLastRunNumber(self, start_date, end_date):
        cur = self.conn.cursor()
        return cur.execute(
            f"""SELECT MAX(number) FROM Run WHERE date BETWEEN \'{start_date}\' AND \'{end_date}\';"""
        ).fetchall()[0][0]

    """
    This method gets the employee number and run number of every responded entry in the table between two dates.
    The full_time bool is used to get full time responded or paid on call responded.

    inputs..
        ft: True for full time, False for paid on call
        start_date: the date for the beginning of a period
        end_date: the date for the end of a period
    returns..
        A list of tuples like `(employee_number, run_number)`
    """

    def getEAndRNumbersFromRespondedBasedOnFullTimeBetweenDates(
            self, ft, start_date, end_date):
        cur = self.conn.cursor()
        return cur.execute(
            f"""SELECT empNumber, runNumber FROM Responded WHERE full_time = {int(ft)} AND date BETWEEN '{start_date}' AND '{end_date}';"""
        ).fetchall()

    """
    This method gets the Medrun bit for a given run.

    inputs..
        run_number: the number of the run
    returns..
        An int, 1 for a med run, or 0 for a fire run
    """

    def getMedRunBitFromRun(self, run_number):
        cur = self.conn.cursor()
        return cur.execute(
            f"""SELECT Medrun FROM Run WHERE number = {run_number};"""
        ).fetchall()[0][0]

    """
    This method gets the FSC bit for a given run.

    inputs..
        run_number: the number of the run
    returns..
        An int, 1 for a FSC run, or 0 for a standard run
    """

    def getFscBitFromRun(self, run_number):
        cur = self.conn.cursor()
        return cur.execute(
            f"""SELECT fsc FROM Run WHERE number = {run_number};""").fetchall(
            )[0][0]

    """
    Gets the name of an employee from the employee number.

    inputs..
        employee_number: the fire department internal employee ID
    returns..
        A string containing a name
    """

    def getNameOfEmployeeBasedOnNumber(self, employee_number):
        cur = self.conn.cursor()
        return cur.execute(
            f"""SELECT name FROM Employee WHERE number = {employee_number}"""
        ).fetchall()[0][0]

    """
    Gets the count of med runs for a given shift between two dates.

    inputs..
        shift: a string containing the shift
        start_date: the beginning date
        end_date: the end date
    returns..
        An integer indicating the number of runs
    """

    def getCountShiftMedRunsBetweenDates(self, shift, start_date, end_date):
        cur = self.conn.cursor()
        return cur.execute(
            f"""SELECT COUNT(*) FROM Run WHERE Shift = '{shift}' AND Medrun = 1 AND date BETWEEN '{start_date}' and '{end_date}';"""
        ).fetchall()[0][0]

    """
    Gets the count of FSC runs for a given shift between two dates.

    inputs..
        shift: a string containing the shift
        start_date: the beginning date
        end_date: the end date
    returns..
        An integer indicating the number of FSC runs
    """

    def getCountShiftFscRunsBetweenDates(self, shift, start_date, end_date):
        cur = self.conn.cursor()
        return cur.execute(
            f"""SELECT COUNT(*) FROM Run WHERE Shift = '{shift}' AND fsc = 1 AND date BETWEEN '{start_date}' and '{end_date}';"""
        ).fetchall()[0][0]

    """
    Gets the number of runs for a given shift that the station was not covered during the run.

    inputs..
        shift: a string containing the shift
        start_date: the beginning date
        end_date: the end date
    returns..
        An integer indicating the number of runs
    """

    def getCountShiftNotCoveredRunsBetweenDates(self, shift, start_date,
                                                end_date):
        cur = self.conn.cursor()
        return cur.execute(
            f"""SELECT COUNT(*) FROM Run WHERE Shift = '{shift}' AND Covered = 0 AND Medrun = 0 AND date BETWEEN '{start_date}' and '{end_date}';"""
        ).fetchall()[0][0]

    """
    Gets the number of runs for a given shift that every employee for the shift responded.

    inputs..
        shift: a string containing the shift
        start_date: the beginning date
        end_date: the end date
    returns..
        An integer indicating the number of runs
    """

    def getCountShiftFullyCoveredRunsBetweenDates(self, shift, start_date,
                                                  end_date):
        cur = self.conn.cursor()
        return cur.execute(
            f"""SELECT COUNT(*) FROM Run WHERE Shift = '{shift}' AND full_coverage = 1 AND Medrun = 0 AND date BETWEEN '{start_date}' and '{end_date}';"""
        ).fetchall()[0][0]

    """
    Gets the number of runs for a given shift that are fire runs.

    inputs..
        shift: a string containing the shift
        start_date: the beginning date
        end_date: the end date
    returns..
        An integer indicating the number of runs
    """

    def getCountShiftFireRunsBetweenDates(self, shift, start_date, end_date):
        cur = self.conn.cursor()
        return cur.execute(
            f"""SELECT COUNT(*) FROM Run WHERE Shift = '{shift}' AND Medrun = 0 AND date BETWEEN '{start_date}' and '{end_date}';"""
        ).fetchall()[0][0]

    """
    Gets the date and the start time of all fire runs for a given shift between two dates.

    inputs..
        shift: a string containing the shift
        start_date: the beginning date
        end_date: the end date
    returns..
        A list of tuples containing the date and start time like `(date, start_time)`
    """

    def getDateAndStartOfFireRunsBetweenDatesForShift(self, shift, start_date,
                                                      end_date):
        cur = self.conn.cursor()
        return cur.execute(
            f"""SELECT date, startTime FROM Run WHERE Shift = '{shift}' AND Medrun = 0 AND date BETWEEN 
            '{start_date}' and '{end_date}';""").fetchall()

    def getCountOfAllPaidRunsByCityNumberBetweenDates(self, start_date,
                                                      end_date, city_number):
        """
        Gets the total number of paid runs an employee responded to.

        inputs..
            start_date: the beginning date
            end_date: the end date
            city_number: the city ID number of an employee
        returns..
            A number that is the total number of runs
        """
        cur = self.conn.cursor()
        return cur.execute(
            f"""select count(*) from run where number in (select runNumber from Responded where 
            empNumber = (select number from employee where city_number = {city_number}) 
            and date between '{start_date}' and '{end_date}') and medrun = 0;"""
        ).fetchall()[0][0]

    def getAllPaidHoursForEmployeeByCityNumberBetweenDates(
            self, city_number, start_date, end_date):
        """
        Gets the total number of paid hours for a given employee during a given period.

        inputs..
            start_date: the beginning date
            end_date: the end date
            city_number: the city ID number of an employee
        returns..
            An number containing the number of paid hours
        """
        cur = self.conn.cursor()
        return cur.execute(
            f"""select sum(runTime) from run where number in (select runNumber from Responded where 
            empNumber = (select number from employee where city_number = {city_number}) and type_of_response = 'P' 
            and date between '{start_date}' and '{end_date}') and paidRun = 1;"""
        ).fetchall()[0][0]

    def getAllSubHoursForEmployeeByCityNumberBetweenDates(
            self, city_number, start_date, end_date):
        """
        Gets the total number of hours to subtract for a given employee during a given period.

        inputs..
            start_date: the beginning date
            end_date: the end date
            city_number: the city ID number of an employee
        returns..
            An number containing the number of subtracted hours
        """
        cur = self.conn.cursor()
        return cur.execute(
            f"""select sum(subhours) from Responded where empNumber = (select number 
            from employee where city_number = {city_number}) and type_of_response = 'P' 
            and date between '{start_date}' and '{end_date}';""").fetchall(
            )[0][0]

    """
    Gets the length of any given run that is a fire run.

    inputs..
        run_number: the id number for a run
    returns..
        A float that contains the length of the run
    """

    def getRunTimeOfFireRunByRunNumber(self, run_number):
        cur = self.conn.cursor()
        return cur.execute(
            f"""SELECT runTime FROM Run WHERE number = {run_number} AND Medrun = 0 AND fsc = 0;"""
        ).fetchall()

    """
    Gets the inter department number and the name of every employee
    that does not yet have a city ID attached to them.

    returns..
        A list of tuples that contains the internal number and name like `(employee number, employee name)`
    """

    def getNumberAndNameOfAllEmployeesWithNoCityNumver(self):
        cur = self.conn.cursor()
        return cur.execute(
            """SELECT number, name FROM Employee where city_number is NULL;"""
        ).fetchall()

    """
    Updates a given employee with a city ID number.

    inputs..
        city_number: the city ID number
        employee_number: the internal department ID number
    """

    def addCityNumberToEmployee(self, city_number, employee_number):
        cur = self.conn.cursor()
        cur.execute(
            f"""UPDATE Employee SET city_number = {city_number} WHERE number = {employee_number};"""
        )
        self.conn.commit()

    """
    Returns the maximum run from the database in the current year.

    inputs..
        date: the first of the year as a string in the format Y-m-d 
    """

    def getMostRecentRun(self, date):
        cur = self.conn.cursor()
        return cur.execute(
            f"""SELECT MAX(number) FROM Run where date >= {date};""").fetchall(
            )[0][0]

    """
    Returns if there are runs between two dates.

    inputs..
        start_date: the start of the period
        end_date: the end of the period
    returns..
        True if there are runs between those dates
        Falsd if there are not
    """

    def checkForRunsBetweenDates(self, start_date, end_date):
        cur = self.conn.cursor()
        return not len(
            cur.execute(
                f"""SELECT * FROM Run WHERE date BETWEEN '{start_date}' AND '{end_date}';"""
            ).fetchall()) == 0


    def getStartTimeOfRuns(self, start_date, end_date):
        """
        Gets the start time for every run in a given period.

        inputs..
            start_date: the start of the period
            end_date: the end of the period
        returns..
            A list of tuples containing the start time
                for each run.
        """
        sql = """SELECT startTime FROM Run WHERE date BETWEEN ? AND ?;"""
        params = [start_date, end_date]
        cur = self.conn.cursor()
        return cur.execute(sql, params).fetchall()


    def getTownshipOfRuns(self, start_date, end_date):
        """
        Gets the township and if it is in the city
        for every run in a given period.

        inputs..
            start_date: the start of the period
            end_date: the end of the period
        returns..
            A list of tuples containing the township and
                if it is in the city for each run.
        """
        sql = """SELECT township FROM Run WHERE date BETWEEN ? AND ?;"""
        params = [start_date, end_date]
        cur = self.conn.cursor()
        return cur.execute(sql, params).fetchall()

    def getApparatusOfRuns(self, start_date, end_date):
        """
        Gets all of the appararus used during each run.

        inputs..
            start_date: the start of the period
            end_date: the end of the period
        returns..
            A list of tuples containing the apparatus used.
        """
        sql = """SELECT apparatus FROM Run WHERE date BETWEEN ? AND ?;"""
        params = [start_date, end_date]
        cur = self.conn.cursor()
        return cur.execute(sql, params).fetchall()

    def getGivenAid(self, start_date, end_date):
        """
        Gets the departments that revieced this station's aid
        as well as the type of aid.

        inputs..
            start_date: the start of the period
            end_date: the end of the period
        returns..
            A list of tuples containing the department
                and the type of aid given.
        """
        sql = """SELECT givenAid FROM Run WHERE date BETWEEN ? AND ?;"""
        params = [start_date, end_date]
        cur = self.conn.cursor()
        return cur.execute(sql, params).fetchall()


    def getTakenAid(self, start_date, end_date):
        """
        Gets the departments that provided this station aid
        as well as the type of aid.

        inputs..
            start_date: the start of the period
            end_date: the end of the period
        returns..
            A list of tuples containing the department
                and the type of aid recieved.
        """
        sql = """SELECT takenAid FROM Run WHERE date BETWEEN ? AND ?;"""
        params = [start_date, end_date]
        cur = self.conn.cursor()
        return cur.execute(sql, params).fetchall()


    def getRunTypes(self, start_date, end_date):
        """
        Gets the types of run that apply to the runs
        for the given period.

        inputs..
            start_date: the start of the period
            end_date: the end of the period
        returns..
            A list of tuples containing the types of runs
        """
        sql = """SELECT runType FROM Run WHERE date BETWEEN ? AND ?;"""
        params = [start_date, end_date]
        cur = self.conn.cursor()
        return cur.execute(sql, params).fetchall()


    def getShiftCoverages(self, start_date, end_date):
        """
        Gets the shift responding to a run as well as
        whether that shift was fully covered (all
        employees of that shift responded).

        inputs..
            start_date: the start of the period
            end_date: the end of the period
        returns..
            A list of tuples containing the shift as
                as if it was covered
        """
        sql = """SELECT shift, full_coverage FROM Run
                WHERE date BETWEEN ? AND ?;"""
        params = [start_date, end_date]
        cur = self.conn.cursor()
        return cur.execute(sql, params).fetchall()


    def getTotalNumberOfRunsDuringPeriod(self, start_date, end_date):
        """
        Gets the sum of all runs in a given period.

        inputs..
            start_date: the start of the period
            end_date: the end of the period
        returns..
            An integer representing the total
        """
        sql = """SELECT COUNT(*) FROM Run
                WHERE date BETWEEN ? AND ?;"""
        params = [start_date, end_date]
        cur = self.conn.cursor()
        return cur.execute(sql, params).fetchall()[0][0]