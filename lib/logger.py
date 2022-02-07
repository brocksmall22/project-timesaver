from datetime import datetime
import json
import os

class Logger:
    logFile = os.getenv('APPDATA') + "\\project-time-saver\\log.json"

    ##Detect if log file is present
    @staticmethod
    def createLogIfNotExists(file = ""):
        file = Logger.logFile if file == "" else file
        emptyLog = {"lastUpdate": "",
                    "errors": [],
                    "generateMessages": []}
        if not os.path.exists(file):
            with open(file, "w") as log:
                json.dump(emptyLog, log)
        elif os.path.getsize(file) == 0:
            with open(file, "w+") as log:
                json.dump(emptyLog, log)
        
    ##Checks if the config file has been created, then returns the last update
    @staticmethod
    def getLastUpdate(file = ""):
        file = Logger.logFile if file == "" else file
        Logger.createLogIfNotExists(file)
        with open(file, "r") as log:
            return json.load(log)["lastUpdate"]

    ###Updates the last update value
    @staticmethod
    def setLastUpdate(newUpdate, file = ""):
        file = Logger.logFile if file == "" else file
        Logger.createLogIfNotExists(file)
        contents = ""
        with open(file, "r") as log:
            contents = json.load(log)
            contents["lastUpdate"] = newUpdate
        with open(file, "w+") as log:
            json.dump(contents, log)

    ##Gets the logged errors
    @staticmethod
    def getErrors(file = ""):
        file = Logger.logFile if file == "" else file
        Logger.createLogIfNotExists(file)
        with open(file, "r") as log:
            return json.load(log)["errors"]

    ###Adds a new error to the log
    @staticmethod
    def addNewError(type: str, datetime: datetime, message: str, file = ""):
        file = Logger.logFile if file == "" else file
        Logger.createLogIfNotExists(file)
        contents = ""
        with open(file, "r") as log:
            contents = json.load(log)
            contents["errors"].append({"type": type, "time": datetime.strftime("%Y-%m-%d %H:%M:%S"), "message": message})
        with open(file, "w+") as log:
            json.dump(contents, log)

    ##Removes all logged errors
    @staticmethod
    def clearErrors(file = ""):
        file = Logger.logFile if file == "" else file
        Logger.createLogIfNotExists(file)
        contents = ""
        with open(file, "r") as log:
            contents = json.load(log)
            contents["errors"] = []
        with open(file, "w+") as log:
            json.dump(contents, log)

    ##Gets the generation messages
    @staticmethod
    def getGenerateMessages(file = ""):
        file = Logger.logFile if file == "" else file
        Logger.createLogIfNotExists(file)
        with open(file, "r") as log:
            return json.load(log)["generateMessages"]

    ###Adds a new generation message
    @staticmethod
    def addNewGenerateMessage(newMessage, file = ""):
        file = Logger.logFile if file == "" else file
        Logger.createLogIfNotExists(file)
        contents = ""
        with open(file, "r") as log:
            contents = json.load(log)
            contents["generateMessages"].append(newMessage)
        with open(file, "w+") as log:
            json.dump(contents, log)

    ###Resets the generation messages
    @staticmethod
    def clearGenerateMessages(file = ""):
        file = Logger.logFile if file == "" else file
        Logger.createLogIfNotExists(file)
        contents = ""
        with open(file, "r") as log:
            contents = json.load(log)
            contents["generateMessages"] = []
        with open(file, "w+") as log:
            json.dump(contents, log)
            
