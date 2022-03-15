from openpyxl import load_workbook

from lib.payroll import payroll
from .config_manager import ConfigManager

class report_reader:
    def __init__(self, filePath):
        """
        When called, this function will create the object for reading
        the run report. If there are any I/O errors, a error
        will be thrown.
        """
        self.run = load_workbook(filePath)
        self.cells = ConfigManager.get_cellLocations(self.run.getDate())
        self.lastEmployeeRow = self.getLastEmployeeRow()
        self.checkForErrors()


    def __enter__(self):
        """
        This function is a boilerplate for creating a with-open block.
        It takes no arguments and simply returns itself.
        """
        return self


    def __exit__(self):
        """
        This function is a boilerplate for creating a with-open block.
        Everything contained within will be executed once the block
        is exited.
        """
        self.run.close()


    def getDate(self):
        """
        TODO: Figure out a better way to get the date agnostic of the
            specific run report. Possibly do a text search on the file
            for the date cell? Could do a regex match.
        This method gets the date, as a string, of the run report.
        This is the weak-link here. If the date cell moves, nothing works.

        returns..
            The date of the run as a string.
        """
        sheet = self.run.active
        return sheet["D2"]


    def checkForErrors(self):
        """
        This method stops execution and raises an error if there is a detectable issue
        with a run sheet.
        """
        sheet = self.run.active
        for subset in sheet[f"A{self.cell['first_employee_row']}:H{self.lastEmployeeRow}"]:
            if subset[4].value is not None or subset[5].value is not None or subset[6].value is not None:
                if subset[0].value in [None, '']:
                    raise Exception("Employee number cannot be empty!")
                if subset[1].value in [None, '']:
                    raise Exception("Employee name cannot be empty!")
                if sheet["D3"].value in [None, '']:
                    raise Exception("Date cannot be empty!")
        if sheet[self.cell["incident_number"]].value in [None, '']:
            raise Exception("Run number cannot be empty!")
        if sheet[self.cell["run_time"]].value in [None, '']:
            raise Exception("Run time cannot be empty!")
        if sheet[self.cell["reported"]].value in [None, '']:
            raise Exception("Reported cannot be empty!")
        if sheet[self.cell["1008"]].value in [None, '']:
            raise Exception("10-8 cannot be empty!")
        if sheet[self.cell["shift"]].value in [None, '']:
            raise Exception("Shift cannot be empty!")


    def getLastEmployeeRow(self):
        """
        This method will discover the total number of employee rows in the
        run report.

        returns..
            The number of employee rows
        """
        end = False
        sheet = self.run.active
        endRange = self.cells["first_employee_row"]
        while (not end):
            if sheet[f"L{endRange + 1}"].value != "=":
                endRange = endRange + 1
            else:
                end = True
        return endRange


    def getEmployeesInRun(self):
        """
        TODO: Ensure this method is as file version agnostic as possible.

        This method will get all of the employees, and all associated information, that responded
        to a run.

        returns..
            A list of tuples containing employees that responded to a run.
        """
        sheet = self.run.active
        returnList = []
        for subset in sheet[f"A{self.cell['first_employee_row']}:H{self.lastEmployeeRow}"]:
            empNumber = self.run["Pay"][subset[0].value.split("!")[1]].value
            if subset[7].value is not None:
                payRate = self.run["Pay"][subset[7].value.split("!")[1]].value
                full_time = 0
            else:
                payRate = 0
                full_time = 1
            Name = self.run["Pay"][subset[1].value.split("!")[1]].value
            if subset[4].value is not None:
                type_of_response = "PNP"
            elif subset[6].value is not None:
                type_of_response = "OD"
            elif subset[5].value is not None:
                type_of_response = "P"
            subhours = int(subset[14].value) if subset[14].value is not None else 0
            returnList.append({"number": empNumber, "payRate": payRate, "fullTime": full_time,
                    "name": Name, "responseType": type_of_response, "subhours": subhours})
        return returnList


    def getRunInfo(self):
        """
        TODO: Rewrite this DOC
        TODO: Finish making this version agnostic
        This gets the Run info from the sheet and runs the SQL import statements.

        inputs..
            sqlRunner: the sql class object
            wb: the workbook we are processing
        returns:
            case 1: the run, date, and run number of the workbook
        """
        sheet = self.run.active
        date = sheet[self.cell["date"]].value.strftime("%Y-%m-%d")
        runNumber = sheet[self.cell["incident_number"]].value
        runTime = sheet[self.cell["run_time"]].value
        startTime = sheet[self.cell["reported"]].value
        endTime = sheet[self.cell["1008"]].value
        shift = sheet[self.cell["shift"]].value
        fsc = 1 if self.checkForFill(sheet, self.cell["run_type"]["FSC"]) else 0
        stationCovered = 1 if self.checkForFill(sheet, self.cell["station_covered"]) else 0
        medrun = 1 if sheet == self.run["MED RUN"] else 0
        # TODO: Make a check here to see if there is a full cover box
        fullCover = self.getFullCover(sheet, shift)
        paid = self.isPaid(sheet, fsc, medrun)
        return {"runNumber": runNumber, "date": date, "startTime": startTime, "endTime": endTime, "runTime": runTime, "stationCovered": stationCovered, "": }
        if sqlRunner.newRunNeedsUpdated(runNumber, Timestamp, payroll.Year):
            sqlRunner.updateRun(runNumber, date, startTime, endTime, runTime, 
                                stationCovered, medrun, shift, Timestamp, 
                                fullCover, fsc, paid)
            return date, runNumber, True
        elif not sqlRunner.checkIfExists(runNumber, date):
            sqlRunner.createRun(runNumber, date, startTime, endTime, runTime, 
                                stationCovered, medrun, shift, Timestamp, 
                                fullCover, fsc, paid)
            return date, runNumber, True
        return date, runNumber, False


    def checkForFill(sheet, cell: str) -> bool:
        """
        This method is to check if the given cell is filled or not.
        Checks for color, legacy index, and any text/number value.

        inputs..
            sheet: the sheet we are checking
        outputs..
            case 1: False if it is not filled
            case 2: True if it is
        """
        color = sheet[cell].fill.start_color.index
        if type(color) == int:
            return False if color == 1 else True
        else:
            return False if color == "00000000" and\
                sheet[cell].value == None else True


    def getFullCover(sheet, shift) -> int:
        """
        This function is responsible for determining if a run was fully
        covered by its respective shift.

        inputs..
            sheet: the current run sheet
            shift: the shift of the run
        returns..
            case 1: interger 1 if the run is fully covered
            case 2: interger 0 if the run is not fully covered
        """
        fullCover = False
        lastShift = None
        for i in range(21, payroll.endRange + 1):
            if sheet[f"L{i}"].value is not None:
                lastShift = sheet[f"L{i}"].value
            if lastShift == shift and (sheet[f"E{i}"].value is not None or sheet[f"F{i}"].value is not None):
                fullCover = True
            elif lastShift == shift and sheet[f"A{i}"].value not in [000, 0000, "000", "0000"]:
                fullCover = False
                break
        return int(fullCover)


    def isPaid(sheet, fsc: int, medrun: int) -> int:
        """
        This method is for determining if a run is paid or not. Some FSC runs are paid,
        others are not, so this method sorts them out.

        inputs..
            sheet: the sheet we are checking
            fsc: the bit that determines if it is a FSC run
            medrun: the bit that determines if it is a medrun
        outputs..
            case 1: 0 if it is not paid
            case 2: 1 if it is paid
        """
        if medrun == 1:
            return 0
        if fsc == 1 and sheet["D5"].value != None:
            return 1
        if fsc == 1:
            for i1 in sheet[f"E21:G{payroll.endRange}"]:
                if i1[0] not in [None, ""] or i1[1] not in [None, ""]:
                    return 0
            return 1
        if fsc == 0 and medrun == 0:
            return 1