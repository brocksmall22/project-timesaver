from contextlib import nullcontext
from hmac import digest
from config_manager import config_manager as conf
import os
import shutil
import hashlib

# TODO get database from local directory --DONE
# TODO upload database to onedrive with the given config --DONE
# TODO make checksum function --DONE
# TODO Run checksum function against version stored on Local against onedrive to check stablity --DONE
# TODO get database from onedrive
# TODO get last modified date from onedrive check against local copy for backup update


class backup_manager:

    database_file = ""
    filename = ""

    def getLocalDB(database_path):
        if database_path == "":
            database_path = os.getenv("APPDATA") + "\\project-time-saver\\database.db"
        backup_manager.database_file = database_path

        backup_manager.filename = os.path.basename(backup_manager.database_file)
        return backup_manager.database_file

    def uploadLocalDB(database, onedrive_path):
        if onedrive_path == "":
            onedrive_path = conf.get_BackupPath()
        shutil.copyfile(database, onedrive_path)

        endPath = os.path.join(onedrive_path, backup_manager.filename)

        return endPath

    def generateHash(filepath):
        md5_hash = hashlib.md5()
        file = open(filepath, "rb")
        file_content = file.read()
        md5_hash.update(file_content)
        digest = md5_hash.hexdigest()
        return digest

    def checksum(local_filePath, cloud_filePath):

        if backup_manager.generateHash(local_filePath) != backup_manager.generateHash(
            cloud_filePath
        ):
            return False

        return True
