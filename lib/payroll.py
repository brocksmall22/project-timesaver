from io import RawIOBase
import os
from openpyxl import load_workbook
import sqlite3
from sqlite3 import Error

class payroll:

    database = r"C://sqlite/RunReportDB"
    returnArray = []
    endRange = 0

    
    # This is here for testing purposes
    def getfilelist(fileString):
        fileList = fileString.split(" ")
        return fileList


    # loops Through the fileList array and runs the readWorkBook on each file
    def loadWorkBooks(fileList):
        for file in fileList:
            print(file)
            wb = load_workbook(file)

            payroll.readWorkBook(wb, file)

        if len(payroll.returnArray) == 0:
            return [True]
        else:
            return payroll.returnArray


    # reads an indiual work book then prints the resulting values from in the range of cells A21->F55
    # issues with
    def readWorkBook(wb, filename):
        conn = payroll.create_connection(os.getenv('APPDATA') + "\\project-time-saver\\database.db")
        try:

            payroll.getRange(wb)

            date, rNum = payroll.getRunInfo(conn, wb)

            payroll.getEmpinfo(conn, wb, date, rNum)
        except Exception as e:
            print(e)
            payroll.returnArray.append(filename)

        conn.close


    # Gets the final A cell with an employee number
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


    # this gets and returns the pay rate and employee number for those on run
    def getEmpinfo(conn, wb, date, rNum):
        sheet = wb.active
        for i1 in sheet[f"A21:h{payroll.endRange}"]:

            if i1[5].value == 1:

                empNumber = wb["Pay"][i1[0].value.split("!")[1]].value
                print("Emp Num: " + str(empNumber))
                payRate = wb["Pay"][i1[7].value.split("!")[1]].value
                print("PayRate: " + str(payRate))
                if payroll.respondedNeedsUpdated(conn, empNumber, date, rNum):
                    payroll.updateResponded(conn, empNumber, payRate, date, rNum)
                else:
                    payroll.create_responded(conn, empNumber, payRate, date, rNum)


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


    # this is no longer needed only here for reference at this time
    def getPayRate(wb):
        sheet = wb.active
        for i1 in sheet[f"F21:H{payroll.endRange}"]:

            if i1[0].value == 1:

                returnSting = wb["Pay"][i1[2].value.split("!")[1]].value
                print("PayRate: " + str(returnSting))


    # gets all run info from the specific cells
    def getRunInfo(conn, wb):
        sheet = wb.active
        date = str(sheet["D3"].value).split(" ")[0]
        num = sheet["B3"].value
        runTime = sheet["B8"].value
        startTime = sheet["B5"].value
        endTime = sheet["L5"].value
        returnString = (
            "RunNumber: {0} \nDate: \'{1}\' \nRunTime: {2} \nStartTime: {3} \nEndtime: {4}"
        )
        if payroll.runNeedsUpdated(conn, num, date):
            payroll.updateRun(conn, num, date, startTime, endTime, runTime)
        else:
            payroll.create_run(conn, num, date, startTime, endTime, runTime)
            print(returnString.format(num, date, runTime, startTime, endTime))
        return date, num


    def runNeedsUpdated(conn, num, date):
        statement = f"""SELECT * FROM Run WHERE Date = \'{date}\' AND number = {num};"""
        cur = conn.cursor()
        cur.execute(statement)
        values = cur.fetchall()

        return False if len(values) == 0 else True


    def updateRun(conn, num, date, startTime, endTime, runTime):
        statement = f"""UPDATE Run SET runTime = {runTime}, startTime = {startTime}, stopTime = {endTime} WHERE number = {num} AND date = \'{date}\';"""
        cur = conn.cursor()
        cur.execute(statement)
        conn.commit()
        return cur.lastrowid


    # database connection
    def create_connection(db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            print(e)
        return conn


    # inserting rows to different tables
    def create_employee(conn, employee):
        sql = """ INSERT INTO Employee(name,number)
                VALUES(?,?) """
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        return cur.lastrowid


    def create_run(conn, num, date, sTime, eTime, rTime):
        sql = """ INSERT INTO Run(number, date, startTime, stopTime, runTime)
                VALUES({0},\'{1}\',{2},{3},{4}) """
        cur = conn.cursor()
        sql = sql.format(num, date, sTime, eTime, rTime)
        print(sql)
        cur.execute(sql)
        conn.commit()
        return cur.lastrowid


    def create_responded(conn, empNumber, payRate, date, num):
        sql = """ INSERT INTO Responded(empNumber, runNumber, date, payRate)
                VALUES({0},{1},\'{2}\',{3}) """
        cur = conn.cursor()
        sql = sql.format(empNumber, num, date, payRate)
        print(sql)
        cur.execute(sql)
        conn.commit()
        return cur.lastrowid

    

    # ----------------------------------------------------------
    # this main is purely for testing and will be removed later
    def main():
        print("ENTER .XLSX FILE PATH:")
        payroll.loadWorkBooks(payroll.getfilelist(input()))


    if __name__ == "__main__":
        main()
    # ----------------------------------------------------------
