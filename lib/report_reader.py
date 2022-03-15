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
        TODO: Revisit this to change all of the sheet cell direct locations with
            locations from the configuration.
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
        if sheet["B3"].value in [None, '']:
            raise Exception("Run number cannot be empty!")
        if sheet["B8"].value in [None, '']:
            raise Exception("Run time cannot be empty!")
        if sheet["B5"].value in [None, '']:
            raise Exception("Reported cannot be empty!")
        if sheet["L5"].value in [None, '']:
            raise Exception("10-8 cannot be empty!")
        if sheet["F3"].value in [None, '']:
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