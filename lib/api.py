import os
from flask import Flask, jsonify, request, Response
from datetime import datetime
from image_api import image_api
from flask.config import Config
from .logger import Logger

from lib.backup_manager import backupManager as bm
from lib.sqlFunctions import sqlFunctions
from .generate_report import generate_report as grp
from .payroll import payroll
import sqlite.check_database as cdb
from flask.wrappers import Request
from .config_manager import ConfigManager
from flask_apscheduler import APScheduler

app = Flask(__name__)
app.register_blueprint(image_api, url_prefix='/images')
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

INTERVAL_TASK_ID = "interval-task-id"
INTERVAL_TASK_ID_1 = "interval-task-id-1"

def scheduled_db_update():
    """
    This is a wrapper for the loadWorkbooks function. It is
    intended to pause the backup job so they cannot run at the
    same time (which may cause synchronony issues).
    """
    scheduler.pause_job(id=INTERVAL_TASK_ID_1)
    payroll.loadWorkBooks()
    scheduler.resume_job(id=INTERVAL_TASK_ID_1)

def scheduled_db_backup():
    """
    This is a wrapper function for the uploadLocalDB function.
    It is intended to pause the update job as it could cause
    synchronoy issues if they execute at the same time.
    """
    scheduler.pause_job(id=INTERVAL_TASK_ID)
    bm.uploadLocalDB(bm.getLocalDB())
    scheduler.resume_job(id=INTERVAL_TASK_ID)

scheduler.add_job(
    id=INTERVAL_TASK_ID,
    func=scheduled_db_update,
    trigger="interval",
    minutes=30
)

scheduler.add_job(
    id=INTERVAL_TASK_ID_1,
    func=scheduled_db_backup,
    trigger="interval",
    minutes=60,
)

"""
This method will run before the first request to the server. It ensures that the DB exists and is ready for use.
"""
@app.before_first_request
def ensure_database_is_ready():
    cdb.check_database.check()


"""
This section will return an error message to the requester (the UI for us)
if an invalid address is sent a request.
"""
@app.errorhandler(404)
def invalid_route():
    return jsonify(
        {
            "message": "Route not found! Requested address was: " + Request.full_path,
        }
    ), 404


"""
This function is for the UI to determine if the server is running. If the server
sees any call to this address, it will return a signal signifying the sercer is alive.
If the UI recieves a socket error, that means the server is not running and needs
to be started.

inputs..
    (request) Any request on this address
returns.. 
    case 1: A Json object signifying the server is alive
"""
@app.route("/verify", methods=["GET", "POST"])
def verify_awake():
    return jsonify({"result": True}), 200


"""
This is the function responsible for accepting a request from the UI
to tell the backend the user wishes to generate the pay reports.

inputs..
    (request): A Json object containing two key value pairs
        startDate and endDate that express the start and end of the
        pay period as strings
returns.. 
    Code 200 on successful completion
    Code 500 if anerror occurs
    Code 400 if bad parameters
"""
@app.route('/generate_report', methods=["POST"])
def generate_reports():
    values = request.json
    try: 
        startDate = values["start_date"].split(" ")[0]
        endDate = values["end_date"].split(" ")[0]
        blank_payroll = values["payroll"]
        blank_breakdown = values["breakdown"]
        success = grp.generate_report(startDate, endDate,
                    blank_payroll, blank_breakdown)
    except Exception as e:
        print(e)
        return Response(status = 400)
    return Response(status = 200) if success else Response(status = 500)


"""
This method gets the one drive folder location on a GET request.

returns..
    the one drive folder as stored in the config
"""
@app.route("/get_one_drive_folder", methods=["GET"])
def get_one_drive_folder():
    return jsonify({"one_drive_folder": ConfigManager.get_folderPath()}), 200


"""
This method sets the one drive folder value in the config.

inputs..
    (request): A json file containing the new value
returns..
    Code 200 on successful update
    Code 400 if bad parameters passed
"""
@app.route("/set_one_drive_folder", methods=["POST"])
def set_one_drive_folder():
    oneDrivefolder = request.json
    try:
        ConfigManager.set_folderPath(oneDrivefolder["one_drive_folder"])
    except Exception:
        return Response(status = 400)
    return Response(status = 200)


"""
This method gets the value of the most recent sync operation on the DB.

returns..
    A json containing the most recent value
"""
@app.route("/get_most_recent_db_update", methods=["GET"])
def get_most_recent_db_update():
    return jsonify({"update": Logger.getLastUpdate()}), 200


"""
This method gets the number of the most revent run.

returns..
    A json containing the number of the most recent run
    The value is 0 if no runs are in the DB
"""
@app.route("/get_most_recent_run", methods=["GET"])
def get_most_recent_run():
    with sqlFunctions(os.getenv("APPDATA") +
                "\\project-time-saver\\database.db" ) as sql:
        stored = sql.getMostRecentRun(datetime.now().strftime("%Y") + "-01-01")
        stored = 0 if stored == None else stored
        return jsonify({"update": stored}), 200


