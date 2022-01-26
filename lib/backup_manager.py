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

    def getLocalDB(database_path):
        if database_path == "":
            database_path = os.getenv("APPDATA") + "\\project-time-saver\\database.db"
        backupManager.database_file = database_path

        backupManager.filename = os.path.basename(backupManager.database_file)

        return backupManager.database_file

    def uploadLocalDB(database, onedrive_path):
        if onedrive_path == "":
            onedrive_path = conf.get_BackupPath()
        shutil.copy(database, onedrive_path)

        endPath = os.path.join(onedrive_path, backupManager.filename)
        # os.close(database)

        return endPath

    def generateHash(filepath):
        md5_hash = hashlib.md5()
        file = open(filepath, "rb")
        file_content = file.read()
        md5_hash.update(file_content)
        digest = md5_hash.hexdigest()
        file.close()
        return digest

    def checksum(local_filePath, cloud_filePath):

        if backupManager.generateHash(local_filePath) != backupManager.generateHash(
            cloud_filePath
        ):
            return False

        return True
