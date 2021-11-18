from openpyxl import load_workbook
from os import getenv
from lib.payroll import payroll

class generate_report:
    # TODO: Change the storage location of the generated files.
    # TODO: Change the path where the blank tally and blank shift
    # breakdowns are stored.
    # TODO: Generate the shift summary output
    # TODO: Separate out all of the SQL, general refactoring
    endPaidOnCall = 0
    startFullTime = 0
    endFullTime = 0
    cannotMatch = []
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
        generate_report.reset()
        conn = payroll.createConnection(getenv('APPDATA') + "\\project-time-saver\\database.db")
        try:
            wb = load_workbook(getenv('APPDATA') + "\\project-time-saver\\base.xlsx")
            sheet = wb["Sheet1"]
            number_of_runs = generate_report.getNumberOfRuns(conn, start_date, end_date)
            min_run = generate_report.getFirstRunNumber(conn, start_date, end_date)
            max_run = generate_report.getLastRunNumber(conn, start_date, end_date)
            generate_report.getEndPaidOnCall(sheet)
            generate_report.getStartFullTime(sheet)
            generate_report.getEndFullTime(sheet)
            generate_report.updateEmployeeNulls(conn, sheet)
            generate_report.fillSheet(conn, wb, start_date, end_date, min_run, max_run)
            additionalReturns = generate_report.checkForIssues(conn, min_run, max_run, number_of_runs, start_date, end_date)
        except Exception as e:
            conn.close
            print(e)
            return [str(e)]
        conn.close
        return [True] + additionalReturns + [f"The generated pay period is from {start_date} to {end_date}.",
            f"There were {number_of_runs} runs total this period.", f"This includes runs from run {min_run} to run {max_run}."]

    """
    Resets the global variables. Should not be needed as this class
    uses static references, but for safety this was added.
    """
    def reset():
        generate_report.endPaidOnCall = 0
        generate_report.startFullTime = 0
        generate_report.endFullTime = 0
        generate_report.cannotMatch = []

    """
    This method will do a sanity check on the final product
    to make sure that all of it looks good. If anything is amiss
    (like an employee that could not be matched to the city ID)
    then it will notify the user.

    inputs..
        conn: the sqlite connection
        min_run: the lowest run number
        max_run: the highest run number
        number_of_runs: the total number of runs
        start_date: the starting date of this report
        end_date: the ending date of this report
    returns..
        case 1: an array of strings describing the detected issues
        case 2: None if no sanity issues are found
    """
    def checkForIssues(conn, min_run, max_run, number_of_runs, start_date, end_date):
        returnArray = ["The report was generated, but failed some sanity checks."]
        missing = generate_report.checkForMissingRuns(conn, max_run, min_run, number_of_runs, start_date, end_date)
        if missing is not None: returnArray.append(missing)
        cannotBeMatched = generate_report.checkForUnmatchedEmployees(conn, start_date, end_date)
        if cannotBeMatched is not None: returnArray += cannotBeMatched
        return returnArray if len(returnArray) != 1 else []


    """
    This method checks to ensure that all employees are matched to a city ID.

    inputs..
        conn: the sqlite connection
        start_date: the starting date of this report
        end_date: the ending date of this report
    returns..
        case 1: a list of strings containing a discription of the issue followed
            by a the unmatched employee(s) and some info about them
        case 2: None of no unmatched employees
    """
    def checkForUnmatchedEmployees(conn, start_date, end_date):
        cur = conn.cursor()
        returnArray = ["One or more employees could not be matched between the run reports\
             and the tally sheet. Ensure all last names are spelled the same on both forms."]
        if generate_report.cannotMatch != []:
            for emp in generate_report.cannotMatch:
                name = emp[1]
                runs = conn.execute(f"""SELECT COUNT(*) FROM Responded 
                    WHERE date BETWEEN \'{start_date}\' AND \'{end_date}\' 
                    AND empNumber = {emp[0]}""").fetchall()[0][0]
                hours = cur.execute(f"""SELECT SUM(runTime)  FROM Run WHERE number = 
                    (SELECT runNumber FROM Responded WHERE type_of_response = 'P' AND empNumber = 
                    {emp[0]} AND date BETWEEN \'{start_date}\' AND \'{end_date}\');""").fetchall()[0][0]
                returnArray.append(f"{name} could not be matched. They had {runs} run(s) and {hours} hour(s) logged.")
        return returnArray if len(returnArray) != 1 else None

    """
    This method checks for any runs that were not included in this
    report. The is done by counting each run and checking for any
    gaps.

    inputs..
        conn: the sqlite connection
        min_run: the lowest run number
        max_run: the highest run number
        number_of_runs: the total number of runs
        start_date: the starting date of this report
        end_date: the ending date of this report
    returns..
        case 1: a string with the missing run(s)
        case 2: None if no sanity issues are found
    """
    def checkForMissingRuns(conn, max_run, min_run, number_of_runs, start_date, end_date):
        cur = conn.cursor()
        if max_run - min_run + 1 != number_of_runs:
            numbers = cur.execute(f"""SELECT DISTINCT number FROM Run WHERE 
                    date BETWEEN \'{start_date}\' AND \'{end_date}\' ORDER BY number;""").fetchall()
            missing = []
            for i in range(min_run, max_run + 1):
                if (i,) not in numbers:
                    missing.append(i)
            if len(missing) == 1:
                return f"Run {missing[0]} is missing from the report."
            elif len(missing) > 2:
                returnVal = "Runs "
                for x in missing[:-1]:
                    returnVal += (str(x) + ", ")
                return returnVal + (f"and {missing[-1]} are missing from the report.")
            else:
                return f"Runs {missing[0]} and {missing[1]} are missing from the report."
        else:
            return None

    """
    This method gets the number of runs for a given period.

    inputs..
        conn: the connection to the SQL
        start_date: the first date as a string
        end_date: the last date as a string
    returns..
        case 1: the number of runs
    """
    def getNumberOfRuns(conn, start_date, end_date):
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
    def getFirstRunNumber(conn, start_date, end_date):
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
    def getLastRunNumber(conn, start_date, end_date):
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
    def fillSheet(conn, wb, start_date, end_date, min_run, max_run):
        sheet = wb["Sheet1"]
        for i in range(8, generate_report.endPaidOnCall + 1):
            city_number = sheet[f"A{i}"].value
            if city_number is not None:
                city_number = int(city_number)
                hours = generate_report.getHours(conn, city_number, start_date, end_date)
                count = generate_report.getCount(conn, city_number, start_date, end_date)
                sheet[f"D{i}"].value = count
                sheet[f"E{i}"].value = hours
            else:
                sheet[f"D{i}"].value = 0
                sheet[f"E{i}"].value = 0
        for i in range(generate_report.startFullTime, generate_report.endFullTime + 1):
            city_number = sheet[f"A{i}"].value
            if city_number is not None:
                city_number = int(city_number)
                count = generate_report.getCount(conn, city_number, start_date, end_date)
                sheet[f"D{i}"].value = count
            else:
                sheet[f"D{i}"].value = 0
        sheet["E5"] = min_run
        sheet["G5"] = max_run
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
    def getCount(conn, city_number, start_date, end_date):
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
    def getHours(conn, city_number, start_date, end_date):
        cur = conn.cursor()
        total = 0
        runs = cur.execute(f"""SELECT runNumber FROM Responded WHERE type_of_response = 'P' AND empNumber = 
            (SELECT number FROM Employee WHERE city_number = {city_number}) AND full_time = 0
            AND date BETWEEN \'{start_date}\' AND \'{end_date}\';""").fetchall()
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
    def updateEmployeeNulls(conn, sheet):
        getNulls = """SELECT number, name FROM Employee where city_number is NULL;"""
        cur = conn.cursor()
        nullEmps = cur.execute(getNulls)
        generate_report.insertCityIDs(conn, nullEmps, sheet)

    """
    This method actually inserts the city IDs for update_employee_nulls

    inputs..
        conn: the connection to the SQL
        nullEmps: a list of employee rows that have null city_number values 
        sheet: the sheet for the tally xlsx
    """
    def insertCityIDs(conn, nullEmps, sheet):
        cur = conn.cursor()
        for emp in nullEmps:
            unmatched = emp
            for i in range(8, generate_report.endFullTime + 1):
                if sheet[f"A{i}"].value is not None and \
                        generate_report.match_names(emp[1], sheet[f"B{i}"].value, sheet[f"C{i}"].value):
                    update_string = f"""UPDATE Employee SET city_number = {sheet[f"A{i}"].value} WHERE number = {emp[0]};"""
                    cur.execute(update_string)
                    conn.commit()
                    unmatched = None
                    break
            if unmatched is not None:
                generate_report.cannotMatch.append(emp)
        return cur.lastrowid


    """
    This method gets the final row paid on call employees.

    inputs..
        sheet: the sheet for the tally xlsx
    """
    def getEndPaidOnCall(sheet):
        end = False
        if generate_report.endPaidOnCall == 0:
            generate_report.endPaidOnCall = 8
            while (not end):
                if sheet[f"C{generate_report.endPaidOnCall + 1}"].value != None:
                    generate_report.endPaidOnCall = generate_report.endPaidOnCall + 1
                else:
                    end = True

    """
    This method gets the first row of full time employees.

    inputs..
        sheet: the sheet for the tally xlsx
    """
    def getStartFullTime(sheet):
        end = False
        if generate_report.startFullTime == 0:
            generate_report.startFullTime = generate_report.endPaidOnCall
            while (not end):
                if sheet[f"A{generate_report.startFullTime + 1}"].value == None:
                    generate_report.startFullTime = generate_report.startFullTime + 1
                else:
                    generate_report.startFullTime = generate_report.startFullTime + 1
                    end = True

    """
    This method gets the final row that we are concerned with editing.

    inputs..
        sheet: the sheet for the tally xlsx
    """
    def getEndFullTime(sheet):
        end = False
        if generate_report.endFullTime == 0:
            generate_report.endFullTime = generate_report.startFullTime
            while (not end):
                if sheet[f"A{generate_report.endFullTime + 1}"].value != None:
                    generate_report.endFullTime = generate_report.endFullTime + 1
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
        elif name[0:3] == "Lt.":
            name = name[3:]
        elif name[0:6] == "Capt. ":
            name = name[6:]
        elif name[0:5] == "Capt.":
            name = name[5:]
        if name[-1].isnumeric():
            if name[-2].isnumeric():
                if name[-5] != "-":
                    name = name[0:-4]
                else:
                    name = name[0:-6]
            else:
                if name[-4] != "-":
                    name = name[0:-3]
                else:
                    name = name[0:-5]

        if name == f"{fname[0]}. {lname}" \
                or name == f"{fname[0]}.{lname}":
            return True
        else:
             return False