from openpyxl import load_workbook


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

    getRunInfo(wb)

    getEmpinfo(wb)


# this gets and returns the pay rate and employe number for those on run
def getEmpinfo(wb):
    sheet = wb.active
    for i1 in sheet["A21:h55"]:

        if i1[5].value == 1:

            returnSting = wb["Pay"][i1[0].value.split("!")[1]].value
            print("Emp Num: " + str(returnSting))
            returnSting = wb["Pay"][i1[7].value.split("!")[1]].value
            print("PayRate: " + str(returnSting))


# this is no longer needed only here for refernce at this time
def getPayRate(wb):
    sheet = wb.active
    for i1 in sheet["F21:H55"]:

        if i1[0].value == 1:

            returnSting = wb["Pay"][i1[2].value.split("!")[1]].value
            print("PayRate: " + str(returnSting))


# gets all run info from the spcifc cells
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


# this main is purely for testing and will be removed later


def main():
    loadWorkBooks(getfilelist(input()))


if __name__ == "__main__":
    main()
