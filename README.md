
# project-timesaver


This will be a markdown of documentation regarding Project Time Saver.
## Documentation from the  payroll.py file for the backend
### This is all for the looping through of the excel workbooks
loadWorkBooks(fileList)
    loops Through the fileList array and runs the readWorkBook on each file this is the main driver for the program
    This requires the whole file list
    It returns the retun array of the failed files or true if no files have failed

readWorkBook(wb, filename)
    reads an indiual work book then prints the resulting values from in the range of cells A21->F55
    It requires the Workbook and the Filename

getRange(wb)
    this function loops through the work book file
    it requires the work book file

getEmpinfo(conn, wb, date, rNum)
    This gets the Employee information from the wb file then it runs the employee and Responded SQL insertions
    It requires the SQL connection workbookFile and the Date and RunNumber from the getRunInfo

getRunInfo(conn, wb)
    This gets the Run info from the sheet and runs the SQL import statements
    it requires the SQL connection and the workbook file
    It retuns the Run Date and Number

### This is for the SQL insertions and updates for the backend
#### This contains all of the SQL functions related to Runs
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

#### This Contains all of the SQL functions related to the Responded tabel
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

#### This Contains all of the SQL functions related to the Employee tabel
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