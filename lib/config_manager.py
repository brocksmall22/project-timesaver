from datetime import datetime
import json
import os


class ConfigManager:
    """
    The config file contains several keys and should look like the following:
    {
        "folder_path": "C:\path\to\oneDrive\folder",
        "backup_path": "C:\path\to\the\backup\folder\in\the\oneDrive",
        "blank_payroll_path": "C:\path/to/the/master/copy/of/payroll",
        "blank_breakdown_path": "C:\path/to/the/master/copy/of/breakdown",
        "cell_locations": [
            {
                "startDate": "",
                "endDate": "",
                "incidentNumber": "",
                "date": "",
                "shift": "",
                "OIC": "",
                "SO": "",
                "filer": "",
                "reported": "",
                "paged": "",
                "1076": "",
                "1023": "",
                "UC": "",
                "1008": "",
                "stationCovered": "",
                "weekend": "",
                "workingHours": "",
                "offHours": "",
                "shiftCovered": "",
                "runTime": "",
                "firstEmployeeRow": "",
                "runType": {},
                "apparatus": {},
                "township": {},
                "givenAid": {},
                "takenAid": {}
                ]
            }
        ]
    }
    """
    configFile = os.getenv("APPDATA") + "\\project-time-saver\\config.json"
    defaultConfig = {"folder_path": "",
                    "Backup_path": "",
                    "blank_payroll_path": "",
                    "blank_breakdown_path": "",
                    "cell_locations": []}

    ##Detect if Configureation File is present
    @staticmethod
    def createConfigIfNotExists(file=""):
        file = ConfigManager.configFile if file == "" else file
        if not os.path.exists(file):
            with open(file, "w") as conf:
                json.dump(ConfigManager.defaultConfig, conf)
        elif os.path.getsize(file) == 0:
            with open(file, "w+") as conf:
                json.dump(ConfigManager.defaultConfig, conf)

    ##Checks if the config file has been created, then returns the Folder Path
    @staticmethod
    def get_folderPath(file=""):
        file = ConfigManager.configFile if file == "" else file
        ConfigManager.createConfigIfNotExists(file)
        with open(file, "r") as conf:
            return json.load(conf)["folder_path"]

    ###Updates the folder path value
    @staticmethod
    def set_folderPath(path, file=""):
        file = ConfigManager.configFile if file == "" else file
        ConfigManager.createConfigIfNotExists(file)
        with open(file, "r") as conf:
            contents = json.load(conf)
            contents["folder_path"] = path
        with open(file, "w+") as conf:
            json.dump(contents, conf)

    @staticmethod
    def get_backupPath(file=""):
        file = ConfigManager.configFile if file == "" else file
        ConfigManager.createConfigIfNotExists(file)
        with open(file, "r") as conf:
            return json.load(conf)["Backup_path"]

    ###Updates the folder path value
    @staticmethod
    def set_backupPath(path, file=""):
        file = ConfigManager.configFile if file == "" else file
        ConfigManager.createConfigIfNotExists(file)
        with open(file, "r") as conf:
            contents = json.load(conf)
            contents["Backup_path"] = path
        with open(file, "w+") as conf:
            json.dump(contents, conf)

    @staticmethod
    def get_blankPayrollPath(file=""):
        file = ConfigManager.configFile if file == "" else file
        ConfigManager.createConfigIfNotExists(file)
        with open(file, "r") as conf:
            return json.load(conf)["blank_payroll_path"]

    ###Updates the blank payroll path value
    @staticmethod
    def set_blankPayrollPath(path, file=""):
        file = ConfigManager.configFile if file == "" else file
        ConfigManager.createConfigIfNotExists(file)
        with open(file, "r") as conf:
            contents = json.load(conf)
            contents["blank_payroll_path"] = path
        with open(file, "w+") as conf:
            json.dump(contents, conf)

    @staticmethod
    def get_blankBreakdownPath(file=""):
        file = ConfigManager.configFile if file == "" else file
        ConfigManager.createConfigIfNotExists(file)
        with open(file, "r") as conf:
            return json.load(conf)["blank_breakdown_path"]

    ###Updates the blank breakdwon path value
    @staticmethod
    def set_blankBreakdownPath(path, file=""):
        file = ConfigManager.configFile if file == "" else file
        ConfigManager.createConfigIfNotExists(file)
        with open(file, "r") as conf:
            contents = json.load(conf)
            contents["blank_breakdown_path"] = path
        with open(file, "w+") as conf:
            json.dump(contents, conf)

    @staticmethod
    def get_allCellLocationConfigs(file=""):
        """
        This method gets all of the layout configs.

        inputs..
            file: an optional file path to the configuration file
        returns..
            A list of layout config dictonaries
        """
        file = ConfigManager.configFile if file == "" else file
        ConfigManager.createConfigIfNotExists(file)
        with open(file, "r") as conf:
            return json.load(conf)["cell_locations"]

    @staticmethod
    def set_cellLocations(configurations: list, file=""):
        """
        This function take in a set of configurations and saves them to the config
        filr.

        inputs..
            configurations: a list of dictonaties
            file: an optional override for the config file path
        """
        file = ConfigManager.configFile if file == "" else file
        ConfigManager.createConfigIfNotExists(file)
        with open(file, "r") as conf:
            contents = json.load(conf)
            contents["cell_locations"] = configurations
        with open(file, "w+") as conf:
            json.dump(contents, conf)
