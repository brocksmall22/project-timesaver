
from openpyxl import load_workbook
from os import getenv, stat
from lib.payroll import payroll

class generate_report:

    endRange = 0
    """
    This function is responsible for being called from the API, running all the
    generation steps, and returning a confirmation or fail message.

    inputs..
        start_date: the first date as a string
        end_date: the last date as a string
    returns..
        case 1: a list containing True in the first position followed be some
            strings with basic details about the report
        case 2: an error message to be displayed to the user
    """
    def generate_report(start_date, end_date):
        conn = payroll.createConnection(getenv('APPDATA') + "\\project-time-saver\\database.db")
        try:
            wb = load_workbook(getenv('APPDATA') + "\\project-time-saver\\base.xlsx")
            sheet = wb["Sheet1"]
            generate_report.getRange(sheet)
            generate_report.update_employee_nulls(conn, sheet)
            generate_report.fill_sheet(conn, wb, start_date, end_date)
            number_of_runs = generate_report.get_number_of_runs(conn, start_date, end_date)
            min_run = generate_report.get_first_run_number(conn, start_date, end_date)
            max_run = generate_report.get_last_run_number(conn, start_date, end_date)

        except Exception as e:
            conn.close
            print(e)
            return [str(e)]
        conn.close
        return [True, f"The generated pay period is from {start_date} to {end_date}.",
            f"There were {number_of_runs} runs total this period.", f"This includes runs from run {min_run} to run {max_run}."]

    """
    This method gets the number of runs for a given period.

    inputs..
        conn: the connection to the SQL
        start_date: the first date as a string
        end_date: the last date as a string
    returns..
        case 1: the number of runs
    """
    def get_number_of_runs(conn, start_date, end_date):
        cur = conn.cursor()
        return cur.execute(f"""SELECT COUNT(number) FROM Run WHERE date BETWEEN \'{start_date}\' AND \'{end_date}\';""").fetchall()[0][0]

    """
    This method gets the lowest run number for a given period.

    inputs..
        conn: the connection to the SQL
        start_date: the first date as a string
        end_date: the last date as a string
    returns..
        case 1: the first run
    """
    def get_first_run_number(conn, start_date, end_date):
        cur = conn.cursor()
        return cur.execute(f"""SELECT MIN(number) FROM Run WHERE date BETWEEN \'{start_date}\' AND \'{end_date}\';""").fetchall()[0][0]


    """
    This method gets the highest run number for a given period.

    inputs..
        conn: the connection to the SQL
        start_date: the first date as a string
        end_date: the last date as a string
    returns..
        case 1: the last run
    """
    def get_last_run_number(conn, start_date, end_date):
        cur = conn.cursor()
        return cur.execute(f"""SELECT MAX(number) FROM Run WHERE date BETWEEN \'{start_date}\' AND \'{end_date}\';""").fetchall()[0][0]

    """
    This method actually fills and saves a copy of the master copy of the tally sheet.

    inputs..
        conn: the connection to the SQL
        wb: the xlsx workbook we are working with
        start_date: the first date as a string
        end_date: the last date as a string
    """
    def fill_sheet(conn, wb, start_date, end_date):
        sheet = wb["Sheet1"]
        for i in range(8, generate_report.endRange + 1):
            city_number = sheet[f"A{i}"].value
            if city_number is not None:
                city_number = int(city_number)
                hours = generate_report.get_hours(conn, city_number, start_date, end_date)
                count = generate_report.get_count(conn, city_number, start_date, end_date)
                sheet[f"D{i}"].value = count
                sheet[f"E{i}"].value = hours
            else:
                sheet[f"D{i}"].value = 0
                sheet[f"E{i}"].value = 0
        wb.save(getenv("APPDATA") + "\\project-time-saver\\tally.xlsx")


    """
    This method gets the number of runs a specific person
    responded to in a given period.

    inputs..
        conn: the connection to the SQL
        city_number: the city assigned employee ID
        start_date: the first date as a string
        end_date: the last date as a string
    returns..
        case 1: the number of runs in a given period
    """
    def get_count(conn, city_number, start_date, end_date):
        cur = conn.cursor()
        sql = f"""SELECT COUNT(runNumber) FROM Responded WHERE empNumber = (SELECT number FROM Employee WHERE city_number = {city_number}) 
            AND date BETWEEN \'{start_date}\' AND \'{end_date}\';"""
        return cur.execute(sql).fetchall()[0][0]

    """
    This method gets the number of hours a specific person
    worked on runs in a given period.

    inputs..
        conn: the connection to the SQL
        city_number: the city assigned employee ID
        start_date: the first date as a string
        end_date: the last date as a string
    returns..
        case 1: the number of hours a given employee worked
    """
    def get_hours(conn, city_number, start_date, end_date):
        cur = conn.cursor()
        total = 0
        runs = cur.execute(f"""SELECT runNumber FROM Responded WHERE empNumber = 
            (SELECT number FROM Employee WHERE city_number = {city_number}) AND date BETWEEN \'{start_date}\' AND \'{end_date}\';""").fetchall()
        for run in runs:
            hour = cur.execute(f"""SELECT runTime FROM Run WHERE number = {run[0]}""").fetchall()
            if hour is not None:
                total += hour[0][0]
        return total

    """
    This method updates the Employee table to ensure no employees have a NULL
    value in the city_number column. If they do they will not be paid.

    inputs..
        conn: the connection to the SQL
        sheet: the sheet for the tally xlsx
    """
    def update_employee_nulls(conn, sheet):
        getNulls = """SELECT number, name FROM Employee where city_number is NULL;"""
        cur = conn.cursor()
        nullEmps = cur.execute(getNulls)
        generate_report.insert_city_ids(conn, nullEmps, sheet)

    """
    This method actually inserts the city IDs for update_employee_nulls

    inputs..
        conn: the connection to the SQL
        nullEmps: a list of employee rows that have null city_number values 
        sheet: the sheet for the tally xlsx
    """
    def insert_city_ids(conn, nullEmps, sheet):
        cur = conn.cursor()
        for emp in nullEmps:
            for i in range(8, generate_report.endRange + 1):
                if generate_report.match_names(emp[1], sheet[f"B{i}"].value, sheet[f"C{i}"].value):
                    update_string = f"""UPDATE Employee SET city_number = {sheet[f"A{i}"].value} WHERE number = {emp[0]};"""
                    cur.execute(update_string)
                    conn.commit()
                    break
        return cur.lastrowid


    """
    This method gets the final row that we are concerned with editing.

    inputs..
        sheet: the sheet for the tally xlsx
    """
    def getRange(sheet):
        end = False
        if generate_report.endRange == 0:
            generate_report.endRange = 8
            while (not end):
                if sheet[f"C{generate_report.endRange + 1}"].value != None:
                    generate_report.endRange = generate_report.endRange + 1
                else:
                    end = True

    """
    This method will take a name from the run reports and compare it to
    a name in the tally xlsx in order to determine if they are the same
    person.

    inputs..
        name: the name from the run report/responded table
        fname: the first name from the tally
        lname: the last name from the tally
    returns..
        case 1: True if they are the same person
        case 2: False if they aren't the same person
    """
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