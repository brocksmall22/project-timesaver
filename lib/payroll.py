import openpyxl

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
        print(file.value)
        wb = loadWorkBooks(file.value)
        readWorkBook(wb)

# reads an indiual work book then prints the resulting values from in the range of cells A20->H55
# this still needs works with openpyxl as it  has trouble starting i do not know which values it returns yet


def readWorkBook(wb):
    sheet = wb.active
    cells = sheet['A20', 'H55']
    for i1, i2, i3, i4 in cells:
        print("{0} {1} {2} {3}".format(i1.value, i2.value, i3.value, i4.value))

# this main is purely for testing and will be removed later


def main():
    loadWorkBooks(getfilelist(input()))


if __name__ == "__main__":
    main()
