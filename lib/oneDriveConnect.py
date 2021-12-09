import os
from datetime import datetime

class oneDriveConnect:
    # TODO finish getFiles function ---DONE
    # TODO make a compertor function to compare last modifed dates
    # TODO strip off .xlxs from filename to get run number ---DONE
    # TODO get last modified date ---DONE
    """
    getFiles(path) 
    accepts the path varible to the run folder and retrevies the run reports from the folder
    """
    files = []
    def getFiles(path):
        for file in os.listdir(path):
            if file.endswith(".xlxs"):
                oneDriveConnect.files.apened(os.path.join(path,file))
            

    """
    getLastModifiedDate(file)
    this gets the last modified date of the file with the given path
    """
    def getLastModifiedDate(file):
       return(os.path.getmtime(file))


    """
    extensionStripper(file)
    this function given the file path strips the path and the file extenstion and returns the run number
    """
    def extensionStripper(file):
        file = os.path.splitext(file)
        return(file.split("\\")[-1])


    def compareModifications(self, runNumber, date):
        Timestamp = datetime.now()
        mod= self.getLastModifiedDate()
        statement = f"""SELECT * FROM Run WHERE Date = \'{date}\' AND number = {runNumber} AND timeStamp = \'{Timestamp}\' AND modified = \'{mod}'\;"""
        cur = self.conn.cursor()
        cur.execute(statement)
        values = cur.fetchall()

        return False if len(values) == 0 else True



