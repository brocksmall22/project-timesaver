from openpyxl import load_workbook
import sqlite3
from sqlite3 import Error

database = r"C://sqlite/RunReportDB"
fileList = []
returnArray = []



# returns the file list as an array using " "as a seperator between file names
# most likley will be deprecated in the future mainly used for testing


def getfilelist(fileString):
    fileList = fileString.split(" ")
    return fileList


# loops Through the fileList array and runs the readWorkBook on each file


def loadWorkBooks(fileList):
    for file in fileList:
        print(file)
        wb = load_workbook(file)
        readWorkBook(wb)


# reads an indiual work book then prints the resulting values from in the range of cells A21->F55
# issues with


def readWorkBook(wb):

    date,rNum = getRunInfo(wb)

    getEmpinfo(wb,date,rNum)


# this gets and returns the pay rate and employee number for those on run
def getEmpinfo(wb,date,rNum):
    sheet = wb.active
    for i1 in sheet["A21:h55"]:

        if i1[5].value == 1:

            empNumber = wb["Pay"][i1[0].value.split("!")[1]].value
            print("Emp Num: " + str(empNumber))
            payRate = wb["Pay"][i1[7].value.split("!")[1]].value
            print("PayRate: " + str(payRate))
            create_responded(0,empNumber,payRate,date,rNum)


# this is no longer needed only here for reference at this time
def getPayRate(wb):
    sheet = wb.active
    for i1 in sheet["F21:H55"]:

        if i1[0].value == 1:

            returnSting = wb["Pay"][i1[2].value.split("!")[1]].value
            print("PayRate: " + str(returnSting))


# gets all run info from the specific cells
def getRunInfo(wb):
    sheet = wb.active
    date = sheet["D3"].value
    num = sheet["B3"].value
    runTime = sheet["B8"].value
    startTime = sheet["B5"].value
    endTime = sheet["L5"].value
    returnString = (
        "RunNumber: {0} \nDate: {1} \nRunTime: {2} \nStartTime: {3} \nEndtime: {4}"
    )
    print(returnString.format(num, date, runTime, startTime, endTime))
    create_run(0,num,date,startTime,endTime,runTime)
    return date, num 


#database connection
def create_connection():
    conn = None
    try:
        conn = sqlite3.connect(database)
    except Error as e:
        print(e)
    return conn

#inserting rows to different tables
def create_employee(conn, employee):
    sql = ''' INSERT INTO Employee(name,number)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, employee)
    conn.commit()
    return cur.lastrowid

def create_run(conn,num,date,sTime,eTime,rTime):
    sql = ''' INSERT INTO Run(number, date, startTime, stopTime, runTime)
              VALUES({0},{1},{2},{3},{4}) '''
    #cur = conn.cursor()
    sql = sql.format(num,date,sTime,eTime,rTime)
    print(sql)
    #cur.execute(sql)
    #conn.commit()
    #return cur.lastrowid

def create_responded(conn,empNumber,payRate,date,num):
    sql = ''' INSERT INTO Responded(empNumber, runNumber, date, payRate)
              VALUES({0},{1},{2},{3}) '''
    #cur = conn.cursor()
    sql = sql.format(empNumber,num,date,payRate)
    print(sql)
    #cur.execute())
    #conn.commit()
    #return cur.lastrowid

#----------------------------------------------------------
# this main is purely for testing and will be removed later
def main():
    loadWorkBooks(getfilelist(input()))


if __name__ == "__main__":
    main()
#----------------------------------------------------------