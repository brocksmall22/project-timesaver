
from openpyxl import load_workbook

class generate_report:

    def loadWorkBooks(fileList):
        for file in fileList:
            print(file)
            wb = load_workbook(file)
            generate_report.readWorkBook(wb, file)

    def getRange(wb):
        end = False
        sheet = wb.active
        if generate_report.endRange == 0:
            generate_report.endRange = 8
            while (not end):
                if sheet[f"C{generate_report.endRange + 1}"].value != None:
                    generate_report.endRange = generate_report.endRange + 1
                else:
                    end = True

    def match_names(name, fname, lname):
        if name[0:4] == "Lt. ":
             name = name[4:]
        elif name[0:6] == "Capt. ":
            name = name[6:]
        if name[-1].isnumeric():
            if name[-2].isnumeric():
                 name = name[0:-6]
            else:
                name = name[0:-5]

        if name == f"{fname[0]}. {lname}":
            return True
        else:
             return False

    def update(conn, number, city_number, date, empNumber):
        statement = f"""SELECT number FROM Employee WHERE city_number = {city_number}; SELECT date, runNumber FROM Responded WHERE empNumber = {empNumber}; 
    SELECT runTime FROM Run WHERE date = \'{date}\' AND number = {number}; UPDATE Employee SET city_number = {city_number} WHERE number = {number}; 
    SELECT name FROM Employee WHERE number = {number};"""
        cur = conn.cursor()
        cur.execute(statement)
        conn.commit()
        return cur.lastrowid