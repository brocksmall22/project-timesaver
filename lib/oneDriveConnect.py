import os

class oneDriveConnect:
    # TODO finish getFiles function ---DONE
    # TODO make a comparator function to compare last modified dates
    # TODO strip off .xlxs from filename to get run number and get last modified date 
    """
    getFiles(path) 
    accepts the path variable to the run folder and retrieves the run reports from the folder
    """
    files = []
    def getFiles(path):
        for file in os.listdir(path):
            if file.endswith(".xlxs"):
                oneDriveConnect.files.apened(os.path.join(path,file))
        for i in oneDriveConnect.files:
            print(i)

    def getLastModifiedDate(file):
       return(os.path.getmtime(file))

    def main():
        oneDriveConnect.getFiles()