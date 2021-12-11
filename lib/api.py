import os
from flask import Flask, jsonify, request
from datetime import datetime

from flask.config import Config
from .logger import Logger

from lib.sqlFunctions import sqlFunctions
from .generate_report import generate_report as grp
from .payroll import payroll
import sqlite.check_database as cdb
from flask.wrappers import Request
from .config_manager import ConfigManager
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
scheduler = BackgroundScheduler()
job = scheduler.add_job(payroll.loadWorkBooks(), 'interval', minutes=30)
scheduler.start()

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
    return(jsonify({"errorCode": 404, "message": "Route not found! Requested address was: " + Request.full_path}))


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
@app.route('/verify', methods=["GET", "POST"])
def verify_awake():
    return jsonify({"result": True})

"""
This is the function responsible for accepting a request from the UI
to tell the backend the user wishes to generate the pay reports.

inputs..
    (request): A Json object containing two key value pairs
        startDate and endDate that express the start and end of the
        pay period as strings
returns.. 
    True on completion
"""
@app.route('/generate_report', methods=["GET", "POST"])
def generate_reports():
    dates = request.json
    startDate = dates["startDate"].split(" ")[0]
    endDate = dates["endDate"].split(" ")[0]
    grp.generate_report(startDate, endDate)
    return jsonify(True)

"""
This method gets the one drive folder location on a GET request.

returns..
    the one drive folder as stored in the config
"""
@app.route("/get_one_drive_folder", methods=["GET"])
def get_one_drive_filder():
    return jsonify({"oneDriveFolder": ConfigManager.get_folderPath()})

"""
This method sets the one drive folder value in the config.

inputs..
    (request): A json file containing the new value
returns..
    True upon completion
"""
@app.route("/set_one_drive_folder", methods=["POST"])
def set_one_drive_folder():
    oneDrivefolder = request.json
    ConfigManager.set_folderPath(oneDrivefolder["oneDriveFolder"])
    return jsonify(True)

"""
This method gets the value of the most recent sync operation on the DB.

returns..
    A json containing the most recent value
"""
@app.route("/get_most_recent_db_update", methods=["GET"])
def get_most_recent_db_update():
    with sqlFunctions(os.getenv('APPDATA') + "\\project-time-saver\\database.db") as sql:
        return jsonify({"update": Logger.getLastUpdate()})

"""
This method gets the number of the most revent run.

returns..
    A json containing the number of the most recent run
"""
@app.route("/get_most_recent_run", methods=["GET"])
def get_most_recent_run():
    with sqlFunctions(os.getenv('APPDATA') + "\\project-time-saver\\database.db") as sql:
        return jsonify({"update": sql.getMostRecentRun(datetime.now().strftime("%Y")+"-01-01")})

"""
This method is responsible for triggering an update to the DB.

returns..
    True on completion
"""
@app.route("/trigger_update", methods = ["GET"])
def trigger_update():
    payroll.loadWorkBooks()
    return jsonify(True)

"""
This method is responsible for getting all of the logged errors.

returns..
    A json array containing error json objects
"""
@app.route("/get_errors", methods = ["GET"])
def get_errors():
    return jsonify(Logger.getErrors())

"""
This method is responsible for triggering a clear errors call.

returns..
    True upon completion
"""
@app.route("/clear_errors", methods = ["GET"])
def clear_errors():
    Logger.clearErrors()
    return jsonify(True)

"""
This method is responsible for getting the generation messages.

returns..
    A json array containing a list of strings
"""
@app.route("/get_generation_messages", methods = ["GET"])
def get_generation_messages():
    return jsonify(Logger.getGenerateMessages())

"""
This method is responsible for clearing the saved generation messages.

returns..
    True upon completion
"""
@app.route("/clear_generation_messages", methods = ["GET"])
def clear_generation_messages():
    Logger.clearGenerateMessages()
    return jsonify(True)