"""
This method is responsible for triggering an update to the DB.

returns..
    Code 200 if successful
    Code 500 if there are any errors
"""
@app.route("/trigger_update", methods=["GET"])
def trigger_update():
    scheduler.pause_job(id=INTERVAL_TASK_ID)
    scheduler.pause_job(id=INTERVAL_TASK_ID_1)
    success = payroll.loadWorkBooks()
    scheduler.resume_job(id=INTERVAL_TASK_ID)
    scheduler.resume_job(id=INTERVAL_TASK_ID_1)
    return Response(status = 200) if success else Response(status = 500)


"""
This method is responsible for getting all of the logged errors.

returns..
    A json array containing error json objects
"""
@app.route("/get_errors", methods=["GET"])
def get_errors():
    return jsonify(Logger.getErrors()), 200


"""
This method is responsible for triggering a clear errors call.

returns..
    True upon completion
"""
@app.route("/clear_errors", methods=["GET"])
def clear_errors():
    Logger.clearErrors()
    return Response(status = 200)


"""
This method is responsible for getting the generation messages.

returns..
    A json array containing a list of strings
"""
@app.route("/get_generation_messages", methods=["GET"])
def get_generation_messages():
    return jsonify(Logger.getGenerateMessages()), 200


"""
This method is responsible for clearing the saved generation messages.

returns..
    True upon completion
"""
@app.route("/clear_generation_messages", methods=["GET"])
def clear_generation_messages():
    Logger.clearGenerateMessages()
    return Response(status = 200)


@app.route("/get_backup_folder", methods=["GET"])
def get_backup_folder():
    """
    This method gets the database backup folder location on a GET request.

    returns..
        the backup folder as stored in the config
    """
    return jsonify({"backup_folder": ConfigManager.get_backupPath()}), 200


@app.route("/set_backup_folder", methods=["POST"])
def set_backup_folder():
    """
    This method sets the backup folder value in the config.

    inputs..
        (request): A json file containing the new value
    returns..
        True upon completion
    """
    oneDrivefolder = request.json
    ConfigManager.set_backupPath(oneDrivefolder["backup_folder"])
    return Response(status = 200)


@app.route("/get_blank_payroll_path", methods=["GET"])
def get_blank_payroll_path():
    """
    This method gets the blank payroll path on a GET request.

    returns..
        the blank payroll path as stored in the config
    """
    return jsonify({"blank_payroll_path": ConfigManager.get_blankPayrollPath()}), 200


@app.route("/set_blank_payroll_path", methods=["POST"])
def set_blank_payroll_path():
    """
    This method sets the blank payroll path value in the config.

    inputs..
        (request): A json file containing the new value
    returns..
        True upon completion
    """
    path = request.json
    ConfigManager.set_blankPayrollPath(path["blank_payroll_path"])
    return Response(status = 200)


@app.route("/get_blank_breakdown_path", methods=["GET"])
def get_blank_breakdown_path():
    """
    This method gets the blank breakdown path on a GET request.

    returns..
        the blank breakdown path as stored in the config
    """
    return jsonify({"blank_breakdown_path": ConfigManager.get_blankBreakdownPath()}), 200


@app.route("/set_blank_breakdown_path", methods=["POST"])
def set_blank_breakdown_path():
    """
    This method sets the blank breakdown path value in the config.

    inputs..
        (request): A json file containing the new value
    returns..
        True upon completion
    """
    path = request.json
    ConfigManager.set_blankBreakdownPath(path["blank_breakdown_path"])
    return Response(status = 200)


@app.route("/trigger_backup", methods=["GET"])
def trigger_backup():
    """
    This method is responsible for triggering a backup of the DB.

    returns..
        Code 200 if successful
        Code 500 if there are any errors
    """
    scheduler.pause_job(id=INTERVAL_TASK_ID)
    scheduler.pause_job(id=INTERVAL_TASK_ID_1)
    success = bm.uploadLocalDB(bm.getLocalDB())
    scheduler.resume_job(id=INTERVAL_TASK_ID)
    scheduler.resume_job(id=INTERVAL_TASK_ID_1)
    return Response(status = 200) if success != "" else Response(status = 500)


@app.route("/trigger_restore", methods=["GET"])
def trigger_restore():
    """
    This method is responsible for triggering a restore of the DB.

    returns..
        Code 200 if successful
        Code 500 if there are any errors
    """
    scheduler.pause_job(id=INTERVAL_TASK_ID)
    scheduler.pause_job(id=INTERVAL_TASK_ID_1)
    success = bm.downloadCloudDB(bm.getCloudDB())
    scheduler.resume_job(id=INTERVAL_TASK_ID)
    scheduler.resume_job(id=INTERVAL_TASK_ID_1)
    return Response(status = 200) if success != "" else Response(status = 500)