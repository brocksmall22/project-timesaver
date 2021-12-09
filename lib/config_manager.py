import json
import os

class ConfigManager:
    configFile = os.getenv('APPDATA') + "\\project-time-saver\\config.json"

    ##Detect if Configureation File is present
    @staticmethod
    def createConfigIfNotExists():
        emptyConf = {"folder_path": ""}
        if not os.path.exists(ConfigManager.configFile):
            with open(ConfigManager.configFile, "w") as conf:
                json.dump(emptyConf, conf)
        elif os.path.getsize(ConfigManager.configFile) == 0:
            with open(ConfigManager.configFile, "w+") as conf:
                json.dump(emptyConf, conf)
        
    ##Checks if the config file has been created, then returns the Folder Path
    @staticmethod
    def get_folderPath():
        ConfigManager.createConfigIfNotExists()
        with open(ConfigManager.configFile, "r") as conf:
            return json.load(conf)["folder_path"]

    ###Updates the folder path value
    @staticmethod
    def set_folderPath(path):
        ConfigManager.createConfigIfNotExists()
        file = ""
        with open(ConfigManager.configFile, "r") as conf:
            file = json.load(conf)
            file["folder_path"] = path
            print(file)
        with open(ConfigManager.configFile, "w+") as conf:
            json.dump(file, conf)
            
