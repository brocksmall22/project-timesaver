from openpyxl import load_workbook

# having trouble with import on PC

fileList = []
returnArray = []

# returns the file list as an array using " "as a seperator between file names


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
# this still needs works with openpyxl as it  has trouble starting i do not know which values it returns yet


def readWorkBook(wb):
    sheet = wb.active
    for i1 in sheet["A21:F55"]:
        
        if i1[5].value == 1:
            
            returnSting = wb["Pay"][i1[0].value.split("!")[1]].value
            print(returnSting)
            

# this main is purely for testing and will be removed later


def main():
    loadWorkBooks(getfilelist(input()))


if __name__ == "__main__":
    main()
