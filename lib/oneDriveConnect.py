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
        return(file.split("/")[-1])



