import os
from .config_manager import ConfigManager


class oneDriveConnect:

    """
    getFiles(path) 
    accepts the path varible to the run folder and retrevies the run reports from the folder
    """
    files = []

    def getFiles(path = ""):
        if path == "":
            path = ConfigManager.get_folderPath()
        for file in os.listdir(path):
            if file.endswith(".xlsx"):
                oneDriveConnect.files.append(os.path.join(path, file))
        return oneDriveConnect.files

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
        file = os.path.splitext(file)[0]
        return(file.split("\\")[-1])
