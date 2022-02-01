import json
import os


class ConfigManager:
    configFile = os.getenv("APPDATA") + "\\project-time-saver\\config.json"

    ##Detect if Configureation File is present
    @staticmethod
    def createConfigIfNotExists(file=""):
        file = ConfigManager.configFile if file == "" else file
        emptyConf = {"folder_path": "", "Backup_path": "", "blank_payroll_path": "", "blank_breakdown_path": ""}
        if not os.path.exists(file):
            with open(file, "w") as conf:
                json.dump(emptyConf, conf)
        elif os.path.getsize(file) == 0:
            with open(file, "w+") as conf:
                json.dump(emptyConf, conf)

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
        print("asdfhalskjfhlakjsdhfljahsdlfhalskfh")
        file = ConfigManager.configFile if file == "" else file
        ConfigManager.createConfigIfNotExists(file)
        with open(file, "r") as conf:
            return json.load(conf)["blank_payroll_path"]

    ###Updates the blank payroll path value
    @staticmethod
    def set_blankPayrollPath(path, file=""):
        print("565461654198165416541654164561464")
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
