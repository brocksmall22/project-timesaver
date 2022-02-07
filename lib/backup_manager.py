from contextlib import nullcontext
from fileinput import close
from hmac import digest
from .config_manager import ConfigManager as conf
import os
import shutil
import hashlib


class backupManager:

    database_file = ""
    filename = ""
    """
    getLocalDB(database_path)
    This method gets the local database file
    
    inputs..
        (database_path): takes a filepath as a string to the database used for testing.
    returns..
        The database file
    """

    def getLocalDB(database_path):
        if database_path == "":
            database_path = os.getenv("APPDATA") + "\\project-time-saver\\database.db"
        backupManager.database_file = database_path

        backupManager.filename = os.path.basename(backupManager.database_file)

        return backupManager.database_file

    """
    uploadLocalDB(database, onedrive_path)
    This method uploads the database to the onedrive

    inputs..
        (database, onedrive_path):takes the database folder itself. takes a filepath to the one drive folder as a string used for testing.
    returns..
        The full filepath of the uploaded folder
    """

    def uploadLocalDB(database, onedrive_path):
        if onedrive_path == "":
            onedrive_path = conf.get_BackupPath()
        shutil.copy(database, onedrive_path)

        endPath = os.path.join(onedrive_path, backupManager.filename)

        return endPath

    """
    getCloudDB(database_path)
    This method gets the cloud database file.

    inputs..
        (database_path): takes a filepath as a string to the database used for testing.
    returns..
        The database file
    """

    def getCloudDB(database_path):
        if database_path == "":
            database_path = conf.get_backupPath() + "//database.db"
        backupManager.database_file = database_path

        backupManager.filename = os.path.basename(backupManager.database_file)

        return backupManager.database_file

    """
    downloadCloudDB(database, local_path)
    This method checks to see if the two databases are diffrent if diffrent then downloads the database

    inputs..
        (database, local_path):takes the database folder itself. takes a filepath to the local database as a string used for testing.
    returns..
        The full filepath of the downloaded file
        Database is already on current version. if the database does not need updated
    """

    def downloadCloudDB(database, local_path):
        if local_path == "":
            local_path = os.getenv("APPDATA") + "\\project-time-saver\\database.db"
        if (
            backupManager.checksum(local_path, conf.get_backupPath() + "//database.db")
            == True
        ):
            return "Database is already on current version."

        shutil.copy(database, local_path)

        endPath = os.path.join(local_path, backupManager.filename)

        return endPath

    """
    generateHash(filepath)
    This method generates the Hash of files contents

    inputs..
        (filepath): takes a filepath as a string.
    returns..
        The hash hexdigest upon completion
    """

    def generateHash(filepath):
        md5_hash = hashlib.md5()
        file = open(filepath, "rb")
        file_content = file.read()
        md5_hash.update(file_content)
        digest = md5_hash.hexdigest()
        file.close()
        return digest

    """
    checksum(local_filePath, cloud_filePath)
    This method runs the generate function on two files and checks the hashes

    inputs..
        (local_filePath, cloud_filePath): these are the paths to the local file path and cloud filepath.
    returns..
        True upon Matching Hashes 

        False upon non matching hashes
    """

    def checksum(local_filePath, cloud_filePath):

        if backupManager.generateHash(local_filePath) != backupManager.generateHash(
            cloud_filePath
        ):
            return False

        return True
