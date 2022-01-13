from contextlib import nullcontext
from config_manager import config_manager as conf
import os
import shutil

# TODO get database from local directory --DONE
# TODO upload database to onedrive with the given config --DONE
# TODO make checksum function
# TODO Run checksum function against version stored on Local against onedrive to check stablity
# TODO get database from onedrive
# TODO get last modified date from onedrive check against local copy for backup update


class backup:

    database_file = ""
    filename = ""

    def getLocalDB(database_path):
        if database_path == "":
            database_path = conf.get_DataBasePath()
        backup.database_file = database_path

        backup.filename = os.path.basename(backup.database_file)
        return backup.database_file



    def uploadLocalDB(database, onedrive_path):
        if onedrive_path == "":
            onedrive_path = conf.get_BackupPath()
        shutil.copyfile(database, onedrive_path)

        endPath = os.path.join(onedrive_path, backup.filename)

        return endPath


