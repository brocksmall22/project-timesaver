import os
from tkinter import W
from config_manager import ConfigManager


class oneDriveConnect:

    files = []

    def getFiles(path = "") -> list or None:
        """
        Gets a list of run report URIs.

        inputs..
            path (optinal): the path to the folder containing run reports,
                used for testing/debugging. Production will fetch this
                location from a configuration file.
        returns..
            list: the list of URIs as strings (empty if none are found)
            None: the response in the case no path is set in the config
                or passed as an argument
        """
        if path == "":
            path = ConfigManager.get_folderPath()
        if path == "":
            return None
                
        for file in os.listdir(path):
            if file.endswith(".xlsx"):
                oneDriveConnect.files.append(os.path.join(path, file))
        return oneDriveConnect.files


    def getLastModifiedDate(file: str) -> int:
        """
        This gets the last modified date of the file with the given path.

        inputs..
            file: the file (URI as a string) that you want to know the
                last modify date of
        returns..
            int: the last modify time of the file as an epoc time int
        """
        return os.path.getmtime(file)


    def extensionStripper(file: str):
        """
        This function given the file path strips the path and the file extenstion and returns the run number

        inputs..
            file: the URI of the file you want to strip
        returns..
            str: the stripped name of the file
        """
        file = os.path.splitext(file)[0]
        return file.split("\\")[-1]
