import os

class oneDriveConnect:
    # TODO finish getFiles function
    # TODO make a compertor function to compare last 
    # TODO strip off .xlxs from filename to get run number and get last modified date 
    """
    getFiles(path) 
    accepts the path varible to the run folder and retrevies the run reports from the folder
    """
    files = []
    def getFiles(path):
        for file in os.listdir(path):
            if file.endswith(".xlxs"):
                oneDriveConnect.files.apened(file)

    