from openpyxl import load_workbook
from .config_manager import ConfigManager

class report_reader:
    def __init__(self, filePath):
        """
        When called, this function will create the object for reading
        the run report. If there are any I/O errors, a error
        will be thrown.
        """
        self.run = load_workbook(filePath)
        #self.cells = ConfigManager.get_cellLocations(self.run.getDate())\
        self.cells = {
            "incident_number": "B3",
            "date": "D3",
            "shift": "F3",
            "OIC": "H3",
            "SO": "J3",
            "filer": "L3",
            "reported": "B5",
            "paged": "D5",
            "1076": "F5",
            "1023": "H5",
            "UC": "J5",
            "1008": "L5",
            "station_covered": "F6",
            "weekend": "F4",
            "working_hours": "",
            "off_hours": "",
            "shift_covered": "",
            "run_time": "B8",
            "first_employee_row": "21",
            "run_type": {
                "Fire": "O3",
                "Invest": "O4",
                "Med": "O5",
                "Hazmat": "O6",
                "Rescue": "Q3",
                "CO": "Q4",
                "Other": "Q5",
                "FSC": "Q6"
            },
            "apparatus": {
                "ENGINE 1": "A11",
                "ENGINE 2": "B11",
                "ENGINE 3": "C11",
                "TOWER 1": "D11",
                "TANKER 1": "A12",
                "GR 1": "B12",
                "COMMAND 1": "C12",
                "Command 2": "D12",
                "RESCUE 1": "A13",
                "INF Boat 1": "B13",
                "INF Boat 3": "C13",
                "Jon Boat": "D13",
                "Hazmat Tr": "A14",
                "Foam Tr": "B14",
                "Gator 1/Trailer": "C14"
            },
            "township": {
                "harrison": {
                    "city": "B17",
                    "county": "B18"
                },
                "lancaster": {
                    "city": "D17",
                    "county": "D18"
                }
            },
            "given_aid": {
                "station": {
                    "Chester": {
                        "man": "I12",
                        "app": "J12"
                    },
                    "Nottingham": {
                        "man": "I13",
                        "app": "J13"
                    },
                    "Poneto": {
                        "man": "I14",
                        "app": "J14"
                    },
                    "Monroe": {
                        "man": "I15",
                        "app": "J15"
                    },
                    "Berne": {
                        "man": "I16",
                        "app": "J16"
                    },
                    "Decatur": {
                        "man": "I17",
                        "app": "J17"
                    }
                }
            },
            "taken_aid": {
                "station": {
                    "Liberty": {
                        "man": "O12",
                        "app": "P12"
                    },
                    "Ossian": {
                        "man": "O13",
                        "app": "P13"
                    },
                    "Uniondale": {
                        "man": "O14",
                        "app": "P14"
                    },
                    "Preble": {
                        "man": "O15",
                        "app": "P15"
                    },
                    "Markle": {
                        "man": "O16",
                        "app": "P16"
                    },
                    "Southwest": {
                        "man": "O17",
                        "app": "P17"
                    }
                }
            }
        }
        self.lastEmployeeRow = self.getLastEmployeeRow()
        self.checkForErrors()


    def __enter__(self):
        """
        This function is a boilerplate for creating a with-open block.
        It takes no arguments and simply returns itself.
        """
        return self


    def __exit__(self, exc_type, exc_value, traceback):
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
        for subset in sheet[f"A{self.cells['first_employee_row']}:H{self.lastEmployeeRow}"]:
            if subset[4].value is not None or subset[5].value is not None or subset[6].value is not None:
                if subset[0].value in [None, '']:
                    raise Exception("Employee number cannot be empty!")
                if subset[1].value in [None, '']:
                    raise Exception("Employee name cannot be empty!")
                if sheet[self.cells["date"]].value in [None, '']:
                    raise Exception("Date cannot be empty!")
        if sheet[self.cells["incident_number"]].value in [None, '']:
            raise Exception("Run number cannot be empty!")
        if sheet[self.cells["run_time"]].value in [None, '']:
            raise Exception("Run time cannot be empty!")
        if sheet[self.cells["reported"]].value in [None, '']:
            raise Exception("Reported cannot be empty!")
        if sheet[self.cells["1008"]].value in [None, '']:
            raise Exception("10-8 cannot be empty!")
        if sheet[self.cells["shift"]].value in [None, '']:
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
        endRange = int(self.cells["first_employee_row"])
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
        for subset in sheet[f"A{self.cells['first_employee_row']}:O{self.lastEmployeeRow}"]:
            if not (subset[4].value == subset[5].value == subset[6].value == None):
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


    def getRunInfo(self) -> dict:
        """
        TODO: Rewrite this DOC
        TODO: Finish making this version agnostic
        TODO: Make the manual implementation for working, off, and sift
        This gets the Run info from the sheet and runs the SQL import statements.

        inputs..
            sqlRunner: the sql class object
            wb: the workbook we are processing
        returns:
            case 1: the run, date, and run number of the workbook
        """
        sheet = self.run.active
        date = sheet[self.cells["date"]].value.strftime("%Y-%m-%d")
        runNumber = sheet[self.cells["incident_number"]].value
        runTime = sheet[self.cells["run_time"]].value
        startTime = sheet[self.cells["reported"]].value
        endTime = sheet[self.cells["1008"]].value
        shift = sheet[self.cells["shift"]].value
        fsc = 1 if self.checkForFill(sheet, self.cells["run_type"]["FSC"]) else 0
        stationCovered = 1 if self.checkForFill(sheet, self.cells["station_covered"]) else 0
        medrun = 1 if sheet == self.run["MED RUN"] else 0
        fullCover = self.getFullCover(sheet, shift) if self.cells["shift_covered"] == "" else sheet[self.cells["shift_covered"]]
        paid = self.isPaid(sheet, fsc, medrun)
        oic = sheet[self.cells["OIC"]].value
        so = sheet[self.cells["SO"]].value
        filer = sheet[self.cells["filer"]].value
        code1076 = sheet[self.cells["1076"]].value
        code1023 = sheet[self.cells["1023"]].value
        uc = sheet[self.cells["UC"]].value
        code1008 = sheet[self.cells["1008"]].value
        #workingHours = sheet[self.cells["working_hours"]].value
        #offHours = sheet[self.cells["off_hours"]].value
        apparatus = self.getApparatus()
        #township = self.getTownship()
        #given_aid = self.getGivenAid()
        #taken_aid = self.getTakenAid()
        return {"runNumber": runNumber, "date": date, "startTime": startTime, "endTime": endTime,
                "runTime": runTime, "stationCovered": stationCovered, "medRun": medrun,
                "shift": shift, "fullCover": fullCover, "fsc": fsc, "paid": paid, "OIC": oic,
                "SO": so, "filer": filer, "1076": code1076, "1023": code1023, "UC": uc,
                "1008": code1008, "workingHours": "TEST", "offHours": "TEST",
                "apparatus": apparatus}


    def checkForFill(self, sheet, cell: str) -> bool:
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
                sheet[cell].value not in [1, "1"] else True


    def getFullCover(self, sheet, shift) -> int:
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
        for i in range(int(self.cells["first_employee_row"]), self.lastEmployeeRow + 1):
            if sheet[f"L{i}"].value is not None:
                lastShift = sheet[f"L{i}"].value
            if lastShift == shift and (sheet[f"E{i}"].value is not None or sheet[f"F{i}"].value is not None):
                fullCover = True
            elif lastShift == shift and sheet[f"A{i}"].value not in [000, 0000, "000", "0000"]:
                fullCover = False
                break
        return int(fullCover)


    def isPaid(self, sheet, fsc: int, medrun: int) -> int:
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
        if fsc == 1 and sheet[self.cells["paged"]].value != None:
            return 1
        if fsc == 1:
            for i1 in sheet[f"E{self.cells['first_employee_row']}:G{self.lastEmployeeRow}"]:
                if i1[0] not in [None, ""] or i1[1] not in [None, ""]:
                    return 0
            return 1
        if fsc == 0 and medrun == 0:
            return 1


    def getApparatus(self):
        """
        This method is responsible for getting a list of apparatus used for
        an incident.

        returns..
            A string encoding of a list
                eg. "ENGINE 1,COMMAND 1,RESCUE 1
                    "RESCUE 1"
        """
        returnVal = ""
        sheet = self.run.active
        apps = self.cells["apparatus"].keys()
        for app in apps:
            if self.checkForFill(sheet, self.cells["apparatus"][app]):
                if returnVal != "":
                    returnVal += ","
                returnVal += app
        return returnVal
