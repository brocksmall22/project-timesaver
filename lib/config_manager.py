import json
import os

class ConfigManager:
    configFile = os.getenv('APPDATA') + "\\project-time-saver\\config.json"

    ##Detect if Configureation File is present
    @staticmethod
    def createConfigIfNotExists(file = ""):
        file = ConfigManager.configFile if file == "" else file
        emptyConf = {"folder_path": ""}
        if not os.path.exists(file):
            with open(file, "w") as conf:
                json.dump(emptyConf, conf)
        elif os.path.getsize(file) == 0:
            with open(file, "w+") as conf:
                json.dump(emptyConf, conf)
        
    ##Checks if the config file has been created, then returns the Folder Path
    @staticmethod
    def get_folderPath(file = ""):
        file = ConfigManager.configFile if file == "" else file
        ConfigManager.createConfigIfNotExists(file)
        with open(file, "r") as conf:
            return json.load(conf)["folder_path"]

    ###Updates the folder path value
    @staticmethod
    def set_folderPath(path, file = ""):
        file = ConfigManager.configFile if file == "" else file
        ConfigManager.createConfigIfNotExists(file)
        with open(file, "r") as conf:
            contents = json.load(conf)
            contents["folder_path"] = path
        with open(file, "w+") as conf:
            json.dump(contents, conf)
            
